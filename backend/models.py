# backend/models.py

from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
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


class Visitor(BaseModel):
    visitor_name: str = Field(..., example="John")
    visitor_surname: str = Field(..., example="Doe")
    visitor_id: str = Field(..., example="dg43dp87")
    visitor_age: Optional[int] = Field(None, example=30)


class Message(BaseModel):
    message: str = Field(..., example="Default message")


class Error(Message):
    status_code: int = Field(..., example=404)
