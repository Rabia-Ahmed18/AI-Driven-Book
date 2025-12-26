from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


class Citation(BaseModel):
    chunk_id: UUID
    text: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[dict] = None


class InteractionBase(BaseModel):
    session_id: UUID
    user_query: str = Field(..., min_length=1, max_length=10000)
    assistant_response: str = Field(..., min_length=1, max_length=10000)
    selected_text: Optional[str] = None
    citations: Optional[List[Citation]] = None
    response_time_ms: Optional[int] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    assistant_response: Optional[str] = Field(None, min_length=1, max_length=10000)
    citations: Optional[List[Citation]] = None
    response_time_ms: Optional[int] = None


class Interaction(InteractionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True