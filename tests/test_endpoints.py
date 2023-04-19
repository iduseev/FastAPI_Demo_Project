# tests/test_endpoints.py

from pathlib import Path
from typing import Dict, AnyStr

import pytest

from dotenv import dotenv_values
from fastapi import status
from fastapi.testclient import TestClient

from backend.endpoints import app


# extract environmental variables from .env file
cwd = Path.cwd()
DOTENV_ABS_LOC = str(Path(cwd, r".env").resolve())
config = dotenv_values(DOTENV_ABS_LOC)


"""
Run tests using the following command in terminal:
python -m pytest -rA -v --tb=line test_endpoints.py --cov-report term-missing --cov=sources
"""


client = TestClient(app)


@pytest.mark.endpoints_user
class TestEndpointsUser:
    """
    Test class to check functionality of endpoints
    which are working with user model
    """

    @classmethod
    def setup_class(cls):
        """
        Prepare test environment
        """
        raise NotImplementedError

    @pytest.mark.endpoints_user
    def test_read_user_me(self):
        """
        Testing functionality of read_user_me() function
        """
        raise NotImplementedError

    @pytest.mark.endpoints_user 
    def test_create_user(self):
        """
        Checks functionality of function create_user()
        """
        headers = {"content-type": "application/json"}
        user_data = {
            "username": f"{config['TEST_USERNAME']}",
            "password": f"{config['TEST_PASSWORD']}",
            "disabled": False,
            "full_name": "Test User",
            "email": "testuser@example.com"
        }
        response = client.post(
            url=f"{config['LOCALHOST']}/user/signup",
            json=user_data,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.ok is True
        assert response.json().get("access_token")

    @pytest.mark.endpoints_user
    def test_login_for_access_token(self):
        """
        Checks functionality of function login_for_access_token()
        """
        # todo add test cases
        raise NotImplementedError

    @classmethod
    def teardown_class(cls):
        """
        Tidy up test environment
        """
        raise NotImplementedError


@pytest.mark.endpoints_books
class TestEndpointsBooks:
    """
    Test class to check functionality of endpoints
    which are working with books data
    """
    @classmethod
    def setup_class(cls):
        """
        Prepare test environment
        """
        raise NotImplementedError

    @pytest.mark.endpoints_root
    def test_read_root(self):
        """
        Test case checks functionality of read_root() function
        """
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "message": "Hello, welcome to the Demo Library API service "
            "built using amazing FastAPI framework!",
        }

    @pytest.mark.endpoints_book
    @pytest.mark.parametrize("book_id, book_name, expected", [
        ("936d4b41ec874007af150bbac8e714c3", "Shantaram", True),
        ("414a1cf5764840c588afab3d17fb97df", "The adventures of Sherlock Holmes", True),
        ("f9b028134ef74bc3a70e1b5e68d69a72", "Test Book Tat Does Not Exist", False),
    ])
    def test_read_book(
        self,
        _login_for_access_token: Dict[AnyStr, AnyStr],
        book_id: AnyStr, 
        book_name: AnyStr,
        expected: bool
    ):
        """
        Test case checks functionality of read_root() function

        :param book_id: book ID gotten from the route
        :type book_id: str
        :param book_name: book name gotten from the route
        :type book_name: str
        :param expected: `True` if extracted book_name matches with expected
                         else `False`
        :type expected: bool
        """
        jwt = _login_for_access_token.get("access_token")
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }
        response = client.get(
            url=f"/books/{book_id}",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert (response.json().get("book_name") == book_name) is expected

    @pytest.mark.endpoints_book
    def test_show_books(self, _login_for_access_token: Dict[AnyStr, AnyStr]):
        """
        Checks functionality of show_books() function
        """
        jwt = _login_for_access_token.get("access_token")

        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }
        response = client.get(
            url="/books",
            headers=headers
        )
        assert response.json()
        assert isinstance(response.json(), list)

    @pytest.mark.endpoints_book
    def test_add_book(self, _login_for_access_token: Dict[AnyStr, AnyStr]):
        """
        Checks the functionality of add_book() function
        """
        jwt = _login_for_access_token.get("access_token")

        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }
        new_book_data = {
            "book_name": "Test Book",
            "author": "Test Author",
            "description": "Test Book is used to check the functionality of "
                           "adding book endpoint"
        }
        response = client.post(
            url=f"{config['LOCALHOST']}/books/add_book", 
            headers=headers, 
            json=new_book_data, 
        )
        assert response.ok is True
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.endpoints_book
    @pytest.mark.parametrize("deletable_book_name, expected", [
        ("Shantaram", True)
    ])
    def test_delete_book(
        self,
        _login_for_access_token: Dict[AnyStr, AnyStr],
        deletable_book_name: AnyStr,
        expected: bool
    ):
        """
        Test case checks functionality of delete_book() function

        :param deletable_book_name: book name to be deleted (gotten from the route)
        :type deletable_book_name: AnyStr
        :param expected: True` if deleted book_name matches with expected
        :type expected: bool
        """
        jwt = _login_for_access_token.get("access_toke")

        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }
        response = client.delete(
            url=f"books/delete/{deletable_book_name}",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert ("successfully" in response.text) is expected

    @classmethod
    def teardown_class(cls):
        """
        Tidy up test environment
        """
        raise NotImplementedError
