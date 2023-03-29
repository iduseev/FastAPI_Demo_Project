# tests/conftest.py

from typing import Dict, AnyStr

import pytest
import requests

from pathlib import Path
from dotenv import dotenv_values


# extract environmental variables from .env file
cwd = Path.cwd()
dotenv_abs_loc = Path(cwd, ".env").resolve().__str__()
config = dotenv_values(dotenv_abs_loc)


@pytest.mark.endpoints_user
@pytest.fixture(scope="session", autouse=True)
def _login_for_access_token() -> Dict[AnyStr, AnyStr]:
    r = requests.post(
        url=f"{config['LOCALHOST']}/token",
        auth=(config["USERNAME"], config["PASSWORD"])
        )
    return r.json()
