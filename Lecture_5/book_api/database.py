"""
Provides utilities for managing a SQLite database using SQLModel,
including creating database tables and handling connections.

This module defines functions to handle database creation based on
SQLModel metadata as well as cleanly disposing of database connections.
"""

from sqlmodel import SQLModel, create_engine

sqlite_file_name = "books.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    """
    Creates the database and associated tables using the SQLModel
    metadata.

    This function ensures that all the tables defined in the model are
    created in the database. It uses SQLModel's metadata and the
    specified engine to perform this operation. If the tables already
    exist, this function does nothing.

    Returns:
        None
    """
    SQLModel.metadata.create_all(engine)


def close_db_connections() -> None:
    """
    Closes all active database connections.

    Disposes the current database engine to ensure that all active connections
    are properly and gracefully closed.

    Returns: None
    """
    engine.dispose()
