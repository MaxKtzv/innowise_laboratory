"""
A module for managing and paginating a collection of books in a database.

This module contains functions for retrieving books, counting the total
number of books, and paginating the collection.
"""

from fastapi import HTTPException, status
from sqlmodel import func, select

from book_api.models import Book
from book_api.schemas import PaginatedBook
from book_api.services.pagination import clamp_limit, compute_offset


def total_books(database) -> int:
    total = database.exec(select(func.count()).select_from(Book)).one()
    return total


def get_books(database, page, limit):
    offset = compute_offset(page, limit)
    query = select(Book)
    books = database.exec(
        query.order_by(Book.id).offset(offset).limit(limit)
    ).all()
    return books


def paginate_books(database, page, limit) -> PaginatedBook:
    total = total_books(database)
    clamped_limit = clamp_limit(limit, max_limit=25)
    books = get_books(
        database,
        page,
        limit,
    )
    if not books:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return PaginatedBook(
        books=books, page=page, limit=clamped_limit, total=total
    )
