# backend/security.py

import os
import binascii

from hashlib import sha1
from datetime import datetime, timedelta, timezone
from typing import AnyStr, Dict, NoReturn, Union, Optional

from jose import jwt
from dotenv import dotenv_values
from passlib.context import CryptContext 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = dotenv_values(".env")


def generate_secret_key() -> bytes:
    """
    Generates a random byte object of 64 symbols length to 
    be used as SECRET_KEY while encrypting/decrypting JWT token

    :return bytes: random byte object of 64 symbols length
    """
    return binascii.hexlify(os.urandom(32))


def hash_password_old(password: AnyStr) -> AnyStr:
    """
    CURRENTLY DEPRECATED FUNCTION AND IS NOT IN USE
    Hashing password using hashlib sha1

    :param password: raw user password passed from authentication form
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


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> Dict[AnyStr, AnyStr]:
    """
    Creates JWT access token based on passed data and applies passed JWT token lifetime 

    :param data: data to be used as claims set
    :type data: Dict
    :param expires_delta: desired JWT token lifetime, defaults to None
    :type expires_delta: Optional[timedelta], optional
    :return: JWT string and related datetime-type strings in ISO format
    :rtype: Dict[AnyStr, AnyStr]
    """
    # copy data and assign it to variable
    to_encode = data.copy()
    # define a datetime object when JWT to be expired
    utcnow = datetime.utcnow()
    if not expires_delta:
        expires_delta = timedelta(minutes=180)
    expires_at = utcnow + expires_delta

    to_encode.update({"exp": expires_at})
    # encode the given contents to get a JWT token
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=config["SECRET_KEY"],
        algorithm=config["ALGORITHM"]
    )
    return {
        "access_token": encoded_jwt,
        "token_type": "Bearer", 
        "expires_at": expires_at.astimezone().isoformat(), 
        "expires_in": expires_delta.seconds, 
        "updated_at": utcnow.replace(tzinfo=timezone.utc).isoformat()
    }


def decode_jwt_token(encoded_token: AnyStr) -> Dict[AnyStr, AnyStr]:
    """
    Decodes given JWT token based on secret key and algorithm from 
    config and returns decoded JTW token payload

    :param encoded_token: encoded JWT token
    :type encoded_token: AnyStr
    :return: decoded JWT token payload
    :rtype: Dict[AnyStr, AnyStr]
    """
    payload = jwt.decode(
        token=encoded_token,
        key=config["SECRET_KEY"],
        algorithms=config["ALGORITHM"]
    )
    return payload


# TODO add function to verify JWT token