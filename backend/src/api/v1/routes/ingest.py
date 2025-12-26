from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import Dict, Any
import uuid

from backend.src.models.book import BookCreate
from backend.src.services.ingestion_service import IngestionService
from backend.src.utils.validators import validate_input, validate_book_content
from backend.src.utils.text_splitter import text_splitter


router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def ingest_book(
    title: str,
    author: str,
    content: str,
    metadata: Dict[str, Any] = None
):
    """
    Ingest a book into the system, process it, and store for retrieval
    """
    try:
        # Validate inputs
        validate_book_content(content)

        # Create book data
        book_data = BookCreate(
            title=title,
            author=author,
            description=metadata.get('description') if metadata else None,
            language=metadata.get('language', 'en') if metadata else 'en'
        )

        # Initialize ingestion service
        ingestion_service = IngestionService()

        # Process and store the book
        result = await ingestion_service.ingest_book(
            book_data=book_data,
            content=content,
            metadata=metadata or {}
        )

        return {
            "book_id": str(result["book_id"]),
            "chunks_created": result["chunks_created"],
            "processing_time_ms": result["processing_time_ms"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during ingestion: {str(e)}"
        )