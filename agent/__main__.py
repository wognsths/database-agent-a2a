import os
import logging
from dotenv import load_dotenv

from core.server.server import A2AServer
from core.types import AgentCard, AgentCapabilities, AgentSkill
from core.utils.push_notification_auth import PushNotificationSenderAuth
from .task_manager import AgentTaskManager
from .agent import DBAgent

from fastapi import FastAPI
from starlette.responses import JSONResponse
import uvicorn

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notification_sender_auth = PushNotificationSenderAuth()
notification_sender_auth.generate_jwk()

capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
skill = AgentSkill(
    id="text_to_sql",
    name="Text to SQL",
    description="Converts NL queries into SQL and runs them.",
    tags=["text-to-sql", "database"],
    examples=["Show me the top 5 customers by revenue"]
)

agent_card = AgentCard(
    name="Database Agent",
    description="NL→SQL agent",
    url="http://database-agent:10001/",
    version="1.0.0",
    defaultInputModes=DBAgent.SUPPORTED_CONTENT_TYPES,
    defaultOutputModes=DBAgent.SUPPORTED_CONTENT_TYPES,
    capabilities=capabilities,
    skills=[skill],
)

server = A2AServer(
    agent_card=agent_card,
    task_manager=AgentTaskManager(
        agent=DBAgent(),
        notification_sender_auth=notification_sender_auth,
    ),
    host="0.0.0.0",
    port=10001,
)
a2a_app = server.app

app = FastAPI(title="Database Agent API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

from .agent_router import router as query_router
app.include_router(query_router)

app.mount("/db_agent", a2a_app)

uvicorn.run(app, host="0.0.0.0", port=10001)