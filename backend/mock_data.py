# backend/mock_data.py

from .models import Book, User, UserInDB

default_book = {
    "book_name": "Shantaram",
    "author": "Gregory David Roberts",
    "description": "Shantaram is a journey through the life of a convict on the lamb, a slum dweller, a prisoner in a crowded Indian jail"
}

default_book_shelf = {
    "cf23df22": Book(
    book_name="Shantaram",
    author="Gregory David Roberts",
    book_id="cf23df22",
    available=True,
    description="Shantaram is a journey through the life of a convict on the lamb, a slum dweller, a prisoner in a crowded Indian jail"
    )
}

default_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "c636e8e238fd7af97e2e500f8c6f0f4c0bedafb0",
        "disabled": True,
    },
    # "johndoe": UserInDB(
    #     username="johndoe",
    #     full_name="John Doe",
    #     email="johndoe@example.com",
    #     hashed_password="e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4",
    #     disabled=False
    # ),
    # "alice": UserInDB(
    #     username="alice",
    #     full_name="Alice Wonderson",
    #     email="alice@example.com",
    #     hashed_password="c636e8e238fd7af97e2e500f8c6f0f4c0bedafb0",
    #     disabled=True
    # )
}
