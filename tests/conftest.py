# tests/conftest.py

from typing import Dict, AnyStr
from pathlib import Path

import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient

from backend.endpoints import app
from backend.models import UserInDB
from backend.database import MongoAdapter


# extract environmental variables from .env file
cwd = Path.cwd()
dotenv_abs_loc = str(Path(cwd, ".env").resolve())
config = dotenv_values(dotenv_abs_loc)
client = TestClient(app)


@pytest.mark.endpoints_user
@pytest.fixture(scope="session", autouse=True)
def _login_for_access_token() -> Dict[AnyStr, AnyStr]:
    """
    Fixture for getting JWT token for existing user
    for test purposes

    :return: JSON response with JWT token
    :rtype: Dict[AnyStr, AnyStr]
    """
    response = client.post(
        url=f"{config['LOCALHOST']}/token",
        auth=(config["USERNAME"], config["PASSWORD"])
        )
    return response.json()


@pytest.mark.mongodb
@pytest.fixture(scope="session", autouse=True)
def create_test_user_model() -> UserInDB:
    """
    Creates UserInDB pydantic model of the default
    test user based on user parameters from .env file

    :return UserInDB: test user pydantic model
    """
    # create UserInDB user model because it should not contain plain password in attribute
    new_user_in_db = UserInDB(
        username=config["TEST_USERNAME"],
        hashed_password=config["TEST_HASHED_PASSWORD"],
        disabled=config["TEST_DISABLED"],
    )
    return new_user_in_db


@pytest.mark.mongodb
@pytest.fixture(scope="session", autouse=True)
def _mongo_adapter_book_shelf_collection() -> MongoAdapter:
    """
    Fixture creates instance of MongoAdapter class to work with
    book shelf collection

    :return database.MongoAdapter: instance of MongoAdapter class
    """
    mongo_adapter = MongoAdapter(
        host=config["TEST_MONGODB_HOST"],
        port=int(config["TEST_MONGODB_PORT"]),
        db_name=config["TEST_MONGODB_DB_NAME"],
        collection_name=config["TEST_MONGODB_BOOK_SHELF_COLLECTION_NAME"],
        recreate_indexes=True
    )
    return mongo_adapter


@pytest.mark.mongodb
@pytest.fixture(scope="session", autouse=True)
def _mongo_adapter_users_collection() -> MongoAdapter:
    """
    Fixture creates instance of MongoAdapter class to work with
    users collection

    :return database.MongoAdapter: instance of MongoAdapter class
    """
    mongo_adapter = MongoAdapter(
        host=config["TEST_MONGODB_HOST"],
        port=int(config["TEST_MONGODB_PORT"]),
        db_name=config["TEST_MONGODB_DB_NAME"],
        collection_name=config["TEST_MONGODB_USER_COLLECTION_NAME"],
        recreate_indexes=True
    )
    return mongo_adapter
