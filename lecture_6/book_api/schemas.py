"""
A module for managing Book entities with data validation and pagination.

This module provides data models for creating, reading, updating, and
paginating book records. It includes validation rules for the fields and
enforces constraints using `Pydantic` and `SQLModel`. The functionality
ensures data integrity and type safety for managing book-related data.
"""

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    """
    Basic book schema.

    Attributes:
        title (str): The title of the book. Must have a minimum length
                    of 1 character.

        author (str): The author of the book. Must have a minimum length
                    of 1 character.

        year (int | None): The publication year of the book.
                                Optional, must be between 0 and 2030.
    """

    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int | None = Field(
        default=None, ge=0, le=2030, description="Optional."
    )

    # Convert 0 year to None
    @field_validator("year", mode="before")
    @classmethod
    def zero_or_empty_to_none(cls, v) -> int | None:
        if v in ("", None):
            return None
        try:
            iv = int(v)
        except (TypeError, ValueError):
            return v
        return None if iv == 0 else iv

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Book Title",
                    "author": "Book Author",
                    "year": "0000",
                }
            ]
        }
    }


class BookCreate(BookBase):
    """Schema for creating a new book record."""

    pass


class BookUpdate(BookBase):
    """
    Schema for updating an existing book record.

    Attributes:
        title (str | None): Updated title of the book, if provided.
                            Optional.
        author (str | None): Updated name of the author of the book, if provided.
                            Optional.
    """

    title: str | None = Field(default=None)
    author: str | None = Field(default=None)


class BookRead(BookBase):
    """
    Schema for book representation in read operations.

    Attributes:
        id (int): Unique identifier for the book record.
    """

    id: int

    model_config = {"from_attributes": True}


class PaginatedBook(SQLModel):
    """
    Schema for paginated books' collection.

    Attributes:
        books (list[BookRead]): A list of book objects.
        page (int): The current page number in the pagination.
        limit (int): The maximum number of books displayed per page.
        total (int): The total number of books available across all pages.
    """

    books: list[BookRead]
    page: int
    limit: int
    total: int
