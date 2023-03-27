# backend/authentication.py

from typing import Annotated, Dict, AnyStr

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .models import User, UserInDB
from .mock_data import default_users_db




