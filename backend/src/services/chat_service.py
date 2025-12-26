from typing import Optional
from uuid import UUID
from backend.src.models.chat_session import ChatSession, ChatSessionCreate
from backend.src.models.interaction import Interaction, InteractionCreate


class ChatService:
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use in-memory storage for demonstration
        self.sessions = {}
        self.interactions = {}

    async def create_session(self, session_data: ChatSessionCreate) -> ChatSession:
        """
        Create a new chat session
        """
        import uuid
        from datetime import datetime

        session_id = uuid.uuid4()
        session = ChatSession(
            id=session_id,
            user_id=session_data.user_id,
            book_id=session_data.book_id,
            title=session_data.title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            active=True
        )

        self.sessions[session_id] = session
        return session

    async def get_session(self, session_id: UUID) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        """
        return self.sessions.get(session_id)

    async def create_interaction(self, interaction_data: InteractionCreate) -> Interaction:
        """
        Create a new interaction in a chat session
        """
        import uuid
        from datetime import datetime

        interaction_id = uuid.uuid4()
        interaction = Interaction(
            id=interaction_id,
            session_id=interaction_data.session_id,
            user_query=interaction_data.user_query,
            assistant_response=interaction_data.assistant_response,
            selected_text=interaction_data.selected_text,
            citations=interaction_data.citations,
            created_at=datetime.utcnow(),
            response_time_ms=interaction_data.response_time_ms
        )

        # Add to session's interactions
        session_interactions = self.interactions.get(interaction_data.session_id, [])
        session_interactions.append(interaction)
        self.interactions[interaction_data.session_id] = session_interactions

        return interaction

    async def get_session_interactions(self, session_id: UUID) -> list:
        """
        Get all interactions for a session
        """
        return self.interactions.get(session_id, [])