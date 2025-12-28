from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import uuid4
from ..services.rag_service import rag_service
from ..services.chat_session_service import chat_session_service
from ..models.query_request import QueryRequest
from ..models.query_response import QueryResponse
from ..core.logging import app_logger

query_router = APIRouter()


class QueryRequestModel(BaseModel):
    question: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None


class QueryResponseModel(BaseModel):
    response_id: str
    session_id: str
    answer: str
    sources: List[Dict[str, Any]]
    timestamp: str


@query_router.post("/query", response_model=QueryResponseModel)
async def query_endpoint(request: QueryRequestModel):
    try:
        # Create or retrieve session
        session_id = request.session_id or str(uuid4())
        session = chat_session_service.get_session(session_id)
        if not session:
            session = chat_session_service.create_session()
            session_id = session.session_id

        # Perform RAG query
        if request.selected_text:
            # Use context-aware query
            result = rag_service.query_with_context(
                question=request.question,
                selected_text=request.selected_text
            )
        else:
            # Use global query
            result = rag_service.query_global(request.question)

        # Add messages to session
        chat_session_service.add_message(
            session_id=session_id,
            role="user",
            content=request.question,
            context_used=request.selected_text
        )

        chat_session_service.add_message(
            session_id=session_id,
            role="assistant",
            content=result["answer"],
            sources=result["sources"]
        )

        response = QueryResponseModel(
            response_id=str(uuid4()),
            session_id=session_id,
            answer=result["answer"],
            sources=result["sources"],
            timestamp="2025-12-28T10:00:00Z"  # In a real implementation, use actual timestamp
        )

        app_logger.info(f"Processed query for session {session_id}")
        return response

    except Exception as e:
        app_logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


class QuerySelectionRequestModel(BaseModel):
    question: str
    selected_text: str
    session_id: Optional[str] = None


@query_router.post("/query-selection", response_model=QueryResponseModel)
async def query_selection_endpoint(request: QuerySelectionRequestModel):
    try:
        # Create or retrieve session
        session_id = request.session_id or str(uuid4())
        session = chat_session_service.get_session(session_id)
        if not session:
            session = chat_session_service.create_session()
            session_id = session.session_id

        # Perform RAG query with selected text context
        result = rag_service.query_with_context(
            question=request.question,
            selected_text=request.selected_text
        )

        # Add messages to session
        chat_session_service.add_message(
            session_id=session_id,
            role="user",
            content=request.question,
            context_used=request.selected_text
        )

        chat_session_service.add_message(
            session_id=session_id,
            role="assistant",
            content=result["answer"],
            sources=result["sources"]
        )

        response = QueryResponseModel(
            response_id=str(uuid4()),
            session_id=session_id,
            answer=result["answer"],
            sources=result["sources"],
            timestamp="2025-12-28T10:00:00Z"  # In a real implementation, use actual timestamp
        )

        app_logger.info(f"Processed query with selection for session {session_id}")
        return response

    except Exception as e:
        app_logger.error(f"Error processing query with selection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")