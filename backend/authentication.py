# backend/authentication.py

from typing import Annotated, Dict, AnyStr, Union, NoReturn

from jose import jwt, JWTError
from dotenv import dotenv_values
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .security import verify_password
from .mock_data import default_users_db
from .models import User, UserInDB, TokenData


# initialize OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# extract environmental variables from .env file
config = dotenv_values(".env")


def fake_decode_token_old(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> UserInDB:
    """
    CURRENTLY DEPRECATED FUNCTION AND IS NOT IN USE
    Completely insecure by now but used to understand concepts

    :param token: incoming token
    :type token: Annotated[AnyStr, Depends(oauth2_scheme)]
    :return: user pydantic model from the database 
    :rtype: UserInDB
    """
    user = get_user(db=default_users_db, username=token)
    return user


def authenticate_user(db: Dict[AnyStr, Dict], username: AnyStr, password: AnyStr) -> Union[UserInDB, bool]:
    """
    Authenticates and returns a user from a fake database

    :param db: database to be used to manage registered users
    :type db: Dict[AnyStr, Dict]
    :param username: username
    :type username: AnyStr
    :param password: user's plain password
    :type password: AnyStr
    :return: either UserInDB pydantic model or False if user not found in DB or failed to verify password
    :rtype: Union[UserInDB, bool]
    """
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user


def get_user(db: Dict[AnyStr, Dict], username: AnyStr) -> Union[UserInDB, None]:
    """
    Returns a user if it is found within the database

    :param db: database with users
    :type db: Dict[AnyStr, Dict]
    :param username: username
    :type username: AnyStr
    :return: either UserInDB pydantic model with user or None if user was not found
    :rtype: Union[UserInDB, None]
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> Union[UserInDB, NoReturn]:
    """
    Receives token, attempts to decode the received token, verifies it and returns the current user.
    If the token is invalid, returns an HTTP error right away.

    :param token: incoming JWT token
    :type token: Annotated[AnyStr, Depends(oauth2_scheme)]
    :raises credentials_exception: HTTPException contains status_code=HTTP_401_UNAUTHORIZED, related message and headers as per OAuth2 specs
    :return: either current user object or raises HTTPException
    :rtype: Union[UserInDB, NoReturn]
    """
    # create alias for frequently used exception
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(
            token=token,
            key=config["SECRET_KEY"],
            algorithms=[config["ALGORITHM"]]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception
    
    user = get_user(db=default_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> Union[User, NoReturn]:
    """
    Checks the current user's 'disabled' attribute value and returns user pydantic model if current user is not disabled

    :param current_user: either passed User model or dependancy
    :type current_user: Annotated[User, Depends(get_current_user)]
    :raises HTTPException: raised when durrent user 'disabled' attribute value is True 
    :return: either current user model if user is not disabled 
    :rtype: Union[User, NoReturn]
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current user {current_user.username} is inactive!"
        )
    return current_user
