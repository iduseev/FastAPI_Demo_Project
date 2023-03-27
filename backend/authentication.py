# backend/authentication.py

from typing import Annotated, Dict, AnyStr

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .models import User, UserInDB
from .mock_data import default_users_db


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


def get_user(db: Dict[AnyStr, User], username: AnyStr):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: Annotated[AnyStr, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current user {current_user.username} is inactive!"
        )
