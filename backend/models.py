# backend/models.py

from typing import Optional, Dict, List, Any, Union
from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4


class BookShelf(BaseModel):
    category: Optional[str] = Field(None, example="Adventures")
    location: Optional[str] = Field(None, example="London, 96 Euston Road")


class IncomingBookData(BaseModel):
    book_name: str = Field(..., example="The adventures of Sherlock Holmes")
    author: Optional[str] = Field(None, example="Sir Arthur Conan Doyle")
    description: Optional[str] = Field(None, example="The Adventures of Sherlock Holmes is a collection of twelve short stories")


class Book(IncomingBookData):
    book_id: str = Field(..., example=uuid4().hex)
    available: bool = Field(..., example=False)


class User(BaseModel):
    username: Union[str, None] = Field(default=None, example="alumni")
    full_name: Union[str, None] = Field(default=None, example="John Doe")
    email: Union[EmailStr, None] = Field(..., example="johndoe@example.com")
    disabled: Union[bool, None] = Field(default=False)


class Message(BaseModel):
    message: str = Field(..., example="Default message")


class Error(Message):
    status_code: int = Field(..., example=404)
