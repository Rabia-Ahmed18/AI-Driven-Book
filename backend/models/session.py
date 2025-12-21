from sqlalchemy import Column, Integer, String, DateTime, Text, UUID, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from ..database import Base
import uuid


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=True)  # Optional, for authenticated users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata = Column(JSON)  # Flexible storage for additional session data