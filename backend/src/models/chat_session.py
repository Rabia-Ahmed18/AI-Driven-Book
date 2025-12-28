from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class ChatSession(BaseModel):
    """
    Represents a conversation between user and the chatbot with history of messages
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None  # optional, for identifying users
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }