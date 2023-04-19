# tests/test_security.py

from pathlib import Path


import pytest
from dotenv import dotenv_values

from backend import security


# extract environmental variables from .env file
cwd = Path.cwd()
DOTENV_ABS_LOC = str(Path(cwd, r".env").resolve())
config = dotenv_values(DOTENV_ABS_LOC)


"""
Test class for security.py module contains test cases to check
security functions functionality
test run terminal command (with activated venv):
python -m pytest -rA -v --tb=line test_security.py --cov-report term-missing --cov=sources
"""


class TestSecurity:
    """
    Test class to check functionality of security module
    """

    @classmethod
    def setup_class(cls):
        """
        Prepare test environment
        """
        raise NotImplementedError

    @pytest.mark.security
    def test_generate_secret_key(self):
        """
        Checks functionality of function generate_secret_key()
        """
        generated_secret_key = security.generate_secret_key()
        assert isinstance(generated_secret_key, bytes)
        assert len(generated_secret_key) == 64

    @pytest.mark.security
    @pytest.mark.parametrize("plain_password, hashed_password, expected", [
        (config["TEST_PASSWORD"], config["TEST_HASHED_PASSWORD"], True),
        ("some_fake_password", "$2b$12$VYfznDH3EdomobpKls4WF.VLW9PyxM05xpDuoIb73YWY3DRuRDQt2", False)
    ])
    def test_verify_password(self, plain_password, hashed_password, expected):
        """
        Checks functionality of function verify_password()

        :param plain_password: plain password value
        :type plain_password: AnyStr
        :param hashed_password: password value hashed using bcrypt algorithm
        :type hashed_password: AnyStr
        :param expected: ``True`` if the password matched the hash,
                        else ``False``
        :type expected: bool
        """
        password_verification_bool = security.verify_password(
            plain_password, 
            hashed_password
        )
        assert password_verification_bool == expected

    @pytest.mark.security
    @pytest.mark.parametrize("plain_password, expected", [
        (config["TEST_PASSWORD"],  True),
    ])
    def test_get_password_hash(self, plain_password, expected):
        """
        Checks functionality of function get_password_hash()

        :param plain_password: plain password value to be hashed
        :type plain_password: AnyStr
        :param expected: ``True`` if the hash computed for given password
                        is the valid hash value, else ``False``
        :type expected: bool
        """
        hashed_password_result = security.get_password_hash(plain_password)
        verification_bool = security.verify_password(
            plain_password,
            hashed_password_result
        )
        assert verification_bool == expected

    @classmethod
    def teardown_class(cls):
        """
        Tidy up test environment
        """
        raise NotImplementedError
