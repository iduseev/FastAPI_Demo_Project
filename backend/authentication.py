# backend/authentication.py

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return User(
        username=token + "fakedecoded", 
        full_name="John Doe", 
        email="johndoe@example.com",
        disabled=False
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token=token)
    return user
