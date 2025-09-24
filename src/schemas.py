from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from beanie import PydanticObjectId
from datetime import datetime

# --------- Comment Schemas ---------
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, json_schema_extra={"example": "Gran dibujo"})

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=500, json_schema_extra={"example": "He actualizado mi comentario."})

class CommentOut(CommentBase):
    id: PydanticObjectId = Field(..., alias="_id")
    dashboard_id: PydanticObjectId
    user_id: PydanticObjectId
    coordinates: List[float]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
