from sqlalchemy import Column, Integer, String, DateTime, Text, UUID, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from ..database import Base
import uuid


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("sessions.session_id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sources = Column(JSON)  # References to document chunks used in the response
    selected_text = Column(Text, nullable=True)  # Text that was selected by the user
    response_time_ms = Column(Integer, nullable=True)  # Time to generate response