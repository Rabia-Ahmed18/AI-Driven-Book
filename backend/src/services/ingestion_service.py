from typing import Dict, Any
import time
import uuid
from uuid import UUID
from backend.src.utils.text_splitter import text_splitter
from backend.src.core.vector_store import vector_store
from backend.src.models.book import BookCreate
from openai import AsyncOpenAI
from backend.src.core.config import settings


class IngestionService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def ingest_book(self, book_data: BookCreate, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process and ingest a book into the system
        """
        start_time = time.time()

        try:
            # Create the book in the database
            from .database_service import DatabaseService
            db_service = DatabaseService()
            book = await db_service.create_book(book_data)
            book_id = book.id

            # Split the content into chunks
            chunks = text_splitter.split_text(content)

            # Generate embeddings for each chunk
            vectors = []
            for chunk in chunks:
                # Generate embedding using OpenAI
                response = await self.openai_client.embeddings.create(
                    input=chunk["content"],
                    model=settings.embedding_model
                )
                embedding = response.data[0].embedding

                vectors.append({
                    "vector": embedding,
                    "content": chunk["content"],
                    "metadata": {**chunk.get("metadata", {}), **(metadata or {}), "book_id": str(book_id)}
                })

            # Store vectors in Qdrant
            vector_store.add_vectors(str(book_id), vectors)

            # Update book's chunk count
            book.chunk_count = len(chunks)

            processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

            return {
                "book_id": book_id,
                "chunks_created": len(chunks),
                "processing_time_ms": processing_time
            }

        except Exception as e:
            raise Exception(f"Error during book ingestion: {str(e)}")