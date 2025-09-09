from collections.abc import AsyncGenerator
from os import getenv

from fastapi import Depends
from sqlalchemy.ext.asyncio import (  # type: ignore [import-error]
    async_sessionmaker,
    create_async_engine as _create_async_engine,
)
from sqlmodel import create_engine as _create_engine
from sqlmodel.ext.asyncio.session import AsyncSession  # type: ignore [import-error]

DEBUG = getenv("DEBUG", "false").lower() in ("1", "true", "yes")
DATABASE_URL = getenv("DATABASE_URL", "")
base_async_url = DATABASE_URL.split("?")[0]
ASYNC_DATABASE_URL = base_async_url.replace("postgresql", "postgresql+asyncpg")
ASYNC_DATABASE_URL = base_async_url.replace("sqlite:", "sqlite+aiosqlite:")


def create_sync_engine(
    url: str = DATABASE_URL,  # connection string
    echo: bool = True,
):
    # TODO doc
    return _create_engine(url=url, echo=echo)


def create_async_engine(
    url: str = ASYNC_DATABASE_URL,  # Async connection string
    echo: bool = DEBUG,
    future=True,
    pool_pre_ping=True
):
    # TODO doc
    return _create_async_engine(url=url, echo=echo, future=future, pool_pre_ping=pool_pre_ping)


async def create_async_session(
    url: str = ASYNC_DATABASE_URL,  # Database URL
    echo: bool = DEBUG,
):
    """
    Create an async SQLAlchemy session factory.

    Example:

        # With SQLite in memory
        async_session = create_async_session(':memory:')
        async with async_session() as session:
            session.add(database_object)
            await session.commit()
    """
    async_engine = create_async_engine(
        url,  # Async connection string
        echo=echo,
        future=True,
    )
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_async_session(url: str = ASYNC_DATABASE_URL, echo: bool = DEBUG) -> AsyncGenerator[AsyncSession, None]:
    """Used with fastapi.Depends to instantiate db session in a view.

    Example:

        # Assumes environment variable DATABASE_URL has been set
        import air
        from fastapi import Depends
        # Session function
        from .models import get_async_dbsession 
        from .models import async_dbsession_dependency # Wrapped shortcut

        app = air.Air()

        @app.page
        def index(session = Depends(get_async_dbsession)):
            return air.H1(session.user['user'name'])

        @app.page
        def home(session = async_dbsession_dependency):
            return air.H1(session.user['user'name'])
    """
    async with create_async_session(url, echo) as session:
        yield session


# Shortcut that only works if DATABASE_URL env var is set
async_session_dependency = Depends(get_async_session)
