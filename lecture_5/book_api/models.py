"""
This module defines the Book model for database representation.

The Book model extends BookBase and adds fields for storing book details
such as ID, title, author, and publication year. It is configured
to act as a database table using SQLModel's features.
"""

from schemas import BookBase
from sqlmodel import Field


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    year: int | None = Field(default=None, nullable=True)
