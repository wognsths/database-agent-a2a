from fastapi import APIRouter, Depends, HTTPException
from core.db.database import db, schema_manager, NoAuthorizationError
from core.db.query_logger import log_sql_response
from .models import SQLqueryRequest, SQLqueryResponse
from typing import Any, Dict, List, Optional

router = APIRouter()

@router.post("/query", response_model=SQLqueryResponse, summary="Run a SQL query")
def run_query(request: SQLqueryRequest) -> SQLqueryResponse:
    try:
        records = db.execute_query(request.sql_query)

        resp = SQLqueryResponse(
            sql_query=request.sql_query,
            success=True,
            data=records,
            rows_returned=len(records),
        )
        log_sql_response(resp)
        return resp
    
    except NoAuthorizationError as e:
        resp = SQLqueryResponse(
            sql_query=request.sql_query,
            success=False,
            error_message=f"NoAuthorizationError: {e}"
        )
        log_sql_response(resp)
        return resp
    
    except Exception as e:
        resp = SQLqueryResponse(
            sql_query=request.sql_query,
            success=False,
            error_message=f"Error: {e}"
        )
        log_sql_response(resp)
        return resp
    
@router.get("/{table_name}/samples", summary="Get sample data of a table")
def get_table_sample(table_name: str, limit: int = 5):
    try:
        sample_data = schema_manager.get_table_sample_data(table_name, limit)
        return {"sample_data": sample_data}
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/schema", response_model=Dict[str, Any], summary="Get full database schema")
async def get_schema():
    try:
        return schema_manager.get_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tables", summary="Get list of tables")
def get_table_list():
    tables = schema_manager.get_tables()
    return {"tables": tables}

@router.get("/{table_name}/summary", summary="Get summaries of a table")
def get_table_summary(table_name: str):
    try:
        summaries = schema_manager.get_table_summary(table_name)
        return {f"Summary of table: {table_name}": summaries}
    except Exception as e:
        return {"error": str(e)}