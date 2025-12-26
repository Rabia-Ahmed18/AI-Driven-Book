from typing import List, Optional
from uuid import UUID
from datetime import datetime
import uuid as uuid_pkg
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.src.models.book import Book, BookCreate
from backend.src.core.database import SessionLocal, engine


# Define the SQLAlchemy model
Base = declarative_base()


class BookDB(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, index=True, nullable=True)
    description = Column(Text, nullable=True)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chunk_count = Column(Integer, default=0)


# Create tables
Base.metadata.create_all(bind=engine)


class DatabaseService:
    def __init__(self, db: Session = None):
        self.db = db if db else SessionLocal()

    async def create_book(self, book_data: BookCreate) -> Book:
        """Create a new book in the database"""
        # Create book instance
        book_uuid = str(uuid_pkg.uuid4())
        db_book = BookDB(
            id=book_uuid,
            title=book_data.title,
            author=book_data.author,
            isbn=book_data.isbn,
            description=book_data.description,
            language=book_data.language,
            chunk_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)

        # Convert to Pydantic model
        return Book(
            id=book_uuid,
            title=db_book.title,
            author=db_book.author,
            isbn=db_book.isbn,
            description=db_book.description,
            language=db_book.language,
            chunk_count=db_book.chunk_count,
            created_at=db_book.created_at,
            updated_at=db_book.updated_at
        )

    async def get_book(self, book_id: UUID) -> Optional[Book]:
        """Get a book by ID"""
        db_book = self.db.query(BookDB).filter(BookDB.id == str(book_id)).first()

        if db_book:
            return Book(
                id=db_book.id,
                title=db_book.title,
                author=db_book.author,
                isbn=db_book.isbn,
                description=db_book.description,
                language=db_book.language,
                chunk_count=db_book.chunk_count,
                created_at=db_book.created_at,
                updated_at=db_book.updated_at
            )
        return None

    async def get_all_books(self) -> List[Book]:
        """Get all books"""
        db_books = self.db.query(BookDB).all()

        books = []
        for db_book in db_books:
            books.append(Book(
                id=db_book.id,
                title=db_book.title,
                author=db_book.author,
                isbn=db_book.isbn,
                description=db_book.description,
                language=db_book.language,
                chunk_count=db_book.chunk_count,
                created_at=db_book.created_at,
                updated_at=db_book.updated_at
            ))

        return books

    def close(self):
        """Close the database session"""
        self.db.close()