"""
This module defines the Book model for database representation.

The Book model extends BookBase and adds fields for storing book details
such as ID, title, author, and publication year. It is configured
to act as a database table using SQLModel's features.
"""

from sqlmodel import Field

from book_api.schemas import BookBase


class Book(BookBase, table=True):
    """
    Represents a book entity in database.

    Attributes:
        id (int | None): Unique identifier for the book record.
                        Autoincrement primary key.
        title (str): The title of the book. Required field.
        author (str): The author of the book. Required field.
        year (int | None): The publication year of the book.
                        Optional field, can be null.
    """

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    year: int | None = Field(default=None, nullable=True)
