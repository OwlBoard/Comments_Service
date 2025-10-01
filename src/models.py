# src/models.py
from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import List
from datetime import datetime, timezone

class Comment(Document):
    dashboard_id: PydanticObjectId
    user_id: PydanticObjectId
    content: str = Field(..., max_length=500)
    coordinates: List[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "comments"