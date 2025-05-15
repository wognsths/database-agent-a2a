from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class SQLqueryRequest(BaseModel):
    sql_query: str = Field(..., description="(SQL) Structured Query Language")
    session_id: Optional[str] = Field(None, description="Session ID to recognize same state")

    @property
    def query(self) -> str:
        return self.sql_query

class SQLqueryResponse(BaseModel):
    sql_query: str = Field(..., description="Returns SQL")
    success: bool = Field(..., description="Check if SQL query is successful")
    data: Optional[List[Dict[str, Any]]] = Field(
        None, description="Records"
    )
    error_message: Optional[str] = Field(
        None, description="Error message (if fails)"
    )
    rows_returned: Optional[int] = Field(
        None, description="Length of the data (If success)"
    )

class DescriptionUploadRequest(BaseModel):
    description_data: Dict[str, Any] = Field(
        ..., description="Full user-defined table/column descriptions"
    )

class DescriptionHandlerResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class TableDescriptionRequest(BaseModel):
    table_name: str
    description: str

class ColumnDescriptionRequest(BaseModel):
    table_name: str
    column_name: str
    description: str