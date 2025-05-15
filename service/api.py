from .db_router import router as db_router
from .schema_router import router as schema_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.db.database import db
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    with db.engine.connect() as conn:
        conn.execute(text("Select 1"))
    print("DB connection is verified")

    yield

    db.engine.dispose()
    print("DB connection closed")

app = FastAPI(
    title="Database API",
    description="Utility Functions for Database Serving API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(db_router, prefix="/db", tags = ["Database"])
app.include_router(schema_router, prefix="/description", tags=["Database Manager"])

