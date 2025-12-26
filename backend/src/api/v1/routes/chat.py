from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from uuid import UUID
import uuid
import time

from src.models.chat_session import ChatSessionCreate
from src.models.interaction import InteractionCreate
from src.services.chat_service import ChatService
from src.services.rag_service import RAGService
from src.core.database import get_db
from src.utils.validators import validate_user_query


router = APIRouter()


@router.post("/", response_model=dict)
async def chat(
    user_query: str,
    book_id: str,
    selected_text: Optional[str] = None,
    session_id: Optional[str] = None
):
    """
    Chat endpoint that handles user queries about book content
    """
    try:
        # Validate inputs
        validate_user_query(user_query)
        
        # Validate UUIDs
        try:
            book_uuid = UUID(book_id)
            session_uuid = UUID(session_id) if session_id else None
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid UUID format"
            )
        
        # Initialize services
        rag_service = RAGService()
        chat_service = ChatService()
        
        # Process the query based on context
        start_time = time.time()
        
        if selected_text:
            # Use selection context - prioritize the selected text
            response = await rag_service.get_selection_context_response(
                user_query, selected_text, book_id
            )
        else:
            # Use global context - search the entire book
            response = await rag_service.get_global_context_response(
                user_query, book_id
            )
        
        response_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Create or update session
        if not session_uuid:
            session_data = ChatSessionCreate(
                user_id=uuid.uuid4(),  # In a real app, this would come from auth
                book_id=book_uuid,
                title=user_query[:50] + "..." if len(user_query) > 50 else user_query
            )
            session = await chat_service.create_session(session_data)
            session_id = str(session.id)
        else:
            session = await chat_service.get_session(session_uuid)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found"
                )
        
        # Save the interaction
        interaction_data = InteractionCreate(
            session_id=UUID(session_id),
            user_query=user_query,
            assistant_response=response.get("response", ""),
            selected_text=selected_text,
            citations=response.get("citations", []),
            response_time_ms=response_time
        )
        await chat_service.create_interaction(interaction_data)
        
        return {
            "response": response.get("response", ""),
            "citations": response.get("citations", []),
            "response_time_ms": response_time,
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )