from sqlalchemy.orm import Session
from typing import Optional
from .models.session import Session as SessionModel
from .models.chat_message import ChatMessage
from .schemas.chat import ChatRequest
import uuid


class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """
        Get an existing session or create a new one if session_id is not provided or doesn't exist.
        
        Args:
            session_id: Optional session ID
            
        Returns:
            Session ID (either the provided one or a newly created one)
        """
        if session_id:
            # Check if session exists
            existing_session = self.db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
            if existing_session:
                return session_id
        
        # Create a new session
        new_session = SessionModel(session_id=uuid.uuid4())
        self.db.add(new_session)
        self.db.commit()
        
        return str(new_session.session_id)
    
    def add_message_to_session(self, session_id: str, role: str, content: str, sources: list = None, selected_text: str = None) -> bool:
        """
        Add a message to a session.
        
        Args:
            session_id: Session ID
            role: Role of the message ('user' or 'assistant')
            content: Content of the message
            sources: List of sources used in the response
            selected_text: Text that was selected by the user when this message was created
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                sources=sources or [],
                selected_text=selected_text
            )
            
            self.db.add(message)
            self.db.commit()
            
            return True
        except Exception as e:
            self.db.rollback()
            return False
    
    def get_session_history(self, session_id: str) -> list:
        """
        Get the history of messages for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of messages in the session
        """
        messages = self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
        return [message.__dict__ for message in messages]