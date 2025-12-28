from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from uuid import uuid4


class QueryResponse(BaseModel):
    """
    Represents the system's response to a user's query
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    query_id: str  # foreign key to Query Request
    content: str  # the response content
    sources: List[Dict[str, Any]] = Field(default_factory=list)  # citations to source documents
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tokens_used: int = 0  # number of tokens used in the response

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def __init__(self, **data):
        super().__init__(**data)
        if not self.content.strip():
            raise ValueError("Content must not be empty")
        if self.tokens_used < 0:
            raise ValueError("Tokens used must be non-negative")