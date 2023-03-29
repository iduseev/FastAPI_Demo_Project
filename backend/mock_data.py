# backend/mock_data.py

from .models import Book

default_book = {
    "book_name": "Shantaram",
    "author": "Gregory David Roberts",
    "description": "Shantaram is a journey through the life of a convict on the lamb, a slum dweller, a prisoner in a crowded Indian jail"
}

default_user = {
        "username": "iduseev",
        "password": "weak_password",
        "full_name": "Ilgiz Duseev",
        "email": "iduseev@example.com",
        "disabled": False,
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
        "hashed_password": "$2b$12$zsy2fnsZCwyFsc45bZier.rtGG2tLXLKGFpt/5wP8TVCf9tewDrjK",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$lxG5P5nWY8QTM4ehuwfl3ubEvpCpL09B6vjUT8luINy71PpQu3cgu",
        "disabled": True,
    }
}
