# backend/models.py

from typing import Optional, Dict, List, Any, Union
from pydantic import BaseModel, Field, EmailStr


class BookShelf(BaseModel):
    category: Optional[str] = Field(None, example="Adventures")
    location: Optional[str] = Field(None, example="London, 96 Euston Road")


class IncomingBookData(BaseModel):
    book_name: str = Field(..., example="The adventures of Sherlock Holmes")
    author: Optional[str] = Field(None, example="Sir Arthur Conan Doyle")
    description: Optional[str] = Field(None, example="The Adventures of Sherlock Holmes is a collection of twelve short stories")


class Book(IncomingBookData):
    book_id: str = Field(..., example="936d4b41ec874007af150bbac8e714c3")
    available: bool = Field(..., example=False)


class User(BaseModel):
    username: str = Field(..., example="johndoe")
    disabled: bool = Field(..., example=False)
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="johndoe@example.com")


class UserInDB(User):
    hashed_password: str = Field(..., example="e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4")


class Message(BaseModel):
    message: str = Field(..., example="Default message")


class Error(Message):
    status_code: int = Field(..., example=404)
