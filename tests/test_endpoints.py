# tests/test_endpoints.py

from pathlib import Path
from typing import Dict, AnyStr

import pytest
import requests

from dotenv import dotenv_values

"""
Run tests using the following command in terminal:
python -m pytest -rA -v --tb=line test_endpoints.py --cov-report term-missing --cov=sources
"""

# extract environmental variables from .env file
cwd = Path.cwd()
dotenv_abs_loc = Path(cwd, r".env").resolve().__str__()
config = dotenv_values(dotenv_abs_loc)


@pytest.mark.endpoints_user
class TestEndpointsUser:

    @classmethod
    def setup_class(cls):
        pass

    def test_create_user(self):
        user_data = {
            "username": f"{config['TEST_USERNAME']}",
            "password": f"{config['TEST_PASSWORD']}",
            "disabled": False,
            "full_name": "Test User",
            "email": "testuser@example.com"
        }
        headers = {"content-type": "application/json"}
        r = requests.post(
            url=f"{config['LOCALHOST']}/user/signup",
            json=user_data,
            headers=headers
        )
        assert r.status_code == 200
        assert r.ok == True
        assert r.json().get("access_token")

    
    def test_login_for_access_token(self):
        # todo add test cases
        pass


    @classmethod
    def teardown_class(cls):
        pass


@pytest.mark.endpoints_books
class TestEndpointsBooks:
     
    @classmethod
    def setup_class(cls):
        pass

    def test_add_book(self, _login_for_access_token: Dict[AnyStr, AnyStr]):
        jwt = _login_for_access_token.get("access_token")

        new_book_data = {
            "book_name": "Test Book",
            "author": "Test Author",
            "description": "Test Book is used to check the functionality of adding book endpoint"
        }
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }
        r = requests.post(
            url=f"{config['LOCALHOST']}/books/add_book", 
            headers=headers, 
            json=new_book_data, 
            verify=False
        )
        assert r.ok == True
        assert r.status_code == 201

    @classmethod
    def teardown_class(cls):
        pass
