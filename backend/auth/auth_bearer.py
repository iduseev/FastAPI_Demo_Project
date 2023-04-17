# backend/auth/auth_bearer.py

from datetime import datetime
from typing import Union, NoReturn

from jose import JWTError
from pydantic import ValidationError
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.security import decode_jwt_token


class JWTBearer(HTTPBearer):
    """
    Subclass of FastAPI's HTTPBearer class used to persist authentication on
    endpoints.
    Represents the protected endpoint verification:
    checks whether the request is authorized or not by scanning the request
    for the JWT
    in the 'Authorization' header.
    Solution taken from https://testdriven.io/blog/fastapi-jwt-auth/

    :param HTTPBearer: FastAPI object used to hold user credentials throughout
                        the session
    """

    def __init__(self, auto_error: bool = True):
        """
        Enables automatic error reporting via auto_error establishing
        :param bool auto_error: enables automatic error reporting, defaults to True
        """
        super().__init__(auto_error=auto_error)

    def __str__(self):
        return """
            Subclass of FastAPI's HTTPBearer class used to persist authentication on endpoints.
            Represents the protected endpoint verification:
            checks whether the request is authorized or not by scanning the request for the JWT
            in the 'Authorization' header.
            Solution taken from https://testdriven.io/blog/fastapi-jwt-auth/
        """

    def __repr__(self):
        return f"{self.__class__.__name__}({self.auto_error if self.auto_error else ''})"

    async def __call__(self, request: Request) -> Union[str, NoReturn]:
        """
        Checks if the credentials passed in during the course of invoking the class are valid.
        1. If the credentials scheme is not a bearer scheme, raises HTTPException if invalid token scheme
        2. If a bearer token was passed, verifies that the JWT is valid
        3. If no credentials were received, raises an invalid authorization error
        :param Request request: incoming Request object from Client
        :raises HTTPException: in case of no credentials, invalid credentials scheme or expired/invalid JWT
        :return Union[str, NoReturn]: user credentials
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code!"
            )
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme!"
            )
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token!"
            )
        return credentials.credentials

    @staticmethod
    def verify_jwt(encoded_token: str) -> bool:
        """
        Verifies if a token is valid. Takes an encoded token, decodes it, checks if payload exists,
        also checks if JWT token has not expired yet
        :param str encoded_token: encoded JWT token
        :raises HTTPException: in case of expired JWT token lifetime
        :return bool: True if JWT token is valid else False
        """
        is_token_valid: bool = False
        try:
            payload = decode_jwt_token(encoded_token)
        except (JWTError, ValidationError) as e:
            print(f"Exception occurred: {e}")
            payload = None
        if payload:
            # raise HTTPException if JWT token is already expired
            if payload.get("exp") <= int(datetime.now().timestamp()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="JWT token expired!"
                )
            print("All good, JWT token verified successfully!")
            is_token_valid = True
        return is_token_valid
