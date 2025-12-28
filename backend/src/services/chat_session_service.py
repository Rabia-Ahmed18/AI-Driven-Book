from typing import Optional, List
from datetime import datetime, timedelta
from ..models.chat_session import ChatSession
from ..models.chat_message import ChatMessage
from ..core.logging import app_logger
from uuid import uuid4


class ChatSessionService:
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using in-memory storage for demo purposes
        self.sessions = {}
        self.messages = {}

    def create_session(self, user_id: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session_id = str(uuid4())
        session = ChatSession(
            session_id=session_id,
            user_id=user_id
        )
        self.sessions[session_id] = session
        self.messages[session_id] = []
        app_logger.info(f"Created new session: {session_id}")
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get an existing chat session"""
        return self.sessions.get(session_id)

    def add_message(self, session_id: str, role: str, content: str, 
                   context_used: Optional[str] = None, 
                   sources: List[dict] = None) -> ChatMessage:
        """Add a message to a session"""
        if sources is None:
            sources = []
        
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            context_used=context_used,
            sources=sources
        )
        
        if session_id in self.messages:
            self.messages[session_id].append(message)
        else:
            # Create session if it doesn't exist
            self.create_session()
            self.messages[session_id].append(message)
        
        # Update session timestamp
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.updated_at = datetime.utcnow()
        
        app_logger.info(f"Added message to session {session_id}")
        return message

    def get_messages(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session"""
        return self.messages.get(session_id, [])

    def delete_session(self, session_id: str) -> bool:
        """Delete a session and its messages"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if session_id in self.messages:
                del self.messages[session_id]
            app_logger.info(f"Deleted session: {session_id}")
            return True
        return False

    def cleanup_old_sessions(self, days: int = 30):
        """Remove sessions older than specified days (for data retention policy)"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        old_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.updated_at < cutoff_time:
                old_sessions.append(session_id)
        
        for session_id in old_sessions:
            self.delete_session(session_id)
        
        app_logger.info(f"Cleaned up {len(old_sessions)} sessions older than {days} days")


# Global instance
chat_session_service = ChatSessionService()