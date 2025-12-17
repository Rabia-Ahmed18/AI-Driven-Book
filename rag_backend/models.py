from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str
    selected_context: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    source_citations: List[str]


class IngestRequest(BaseModel):
    source_path: str
    force_reprocess: Optional[bool] = False


class IngestResponse(BaseModel):
    status: str
    processed_files: List[str]
    errors: Optional[List[str]] = []