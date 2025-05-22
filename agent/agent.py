from typing import Any, Dict, Optional, Literal, AsyncIterable
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, ToolMessage

from .tools import TOOLS
from .prompts import SYSTEM_INSTRUCTION

class DBAgentResponse(BaseModel):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)
    status: Literal["input_required", "completed", "error"] = "input_required"
    data: Optional[Any] = None
    content: str

memory = MemorySaver()

class DBAgent:
    SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.tools = TOOLS
        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=DBAgentResponse
        )

    def invoke(self, query: str, session_id: str) -> DBAgentResponse:
        config = {"configurable": {"thread_id": session_id}}
        self.graph.invoke({"messages": [("user", query)]}, config)
        sr = self.graph.get_state(config).values.get("structured_response")
        if isinstance(sr, DBAgentResponse):
            return sr
        return DBAgentResponse(status="error", message="Unexpected error: unable to retrieve agent response.")

    async def stream(self, query: str, session_id: str) -> AsyncIterable[Dict[str, Any]]:
        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": session_id}}

        last_tool: Optional[str] = None

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if isinstance(message, AIMessage) and message.tool_calls:
                last_tool = message.tool_calls[0]['name']
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": f"Calling tool `{last_tool}` with arguments {message.tool_calls[0]['arguments']}"
                }
            elif isinstance(message, ToolMessage):
                if last_tool == "execute_query":
                    result = message.content
                    if not result.get("success", False):
                        yield {
                            "is_task_complete": False,
                            "require_user_input": False,
                            "data": None,
                            "content": f"SQL Error: {result.get('error_message')}. Retrying..."
                        }
                        continue
                    data = result.get("data")
                    yield {
                        "is_task_complete": False,
                        "require_user_input": False,
                        "data": data,
                        "content": "Here are the results of your query."
                    }
                else:
                    yield {
                        "is_task_complete": False,
                        "require_user_input": False,
                        "data": message.content,
                        "content": f"Returns the results of tool execution of {last_tool}"
                    }

        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        if isinstance(structured_response, DBAgentResponse):
            yield {
                "is_task_complete": structured_response.status == "completed",
                "require_user_input": structured_response.status == "input_required",
                "data": structured_response.data,
                "content": structured_response.content
            }
        else:
            yield {
                "is_task_complete": False,
                "require_user_input": True,
                "content": "We are unable to process your request at the moment. Please try again."
            }

    def get_agent_response(self, config: Dict[str, Any]) -> Dict[str, Any]:
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        if isinstance(structured_response, DBAgentResponse):
            if structured_response.status == "input_required":
                return {"is_task_complete": False, "require_user_input": True, "content": structured_response.message}
            if structured_response.status == "error":
                return {"is_task_complete": False, "require_user_input": True, "content": structured_response.message}
            if structured_response.status == "completed":
                return {"is_task_complete": True, "require_user_input": False, "content": structured_response.message, "data": structured_response.data}
        return {"is_task_complete": False, "require_user_input": True, "content": "We are unable to process your request at the moment. Please try again."}

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
