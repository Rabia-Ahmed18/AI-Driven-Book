from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None
    book_id: str


class SourceReference(BaseModel):
    chunk_id: str
    content: str
    source_file: str
    source_section: Optional[str] = None
    relevance_score: float


class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[SourceReference] = []


class IngestionRequest(BaseModel):
    book_id: str
    source_path: str
    chunk_size: int = 1000
    chunk_overlap: int = 100


class IngestionResponse(BaseModel):
    status: str
    chunks_processed: int
    book_id: str


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[dict]  # Contains message details