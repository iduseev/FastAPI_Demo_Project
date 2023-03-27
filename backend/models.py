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
    username: str = Field(..., example="johndoe")
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="johndoe@example.com")
    disabled: Optional[bool] = Field(False)


class UserInDB(User):
    hashed_password: str


class Message(BaseModel):
    message: str = Field(..., example="Default message")


class Error(Message):
    status_code: int = Field(..., example=404)
