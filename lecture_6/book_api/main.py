from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from book_api.dependencies.database import close_db_connections, create_db_and_tables
from book_api.routers.routers import router

description = """
A FastAPI + SQLModel service for managing books stored in SQLite. 
It exposes CRUD and search endpoints under /books, supports pagination
with metadata  (books, page, limit, total), and uses Pydantic/SQLModel
schemas (BookCreate, BookUpdate, BookRead, PaginatedBook) for validation
and responses. The Book model tracks title, author, and an optionally
year.
"""


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Manages the lifespan of the application, initialize database and
    cleaned up at the start and end of the application's lifecycle.

    This function runs within the context of the FastAPI lifespan and
    uses threadpool execution to perform potentially blocking
    operations asynchronously. As part of the application's lifecycle,
    it initializes the database and its tables upon startup and ensures
    proper closure of database connections upon shutdown.

    Params:
        _: The FastAPI instance managing the application lifecycle.
    Yields:
        None: An asynchronous generator.
    """
    await run_in_threadpool(create_db_and_tables)
    try:
        yield
    finally:
        await run_in_threadpool(close_db_connections)


app = FastAPI(
    lifespan=lifespan, title="Tiny Book API", description=description
)


@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}


app.include_router(router)
