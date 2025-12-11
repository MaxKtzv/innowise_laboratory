"""
Provides a database session generator and dependency injection setup.

The utility helps in managing database transactions securely and
conveniently using sessions. It ensures that database operations are
either committed upon success or rolled back in case of an error.

Functions:
- get_session: A generator function that manages database sessions.
- db_dependency: A FastAPI dependency for injecting managed database
  sessions.
"""

from typing import Annotated, Generator

from database import engine
from fastapi import Depends
from sqlmodel import Session


def get_session() -> Generator[Session, None, None]:
    """
    Creates and manages a database session using the provided engine.

    This function provides a session generator that ensures proper
    handling of database transactions. It yields sessions for accessing
    the database while guaranteeing that they are committed or rolled
    back appropriately in case of errors. Sessions are automatically
    closed after their use.

    :yield:
        Session: A generator yielding session instances for database access.
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise


db_dependency = Annotated[Session, Depends(get_session)]
