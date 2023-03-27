# backend/security.py

from hashlib import sha1
from typing import AnyStr


def hash_password(password: AnyStr) -> AnyStr:
    """
    Hashing password using hashlib sha1 and rename the function

    :param password: raw user passwordpassed from authentication form
    :type password: AnyStr
    :return: password value hashed via sha1 algorithm
    :rtype: AnyStr
    """
    #
    return sha1(password.encode()).hexdigest()
