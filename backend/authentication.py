# backend/authentication.py

from uuid import uuid4
from typing import Annotated, Dict, AnyStr, Union, NoReturn

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .models import User, UserInDB
from .mock_data import default_users_db


# initialize OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> UserInDB:
    print(f"Calling 'fake_decode_token' function ...")      # fixme delete
    print(f"incoming token: {token}\n\n")
    # return User(
    #     username=token + "fakedecoded", 
    #     full_name="John Doe", 
    #     email="johndoe@example.com",
    #     disabled=False
    # )
    # fixme completely insecure by now but used to understand concepts
    user = get_user(db=default_users_db, username=token)
    print(f"Gotten the following user: {user}")      # fixme delete
    return user


def get_user(db: Dict[AnyStr, UserInDB], username: AnyStr) -> Union[UserInDB, None]:
    print(f"Calling 'get_user' function ...")       # fixme delete
    print(f"incoming username: {username}\n\n")
    if username in db:
        print(f"Detected user {username} in DB!")      # fixme delete
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> UserInDB:
    print(f"Calling 'get_current_user' function ...")       # fixme delete
    user = fake_decode_token(token=token)
    print(f"Gotten the following user: {user.username}")      # fixme delete
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"Returning user: {user}\n\n")
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> Union[None, NoReturn]:
    print(f"Calling 'get_current_active_user' function ...")        # fixme delete
    print(f"Incoming current_user: {current_user}")
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current user {current_user.username} is inactive!"
        )
    return current_user