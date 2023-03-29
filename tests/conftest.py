# tests/conftest.py

from typing import Dict, AnyStr

import pytest
import requests


LOCALHOST = "http://127.0.0.1:8000"
USERNAME = "johndoe"  # todo move credentials to .env file
PASSWORD = "secret"  # todo move credentials to .env file


@pytest.mark.endpoints_user
@pytest.fixture(scope="session", autouse=True)
def _login_for_access_token() -> Dict[AnyStr, AnyStr]:
    r = requests.post(
        url=f"{LOCALHOST}/token",
        auth=(USERNAME, PASSWORD)
        )
    return r.json()
