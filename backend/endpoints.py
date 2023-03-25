# backend/endpoints.py

from uuid import uuid4
from typing import Union, List, Optional, Dict, Annotated, NoReturn

from fastapi import FastAPI, Path, Body, Query, HTTPException, status, Request, Depends
# from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from .mock_data import default_book_shelf, default_book
from .models import IncomingBookData, Book, Message, Error, User
from .authentication import oauth2_scheme, get_current_user


app = FastAPI()


@app.get("/")
async def read_root() -> Dict:
    return {
        "message": "Hello, welcome to the Demo Library API service built using amazing FastAPI framework!",
    }


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error}
    },
)
def read_book(
    request: Request, 
    token: Annotated[str, Depends(oauth2_scheme)],
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
    token: Annotated[str, Depends(oauth2_scheme)],
    incoming_book: IncomingBookData = Body(..., title="Required book data to be added", example=default_book)
    ) -> Union[NoReturn, Message]:
    client_host = request.client.host
    print(f"Detected incoming GET request from the client with IP {client_host} ...")

    # todo add authorization via JWT token

    incoming_book_data = incoming_book.dict()

    book_name = incoming_book_data.get("book_name")
    author = incoming_book_data.get("author")
    description = incoming_book_data.get("description")

    if book_name in [book.book_name for book in default_book_shelf.values()]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The aforementioned book already exists in the book shelf!"
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
    return Message(
        message=f"Book {book_name} was successfully added to the book shelf! Book ID assigned: {book_id}"
    )


@app.delete(
    "/books/delete/{book_name}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}
    }
)
def delete_book(
    request: Request, 
    token: Annotated[str, Depends(oauth2_scheme)],
    book_name: str = Path(..., title="Required book name to be deleted", example="Shantaram")
) -> Union[NoReturn, Message]:
        client_host = request.client.host
        print(f"Detected incoming GET request from the client with IP {client_host} ...")

        # todo add authorization via JWT token            

        for book_id, book in default_book_shelf.items():
            if book_name == book.book_name:
                print(f"Book {book_name} with assigned book ID {book_id} is found on the book shelf and is to be deleted ...")
                del default_book_shelf[book_id]
                return Message(message=f"Book {book_name} was successfully deleted from the book shelf!")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The book with ID {book_id} was not found in the book shelf!"
            )
