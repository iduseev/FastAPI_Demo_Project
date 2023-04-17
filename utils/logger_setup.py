# backend/utils/logger_setup.py

import logging

from sys import stdout
from pathlib import Path
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


PROJECT_FOLDER_PATH = Path(__file__).parents[1]


def logger_setup() -> logging.getLogger():
    """
    Logger configuration (used throughout the modules)
    """

    log_folder = Path(PROJECT_FOLDER_PATH, "logs").resolve()
    print(f"log_folder initialized as per follows: {log_folder}")

    formatter = logging.Formatter(
        "%(asctime)-15s\t%(levelname)s\t%(module)s: %(message)s"
    )
    root = logging.getLogger()

    console_handler = logging.StreamHandler(stdout)
    # console_handler.level = logging.INFO
    console_handler.setFormatter(formatter)

    rotating_handler = TimedRotatingFileHandler(
        filename=log_folder.joinpath(
            f"FastAPI_Demo_Project_{datetime.now().strftime('%Y-%m-%d')}.log"
        ),
        encoding="utf-8",
        when="W6",  # W0 - MONDAY
        interval=1,
        atTime=datetime(2020, 1, 1, 0, 0, 0)
    )
    # rotating_handler.level = logging.DEBUG
    rotating_handler.setFormatter(formatter)

    root.setLevel("DEBUG")
    root.addHandler(console_handler)
    root.addHandler(rotating_handler)
    return root
