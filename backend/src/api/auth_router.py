from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..services.chat_session_service import chat_session_service
from ..core.logging import app_logger
import uuid

auth_router = APIRouter()

class CreateSessionRequest(BaseModel):
    user_id: Optional[str] = None

class CreateSessionResponse(BaseModel):
    session_id: str
    message: str

@auth_router.post("/session", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    try:
        # Create a new chat session
        session = chat_session_service.create_session(user_id=request.user_id)
        
        response = CreateSessionResponse(
            session_id=session.session_id,
            message="Session created successfully"
        )
        
        app_logger.info(f"Created new session: {session.session_id}")
        return response
    except Exception as e:
        app_logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    try:
        success = chat_session_service.delete_session(session_id)
        if success:
            app_logger.info(f"Deleted session: {session_id}")
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        app_logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")