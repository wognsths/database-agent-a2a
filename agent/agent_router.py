from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse, StreamingResponse
import asyncio

from .agent import DBAgent, DBAgentResponse

db_agent = DBAgent()

def get_db_agent():
    return db_agent

router = APIRouter()

class QueryInput(BaseModel):
    query: str
    session_id: str

@router.post("/query")
async def handle_query(data: QueryInput, agent: DBAgent = Depends(get_db_agent)):
    res: DBAgentResponse = agent.invoke(data.query, data.session_id)
    return JSONResponse({
        "is_task_complete":  res.status == "completed",
        "require_user_input": res.status == "input_required",
        "content":           res.content,
        "data":              res.data,
    })

async def stream_generator(agent, query, session_id):
    import json
    async for chunk in agent.stream(query, session_id):
        yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"

@router.post("/query/stream")
async def handle_stream_query(data: QueryInput, agent: DBAgent = Depends(get_db_agent)):
    return StreamingResponse(
        stream_generator(agent, data.query, data.session_id),
        media_type="text/event-stream"
    )