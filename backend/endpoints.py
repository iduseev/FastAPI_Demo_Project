# backend/endpoints.py

from uuid import uuid4
from datetime import timedelta
from typing import Union, List, Dict, Annotated, NoReturn

from fastapi import FastAPI, Path, Body, Query, HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from .mock_data import default_book_shelf, default_book, default_users_db, default_user
from .models import IncomingBookData, Book, Message, Error, User, Token, UserInDB
from .authentication import oauth2_scheme, get_current_active_user, authenticate_user
from .security import create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES


app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> Dict:
    return {
        "message": "Hello, welcome to the Demo Library API service built using amazing FastAPI framework!",
    }


@app.post("/token", response_model=Token, tags=["user"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    """
    Authenticates the user and creates JWT access token for him  

    :param form_data: data from the authentication form
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends
    :raises HTTPException: exception with status_code HTTP_401_UNAUTHORIZED in case the system was not able to authenticate the user 
    :return: JWT access token in dict format with indicated token type 
    :rtype: JSONResponse
    """
    # attempt to authenticate user
    user = authenticate_user(db=default_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # define JWT token expiry time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create JWT access token fot the user
    # key 'sub' with the token subject is added as per JWT specs
    access_token_data = create_access_token(
        data={"sub": user.username},  
        expires_delta=access_token_expires
        )
    return JSONResponse(
        content={
            "access_token": access_token_data.get("encoded_jwt"), 
            "token_type": "Bearer",
            "expires_at": access_token_data.get("expires_at"),
            "expires_in": access_token_data.get("expires_in"),
            "updated_at": access_token_data.get("utc_now"),
            },
        status_code=status.HTTP_200_OK
    )



@app.get("/user/me", tags=["user"])
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> UserInDB:
    """
    Returns info about currently logged user

    :param current_user: either User pydantic model or dependency
    :type current_user: Annotated[User, Depends(get_current_active_user)]
    :return: pydantic model of the currently active user
    :rtype: User
    """
    current_user_data = current_user.dict()
    current_user_db_entry = UserInDB(**current_user_data)
    return current_user_db_entry


@ app.post("/user/signup", tags=["user"])
async def create_user(
    new_user: User = Body(..., title="Required new user information", example=default_user)
    ) -> JSONResponse:
    """
    Creates a new user with passed username and password. Adds new user entry in the DB, preserving only
    hashed password value

    :param new_user: new user data
    :type new_user: User pydantic model
    :return: JWT token with 
    :rtype: JSONResponse
    """
    # get hash for plain password of the new user
    hashed_password = get_password_hash(plain_password=new_user.password)
    # create UserInDB user model because it should not contain plain password in attribute
    new_user_in_db = UserInDB(
        username=new_user.username,
        hashed_password=hashed_password,
        disabled=new_user.disabled,
        full_name=new_user.full_name,
        email=new_user.email
    )
    # add new user to the database
    default_users_db[new_user_in_db.username] = new_user_in_db.dict()
    # define JWT token expiry time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create JWT access token fot the user
    # key 'sub' with the token subject is added as per JWT specs
    access_token_data = create_access_token(
        data={"sub": new_user_in_db.username},  
        expires_delta=access_token_expires
        )
    return JSONResponse(
        content={
            "access_token": access_token_data.get("encoded_jwt"), 
            "token_type": "Bearer",
            "expires_at": access_token_data.get("expires_at"),
            "expires_in": access_token_data.get("expires_in"),
            "updated_at": access_token_data.get("utc_now"),
            },
        status_code=status.HTTP_200_OK
    )


@app.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Error}
    },
    tags=["books"]
)
def read_book(
        request: Request, 
        token: Annotated[str, Depends(oauth2_scheme)],
        book_id: str = Path(..., title="Required book ID", example="936d4b41ec874007af150bbac8e714c3")
    ) -> Book:
    """
    Extract book data from the book shelf by book ID 

    :param request: request object
    :type request: Request
    :param token: JWT access token assigned to the user
    :type token: Annotated[str, Depends(oauth2_scheme)]
    :param book_id: Path parameter, book ID gotten from the route
    :type book_id: str
    :raises HTTPException: exception  with status_code HTTP_404_NOT_FOUND raised in case the given book_id is not found on the book shelf 
    :return: pydantic model of the requested book
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
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}},
    tags=["books"]
    )
def show_books(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)],
        limit: int = Query(default=10, example=10)
    ) -> List[Book]:
    """
    Shows all the books available on the book shelf, allows to limit the number of showed books 

    :param request: request object
    :type request: Request
    :param token: JWT access token assigned to the user
    :type token: Annotated[str, Depends(oauth2_scheme)]
    :param limit: query parameter, used to limit the returning book batch, defaults to 10
    :type limit: int, optional
    :return: list of books currently available on the book shelf, limited by given number (if applicable)
    :rtype: List[Book]
    """
    return list(default_book_shelf.values())[: limit]


@app.post(
    "/books/add_book",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
    responses={
        status.HTTP_409_CONFLICT: {"model": Error},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}
    },
    tags=["books"]
)
def add_book(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    incoming_book: IncomingBookData = Body(..., title="Required book data to be added", example=default_book)
    ) -> Union[Message, NoReturn]:
    """
    Accepts book data and adds a new Book pydantic model object to the book shelf in DB 

    :param request: request object
    :type request: Request
    :param token: JWT access token assigned to the user
    :type token: Annotated[str, Depends(oauth2_scheme)]
    :param incoming_book: body parameter, new book data
    :type incoming_book: IncomingBookData, optional
    :raises HTTPException: exception with status_code HTTP_409_CONFLICT raised in case the given book name already exists on the book shelf 
    :return: message about successful adding a new book to the book shelf
    :rtype: Union[Message, NoReturn]
    """
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
    },
    tags=["books"]
)
def delete_book(
    request: Request, 
    token: Annotated[str, Depends(oauth2_scheme)],
    book_name: str = Path(..., title="Required book name to be deleted", example="Shantaram")
) -> Union[Message, NoReturn]:
    """
    Deletes a book from the book shelf by given book name

    :param request: request object
    :type request: Request
    :param token: JWT access token assigned to the user
    :type token: Annotated[str, Depends(oauth2_scheme)]
    :param book_name: Path parameter, book name gotten from the route
    :type book_name: str, optional
    :raises HTTPException: exception with status_code HTTP_404_NOT_FOUND raised in case the given book name does not exist on the book shelf
    :return: message about successful book deletion from the book shelf
    :rtype: Union[NoReturn, Message]
    """
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
