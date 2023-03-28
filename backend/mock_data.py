# backend/mock_data.py

from .models import Book

default_book = {
    "book_name": "Shantaram",
    "author": "Gregory David Roberts",
    "description": "Shantaram is a journey through the life of a convict on the lamb, a slum dweller, a prisoner in a crowded Indian jail"
}

default_book_shelf = {
    "936d4b41ec874007af150bbac8e714c3": Book(
        book_name="Shantaram",
        author="Gregory David Roberts",
        description="Shantaram is a journey through the life of a convict on the lamb, a slum dweller, a prisoner in a crowded Indian jail",
        book_id="936d4b41ec874007af150bbac8e714c3",
        available=True
    ),
    "f9b028134ef74bc3a70e1b5e68d69a72": Book(
        book_name="Harry Potter and the Chamber of Secrets",
        author="Joan K. Rowling",
        description="The second book about Harry Potter adventures",
        book_id="f9b028134ef74bc3a70e1b5e68d69a72",
        available=True
    ),
    "414a1cf5764840c588afab3d17fb97df": Book(
        book_name="The adventures of Sherlock Holmes",
        author="Sir Arthur Conan Doyle",
        description="The Adventures of Sherlock Holmes is a collection of twelve short stories",
        book_id="414a1cf5764840c588afab3d17fb97df",
        available=True
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
    }
}
