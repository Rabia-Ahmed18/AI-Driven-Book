from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = None
    description: Optional[str] = None
    language: str = Field(default="en", pattern=r"^[a-z]{2}$")

    @field_validator('isbn', mode='before')
    @classmethod
    def validate_isbn(cls, v):
        if v is None:
            return v

        # Remove any hyphens
        clean_isbn = v.replace('-', '')

        # Check if it's ISBN-10 or ISBN-13
        if len(clean_isbn) == 10:
            # Basic ISBN-10 validation
            if not clean_isbn[:-1].isdigit():
                raise ValueError('Invalid ISBN-10')
            # Last character can be digit or X
            if not (clean_isbn[-1].isdigit() or clean_isbn[-1].upper() == 'X'):
                raise ValueError('Invalid ISBN-10')
        elif len(clean_isbn) == 13:
            # Basic ISBN-13 validation
            if not clean_isbn.isdigit():
                raise ValueError('Invalid ISBN-13')
        else:
            raise ValueError('ISBN must be either 10 or 13 digits')

        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = Field(None, pattern=r"^[a-z]{2}$")

    @field_validator('isbn', mode='before')
    @classmethod
    def validate_isbn(cls, v):
        if v is None:
            return v

        # Remove any hyphens
        clean_isbn = v.replace('-', '')

        # Check if it's ISBN-10 or ISBN-13
        if len(clean_isbn) == 10:
            # Basic ISBN-10 validation
            if not clean_isbn[:-1].isdigit():
                raise ValueError('Invalid ISBN-10')
            # Last character can be digit or X
            if not (clean_isbn[-1].isdigit() or clean_isbn[-1].upper() == 'X'):
                raise ValueError('Invalid ISBN-10')
        elif len(clean_isbn) == 13:
            # Basic ISBN-13 validation
            if not clean_isbn.isdigit():
                raise ValueError('Invalid ISBN-13')
        else:
            raise ValueError('ISBN must be either 10 or 13 digits')

        return v


class Book(BookBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    chunk_count: int = 0

    class Config:
        from_attributes = True