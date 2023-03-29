# backend/models.py

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class BookShelf(BaseModel):
    """
    CURRENTLY NOT IN USE YET
    """
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
    password: str = Field(..., example="weak_password")
    disabled: bool = Field(..., example=False)
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="johndoe@example.com")


class UserInDB(BaseModel):
    username: str = Field(..., example="johndoe")
    hashed_password: str = Field(..., example="$2b$12$zsy2fnsZCwyFsc45bZier.rtGG2tLXLKGFpt/5wP8TVCf9tewDrjK")
    disabled: bool = Field(..., example=False)
    full_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="johndoe@example.com")


class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    token_type: str = Field(..., example="Bearer")
    expires_at: Optional[str] = Field(None, example="2023-03-30T13:22:01.366168+06:00")
    expires_in: Optional[int] = Field(None, example=21600)
    updated_at: Optional[str] = Field(None, example="2023-03-29T07:22:01.366168+00:00")


class TokenData(BaseModel):
    username: Optional[str] = Field(None, example="johndoe")


class Message(BaseModel):
    message: str = Field(..., example="Default message")


class Error(Message):
    status_code: int = Field(..., example=404)
