from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from beanie import PydanticObjectId
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, json_schema_extra={"example": "Gran dibujo"})

class CommentCreate(CommentBase):
    coordinates: str = Field(..., pattern=r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$", json_schema_extra={"example": "150.5,320.0"})

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=500, json_schema_extra={"example": "He actualizado mi comentario."})
    coordinates: Optional[List[float]] = Field(None, min_items=2, max_items=2, json_schema_extra={"example": [150.5, 320.0]})

class CommentOut(CommentBase):
    id: PydanticObjectId = Field(..., alias="_id")
    dashboard_id: PydanticObjectId
    user_id: PydanticObjectId
    coordinates: List[float]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
