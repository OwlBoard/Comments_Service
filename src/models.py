# src/models.py
from beanie import Document, PydanticObjectId #si
from pydantic import Field, validator
from typing import List
from datetime import datetime, timezone

class Comment(Document):
    dashboard_id: PydanticObjectId
    user_id: PydanticObjectId
    content: str = Field(..., max_length=500)
    coordinates: List[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El contenido del comentario no puede estar vacío')
        return v.strip()

    @validator('coordinates')
    def coordinates_must_be_valid(cls, v):
        if len(v) != 2:
            raise ValueError('Las coordenadas deben tener exactamente dos valores (x,y)')
        return v

    class Settings:
        name = "comments"