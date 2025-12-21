from sqlalchemy import Column, Integer, String, DateTime, Text, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from ..database import Base
import uuid


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(PG_UUID(as_uuid=True), ForeignKey("book_metadata.book_id"), nullable=False)
    content = Column(Text, nullable=False)
    source_file = Column(String(500), nullable=False)
    source_section = Column(String(255), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    embedding_vector_id = Column(String, nullable=False)  # ID in Qdrant
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    checksum = Column(String(64), nullable=True)  # SHA-256 hash of the content