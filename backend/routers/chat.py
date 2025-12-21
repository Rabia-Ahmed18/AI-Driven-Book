from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import uuid

from ..database import get_db
from ..schemas.chat import ChatRequest, ChatResponse, IngestionRequest, IngestionResponse, SessionHistoryResponse
from ..rag import RAGService
from ..session_service import SessionService
from ..models.book_metadata import BookMetadata

# Initialize services
rag_service = RAGService()

app = APIRouter()


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process user queries and return AI-generated responses.
    This endpoint handles chat requests with two possible flows:
    - Standard RAG: Vector search in Qdrant based on user query
    - Targeted RAG: Context strictly limited to user-selected text from the frontend
    """
    try:
        # Validate that the book exists
        book_exists = db.query(BookMetadata).filter(BookMetadata.book_id == chat_request.book_id).first()
        if not book_exists:
            raise HTTPException(status_code=400, detail="Invalid book_id")
        
        # Get or create session
        session_service = SessionService(db)
        session_id = session_service.get_or_create_session(chat_request.session_id)
        
        # Add user message to session
        session_service.add_message_to_session(
            session_id=session_id,
            role="user",
            content=chat_request.query,
            selected_text=chat_request.selected_text
        )
        
        # Get response from RAG service
        result = rag_service.get_answer(
            query=chat_request.query,
            book_id=chat_request.book_id,
            selected_text=chat_request.selected_text
        )
        
        # Add assistant message to session
        session_service.add_message_to_session(
            session_id=session_id,
            role="assistant",
            content=result["response"],
            sources=result["sources"]
        )
        
        # Return the response
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            sources=result["sources"]
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/ingest", response_model=IngestionResponse)
async def ingest_endpoint(ingestion_request: IngestionRequest):
    """
    Process book content and store embeddings.
    """
    try:
        # This would call the ingestion pipeline
        # For now, we'll just return a placeholder response
        # In a real implementation, we would call the IngestionPipeline class
        from .ingestion_script import IngestionPipeline
        
        pipeline = IngestionPipeline(
            book_id=ingestion_request.book_id,
            source_path=ingestion_request.source_path,
            chunk_size=ingestion_request.chunk_size,
            chunk_overlap=ingestion_request.chunk_overlap
        )
        
        chunks_processed = pipeline.process_and_store()
        
        return IngestionResponse(
            status="completed",
            chunks_processed=chunks_processed,
            book_id=ingestion_request.book_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.get("/sessions/{session_id}", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieve chat history for a session.
    """
    try:
        # Validate session ID format
        try:
            UUID(session_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid session_id format")
        
        session_service = SessionService(db)
        messages = session_service.get_session_history(session_id)
        
        if not messages:
            raise HTTPException(status_code=404, detail="Session not found or has no messages")
        
        return SessionHistoryResponse(
            session_id=session_id,
            messages=messages
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG-Based AI Book Chatbot API"}