from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from core.db.schema_manager import user_description_manager
from .models import (
    DescriptionUploadRequest,
    DescriptionHandlerResponse,
)
router = APIRouter()

@router.get("/user-description/full", response_model=Dict[str, Any])
async def get_full_description_of_database():
    try:
        description = user_description_manager.get_user_description()
        if not description:
            raise HTTPException(status_code=404, detail="No user-defined description found")
        return description
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-description/tables")
async def get_table_description():
    try:
        description = user_description_manager.get_user_description()
        if not description:
            raise HTTPException(status_code=404, detail="No user-defined description found")
        
        tables = {}
        for key, value in description.items():
            if not key.startswith('_'):
                tables[key] = value
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/user-description", response_model=DescriptionHandlerResponse)
async def create_user_defined_description(request: DescriptionUploadRequest):
    try:
        success = user_description_manager.upload_user_description(request.description_data)
        return DescriptionHandlerResponse(
            success=success,
            message="Description created successfully" if success else "Failed to create description"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dbuser-description/{table_name}", response_model=List[Dict[str, Any]])
async def get_column_description(table_name: str):
    try:
        description = user_description_manager.get_user_description()
        if not description:
            raise HTTPException(status_code=404, detail="No user-defined description found")
            
        if table_name not in description:
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
            
        if "columns" not in description[table_name]:
            raise HTTPException(status_code=404, detail=f"No columns found for table {table_name}")
            
        return description[table_name]["columns"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))