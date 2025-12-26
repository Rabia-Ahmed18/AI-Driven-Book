from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ChatSessionBase(BaseModel):
    user_id: UUID
    book_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    active: bool = True


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    active: Optional[bool] = None


class ChatSession(ChatSessionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True