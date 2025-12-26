from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class UserRole(str):
    READER = "reader"
    CONTENT_ADMIN = "content_admin"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.READER


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True