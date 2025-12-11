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
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int | None = Field(default=None, ge=0, le=2030, description="Optional.")

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
    pass


class BookUpdate(BookBase):
    title: str | None = Field(default=None)
    author: str | None = Field(default=None)


class BookRead(BookBase):
    id: int

    model_config = {"from_attributes": True}


class PaginatedBook(SQLModel):
    books: list[BookRead]
    page: int
    limit: int
    total: int
