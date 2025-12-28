from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4


class DocumentChunk(BaseModel):
    """
    Represents a segment of content from the book with associated metadata
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str = Field(..., min_length=1)
    source_url: str  # URL of the original document
    heading: str = ""  # heading/section title where the chunk appears
    embedding: Optional[list] = None  # vector embedding of the content
    metadata: Dict[str, Any] = Field(default_factory=dict)  # additional metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def __init__(self, **data):
        super().__init__(**data)
        if self.embedding is not None and len(self.embedding) != 1536:
            raise ValueError("Embedding must have exactly 1536 dimensions for OpenAI text-embedding-3-small")