from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from uuid import UUID

from backend.src.models.book import Book, BookCreate
from backend.src.services.database_service import DatabaseService


router = APIRouter()


@router.get("/", response_model=List[Book])
async def list_books():
    """
    List all books in the system
    """
    try:
        db_service = DatabaseService()
        books = await db_service.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving books: {str(e)}"
        )


@router.post("/", response_model=Book)
async def create_book(
    title: str,
    author: str,
    isbn: str = None,
    description: str = None,
    language: str = "en"
):
    """
    Create a new book entry without ingesting content
    """
    try:
        book_data = BookCreate(
            title=title,
            author=author,
            isbn=isbn,
            description=description,
            language=language
        )

        db_service = DatabaseService()
        book = await db_service.create_book(book_data)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating book: {str(e)}"
        )


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """
    Get details about a specific book
    """
    try:
        # Validate UUID
        book_uuid = UUID(book_id)

        db_service = DatabaseService()
        book = await db_service.get_book(book_uuid)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        return book
    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving book: {str(e)}"
        )