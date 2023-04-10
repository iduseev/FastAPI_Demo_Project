# backend/authentication.py

from typing import Annotated, AnyStr, Union, NoReturn, Optional, Any

from jose import JWTError
from dotenv import dotenv_values
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .database import MongoAdapter
from .models import User, UserInDB, TokenData
from .security import verify_password, decode_jwt_token


# initialize OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="JWT")

# extract environmental variables from .env file
config = dotenv_values(".env")


def fake_decode_token_old(mongo_adapter: MongoAdapter, token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> UserInDB:
    """
    CURRENTLY DEPRECATED FUNCTION AND IS NOT IN USE
    Completely insecure by now but used to understand concepts

    :param db: database with users collection
    :type db: MongoAdapter class instance
    :param token: incoming token
    :type token: Annotated[AnyStr, Depends(oauth2_scheme)]
    :param logger: logger instance, defaults to None
    :type logger: Optional[Any]
    :return: user pydantic model from the database 
    :rtype: UserInDB
    """
    user = get_user(mongo_adapter=mongo_adapter, username=token)
    return user


def authenticate_user(mongo_adapter: MongoAdapter, username: AnyStr, password: AnyStr, logger: Optional[Any] = None) -> Union[UserInDB, bool]:
    """
    Authenticates and returns a user from a database

    :param db: database to be used to manage registered users
    :type db: MongoAdapter class instance
    :param username: username
    :type username: AnyStr
    :param password: user's plain password
    :type password: AnyStr
    :param logger: logger instance, defaults to None
    :type logger: Optional[Any]
    :return: either UserInDB pydantic model or False if user not found in DB or failed to verify password
    :rtype: Union[UserInDB, bool]
    """
    user = get_user(mongo_adapter=mongo_adapter, username=username)
    if not user:
        if logger: logger.debug(f"No user found, unable to authenticate!")
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        if logger: logger.debug("Password verification failed, unable to authenticate!")
        return False
    if logger: logger.debug(f"User {username} authenticated successfully!")
    return user


def get_user(mongo_adapter: MongoAdapter, username: AnyStr, logger: Optional[Any] = None) -> Union[UserInDB, None]:
    """
    Returns a user if it is found within the database

    :param db: database with users collection
    :type db: MongoAdapter class instance
    :param username: username
    :type username: AnyStr
    :param logger: logger instance, defaults to None
    :type logger: Optional[Any]
    :return: either UserInDB pydantic model with user or None if user was not found
    :rtype: Union[UserInDB, None]
    """
    user_dict = mongo_adapter.read_first_match(data={"username": username})
    if user_dict:
        if logger: logger.debug(f"user dict is as per follows: {user_dict}")
        return UserInDB(**user_dict)
    if logger: logger.debug(f"No user found in the database!")
    return


async def get_current_user(mongo_adapter: MongoAdapter, token: Annotated[AnyStr, Depends(oauth2_scheme)], logger: Optional[Any] = None) -> Union[UserInDB, NoReturn]:
    """
    Receives token, attempts to decode the received token, verifies it and returns the current user.
    If the token is invalid, returns an HTTP error right away.

    :param db: database with users collection
    :type db: MongoAdapter class instance
    :param token: incoming JWT token
    :type token: Annotated[AnyStr, Depends(oauth2_scheme)]
    :param logger: logger instance, defaults to None
    :type logger: Optional[Any]
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
        payload = decode_jwt_token(encoded_token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        if logger: logger.warning(f"Exception with JWT token: {e}")
        raise credentials_exception
    user = get_user(mongo_adapter=mongo_adapter, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)], logger: Optional[Any] = None) -> Union[UserInDB, NoReturn]:
    """
    Checks the current user's 'disabled' attribute value and returns user pydantic model if current user is not disabled

    :param current_user: either passed User model or dependency
    :type current_user: Annotated[User, Depends(get_current_user)]
    :param logger: logger instance, defaults to None
    :type logger: Optional[Any]
    :raises HTTPException: raised when current user 'disabled' attribute value is True 
    :return: either current user model if user is not disabled 
    :rtype: Union[UserInDB, NoReturn]
    """
    if current_user.disabled:
        if logger: logger.warning(f"Current user is disabled: {current_user.disabled}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current user {current_user.username} is inactive!"
        )
    return current_user
