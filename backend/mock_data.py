# backend/mock_data.py

from .models import Visitor, Book

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

default_visiotrs = {
    "dg43dp87": Visitor(
    visitor_name="John",
    visitor_surname="Doe",
    visitor_id="dg43dp87",
    age="30"
    )
}
