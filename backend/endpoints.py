# backend/endpoints.py

import pathlib
from uuid import uuid4
from typing import Union, List, Optional, Dict

from fastapi import FastAPI, Path, Body, Query, HTTPException, status, Request
from fastapi.responses import JSONResponse

from .mock_data import default_book_shelf, default_book
from .models import IncomingBookData, Book, Visitor, Message, Error

app = FastAPI()


@app.get("/")
async def read_root() -> Dict:
    return {"message": "Hello, welcome to the Demo Library API service built using amazing FastAPI framework!"}


@app.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error}
    }
)
def read_book(
    request: Request, 
    book_id: str = Path(..., title="Required book ID", example="cf23df22")
    ) -> Book:
    """_summary_

    :param request: _description_
    :type request: Request
    :param book_id: _description_, defaults to Path(..., title="Required book ID", example="cf23df22")
    :type book_id: str, optional
    :raises HTTPException: _description_
    :return: _description_
    :rtype: Book
    """
    client_host = request.client.host
    print(f"Detected incoming GET request from the client with IP {client_host} ...")

    # todo add authorization via JWT token

    if book_id not in default_book_shelf.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The book with ID {book_id} was not found in the book shelf!"
        )
    return default_book_shelf[book_id]


@app.get(
    "/books",
    status_code=status.HTTP_200_OK,
    response_model=List[Book],
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}}
    )
def show_books(limit: int = Query(default=10, example=10)) -> List[Book]:
    return list(default_book_shelf.values())[: limit]


@app.post(
    "/books/{book_name}",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
    responses={
        status.HTTP_409_CONFLICT: {"model": Error},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}
    }
)
def add_book(
    request: Request,
    incoming_book: IncomingBookData = Body(..., title="Required book data to be added", example=default_book)
    ) -> str:
    client_host = request.client.host
    print(f"Detected incoming GET request from the client with IP {client_host} ...")

    # todo add authorization via JWT token

    incoming_book_data = incoming_book.dict()

    book_name = incoming_book_data.get("book_name")
    author = incoming_book_data.get("author")
    description = incoming_book_data.get("description")

    if book_name in [book.book_name for book in default_book_shelf.values()]:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=Error(
                message=f"The aforementioned book already exists in the book shelf!",
                status_code=status.HTTP_409_CONFLICT
            ).dict()
        )
    book_id = uuid4().hex
    print(f"Assigned new book ID to the added book: {book_id}")
    new_book = Book(
        book_name=book_name,
        book_id=book_id,
        available=True,
        author=author if author else None,
        description=description if description else None
    )
    print(f"Created new book object! Book data:\n{new_book.dict()}")
    default_book_shelf[book_id] = new_book
    print(f"Assigned new book {book_name} to the book shelf! ")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=Message(
            message=f"Book {book_name} was successfully added to the book shelf! Book ID assigned: {book_id}"
        ).dict()
    )