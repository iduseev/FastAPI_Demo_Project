# backend/endpoints.py

import traceback

from uuid import uuid4
from typing import Union, List, Optional, Dict, Annotated, NoReturn, AnyStr

from fastapi import FastAPI, Path, Body, Query, HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from .mock_data import default_book_shelf, default_book, default_users_db
from .models import IncomingBookData, Book, Message, Error, User, UserInDB
from .security import hash_password


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> UserInDB:
    # return User(
    #     username=token + "fakedecoded", 
    #     full_name="John Doe", 
    #     email="johndoe@example.com",
    #     disabled=False
    # )
    # fixme completely insecure by now but used to understand concepts
    user = get_user(db=default_users_db, username=token)
    return user


def get_user(db: Dict[AnyStr, UserInDB], username: AnyStr) -> Union[UserInDB, None]:
    if username in db:
        print(f"Detected user {username} in DB!")
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token=token)
    print(f"Gotten the following user: {user.username}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current user {current_user.username} is inactive!"
        )


@app.get("/")
async def read_root() -> Dict:
    return {
        "message": "Hello, welcome to the Demo Library API service built using amazing FastAPI framework!",
    }


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Dict:
    user_dict = default_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect username or password"
        )
    user = UserInDB(**user_dict)
    # check password validity
    hashed_password = hash_password(password=form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    try:
        # fixme catch error 
        # none is not an allowed value (type=type_error.none.not_allowed)
        return current_user
    except Exception as e:
        TB = traceback.format_exc()
        print(f"Following exception occurred: {e}\nTraceback: {TB}")


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

        if book_name not in [book.book_name for book in default_book_shelf.values()]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The book {book_name} was not found in the book shelf!"
            )

        for book_id, book in default_book_shelf.items():
            if book_name == book.book_name:
                print(f"Book {book_name} with assigned book ID {book_id} is found on the book shelf and is to be deleted ...")
                del default_book_shelf[book_id]
                return Message(message=f"Book {book_name} was successfully deleted from the book shelf!")
