"""
This module provides a set of endpoints to manage books, allowing
functionality such as retrieving, searching, creating, updating,
and deleting book records.

The module interacts with a database and utilizes pagination.
It also provides filtering capabilities for searching books by title,
author or publication year.
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
)
from sqlmodel import String, cast, func, select

from book_api.dependencies.db import db_dependency
from book_api.models import Book
from book_api.schemas import BookCreate, BookRead, BookUpdate, PaginatedBook
from book_api.services.books import paginate_books
from book_api.services.pagination import clamp_limit

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedBook,
)
def read_all_books(
    database: db_dependency,
    page: Annotated[int, Query(ge=1, description="Current page number")] = 1,
    limit: Annotated[
        int, Query(ge=1, le=25, description="Items per page")
    ] = 10,
) -> PaginatedBook:
    """
    Fetches a paginated list of all books from the database.

    This function retrieves a specific page of books, constrained by the
    given page and limit parameters. If no books are available for the
    specified page, a 204 No Content HTTP status is raised. Pagination
    is handled internally to ensure items are displayed based on the
    provided page and limit constraints.

    Params:
        database (session): A dependency-provided database session used
                            for accessing book data.
        page (int): Current page number for pagination.
        limit (int): Number of items per page for pagination.
    Return:
        PaginatedBook: A paginated collection of books wrapped in a
                        PaginatedBook response model.
    """
    return paginate_books(database, page, limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRead,
    response_description="New book was created",
)
def create_book(database: db_dependency, book_request: BookCreate) -> Book:
    """
    Creates a new book based on the provided input data and stores it
    in the database.

    Accepts a database dependency and a book request that contains
    necessary details to create a new book entry. The book data is
    saved into the database, and the persisted record is returned.

    Params:
        database (session): A dependency-provided database session used
                            for accessing book data.
        book_request: The book creation request containing the data.
    Returns:
        BookRead (Book): The newly created and persisted book record, as an
        instance of the `Book` model.
    """
    book = Book(**book_request.model_dump())

    database.add(book)
    database.commit()
    database.refresh(book)
    return book


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedBook,
)
def search_book(
    database: db_dependency,
    search_by_title: Annotated[str | None, Query(min_length=1)] = None,
    search_by_author: Annotated[str | None, Query(min_length=1)] = None,
    search_by_year: Annotated[int | None, Query(ge=0, le=2030)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=25)] = 10,
) -> PaginatedBook:
    """
    Searches for books in the database based on given filter criteria
    such as title, author and publication year. Supports paginated
    results with customizable page size and numbering. Returns a paginated
    collection of book entries that match the filters.

    Params:
        database (session): A dependency-provided database session used
                            for accessing book data.
        search_by_title (str): Optional filter to search for books by
                    title. The value must have a minimum length of 1
                        character.
        search_by_author (str): Optional filter to search for books by
                         author. The value must have a minimum length
                         of 1 character.
        search_by_year (int): Optional filter to search for books by
                    publication year. The value must be an integer
                    between 0 and 2030 inclusive.
        page (int): Current page number for pagination.
        limit (int): Number of items per page for pagination.
                inclusive.
    Returns:
        PaginatedBook: A paginated collection of books that match the
                        filter criteria.
    """
    filters: list = []
    if search_by_title:
        book_title = cast(Book.title, String)
        filters.append(book_title.ilike(f"%{search_by_title}%"))
    if search_by_author:
        book_author = cast(Book.author, String)
        filters.append(book_author.ilike(f"%{search_by_author}%"))
    if search_by_year is not None:
        filters.append(Book.year == search_by_year)

    offset = (page - 1) * limit
    query = select(Book)
    if filters:
        query = query.where(*filters)

    total = database.exec(
        select(func.count()).select_from(query.subquery())
    ).one()
    clamped_limit = clamp_limit(limit, max_limit=25)
    books = database.exec(
        query.order_by(Book.id).offset(offset).limit(limit)
    ).all()
    if not filters or not books:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Book not found."
        )

    return PaginatedBook(
        books=books, page=page, limit=clamped_limit, total=total
    )


@router.put(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookRead,
    response_description="The book was updated.",
)
def update_book(
    database: db_dependency,
    book_request: BookUpdate,
    book_id: Annotated[int, Path(ge=1)],
) -> Book:
    """
    Updates an existing book in the database with the provided information. If the book
    does not exist, raises an HTTP 404 exception.

    Params:
        database (session): A dependency-provided database session used
                            for accessing book data.
        book_request: The request object containing book update
                        information. Must conform to the BookUpdate
                        model.
        book_id (int): The ID of the book to be updated. Must be
                            an integer greater than or equal to 1.
    Returns:
        BookRead: The updated book object, adhering to the Book model.
    """
    book_to_update: Book | None = database.get(Book, book_id)
    if not book_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )

    updated_book = book_request.model_dump(exclude_unset=True)
    book_to_update.sqlmodel_update(updated_book)
    database.add(book_to_update)
    database.commit()
    database.refresh(book_to_update)
    return book_to_update


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="The book was deleted.",
)
def delete_book(
    database: db_dependency, book_id: Annotated[int, Path(ge=1)]
) -> None:
    """
    Deletes a book from the database by its ID.

    This function is registered as a DELETE endpoint and allows the
    removal of a book specified by its unique identifier. If the book
    does not exist, a 404 HTTP exception is raised. Upon successful
    deletion, the changes are committed to the database.

    Params:
        database (session): A dependency-provided database session used
                            for accessing book data.
            book_id (int): The ID of the book to be updated. Must be
                            an integer greater than or equal to 1.
    Returns: None
    """
    book_model: Book | None = database.get(Book, book_id)
    if book_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )
    database.delete(book_model)
    database.commit()
