from sqlalchemy import Column, Integer, String, DateTime, Text, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from ..database import Base
import uuid


class BookMetadata(Base):
    __tablename__ = "book_metadata"

    book_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    source_path = Column(String(500), nullable=False)