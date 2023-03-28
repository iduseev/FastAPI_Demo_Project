# backend/security.py

from hashlib import sha1
from datetime import datetime, timedelta
from typing import AnyStr, Dict, NoReturn, Union, Optional

from jose import jwt
from passlib.context import CryptContext 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY generated using the following command:
# openssl rand -hex 32
SECRET_KEY = "72f3c1ec8caadebb29e3e77f461bc36f08f1510d70ca92f175432f38a07ef1ea"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1800


def hash_password_old(password: AnyStr) -> AnyStr:
    """
    CURRENTLY DEPRECATED FUNCTION AND IS NOT IN USE
    Hashing password using hashlib sha1

    :param password: raw user passwordpassed from authentication form
    :type password: AnyStr
    :return: password value hashed via sha1 algorithm
    :rtype: AnyStr
    """
    return sha1(password.encode()).hexdigest()


def verify_password(plain_password: AnyStr, hashed_password: AnyStr) -> Union[bool, NoReturn]:
    """
    Verifies that plain password matches the hashed password using pwd_context

    :param plain_password: plain password value
    :type plain_password: AnyStr
    :param hashed_password: password value hashed using bcrypt algorithm
    :type hashed_password: AnyStr
    :return: either ``True`` if the password matched the hash, else ``False`` or raises TypeError | ValueError
    :rtype: Union[bool, NoReturn]
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: AnyStr) -> AnyStr:
    """
    Returns hashed password value using pwd_context and bcrypt algorithm

    :param plain_password: plain password value to be hashed
    :type plain_password: AnyStr
    :return: password value hashed using bcrypt algorithm
    :rtype: AnyStr
    """
    return pwd_context.hash(plain_password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> AnyStr:
    """
    Creates JWT access token based on passed data and applies passed JWT token lifetime 

    :param data: data to be used as claims set
    :type data: Dict
    :param expres_delta: desired JWT token lifetime, defaults to None
    :type expres_delta: Optional[timedelta], optional
    :return: JWT string
    :rtype: AnyStr
    """
    # copy data and assign it to variable
    to_encode = data.copy()
    # define a datetime object when JWT to be expired
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=180)
    to_encode.update({"exp": expire})
    # encode the given contents to get a JWT token
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt
