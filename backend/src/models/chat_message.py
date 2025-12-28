from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4


class ChatMessage(BaseModel):
    """
    Represents a single message in a chat session
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str  # foreign key to Chat Session
    role: str  # either "user" or "assistant"
    content: str  # the actual message content
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context_used: Optional[str] = None  # optional, the selected text context if applicable
    sources: List[Dict[str, Any]] = Field(default_factory=list)  # citations to source documents

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def __init__(self, **data):
        super().__init__(**data)
        if self.role not in ["user", "assistant"]:
            raise ValueError("Role must be either 'user' or 'assistant'")
        if not self.content.strip():
            raise ValueError("Content must not be empty")