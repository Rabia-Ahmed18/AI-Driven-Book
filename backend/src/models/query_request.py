from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class QueryRequest(BaseModel):
    """
    Represents a user's question with optional selected text context
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    question: str  # the user's question
    selected_text: Optional[str] = None  # optional, text selected by user
    session_id: Optional[str] = None  # optional, session identifier
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    response_id: Optional[str] = None  # optional, reference to the response

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def __init__(self, **data):
        super().__init__(**data)
        if not self.question.strip():
            raise ValueError("Question must not be empty")
        if self.selected_text and not self.selected_text.strip():
            raise ValueError("Selected text, if provided, must not be empty")