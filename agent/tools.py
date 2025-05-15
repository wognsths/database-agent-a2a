from typing import Any, List, Dict, Optional
from langchain_core.tools import tool
import httpx
from settings.db_settings import get_dbsettings
from dotenv import load_dotenv
load_dotenv()
import os

def request_helper(method: str, endpoint: str, **kwargs) -> Any:
    base = "http://db-service:8001"
    url  = f"{base}{endpoint}"
    try:
        with httpx.Client(timeout=5.0) as client:
            if method.lower() == "get":
                response = client.get(url, **kwargs)
            elif method.lower() == "post":
                response = client.post(url, **kwargs)
            else:
                raise ValueError("Unsupported HTTP method")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

@tool
def get_database_schema():
    """Fetch the full database schema."""
    return request_helper("get", "/db/schema")

@tool
def get_table_list() -> Any:
    """Fetch the list of tables in the database."""
    return request_helper("get", "/db/tables")

@tool
def get_table_samples(table_name: str, limit: int = 5) -> Any:
    """Fetch sample data from a specific table."""
    return request_helper("get", f"/db/{table_name}/samples", params={"limit": limit})

@tool
def get_table_summary(table_name: str) -> Any:
    """Fetch summaries of a specific table."""
    return request_helper("get", f"/db/{table_name}/summary")

@tool
def execute_query(query: str, session_id: str) -> Any:
    """Execute the SQL query"""
    return request_helper(
        "post",
        "/db/query",
        json={
            "sql_query": query,
            "session_id": session_id
        }
    )

@tool
def get_full_description_of_database() -> Any:
    """Fetch the full description of the database."""
    return request_helper("get", "/user-description/full")

@tool
def get_table_description() -> Any:
    """Fetch the description of tables."""
    return request_helper("get", f"/user-description/tables")

@tool
def get_column_description(table_name: str) -> Any:
    """Fetch the column description of specific table's description."""
    return request_helper("get", f"/user-description/{table_name}")


TOOLS = [
    get_database_schema,
    get_table_list,
    get_table_samples,
    get_table_summary,
    execute_query,
    get_full_description_of_database,
    get_table_description,
    get_column_description,
]