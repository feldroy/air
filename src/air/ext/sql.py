"""
This module includes utility functions for using SQL with AIR.

Introduces two environment variables

- DEBUG
- DATABASE_URL

Requires additional dependencies:

- SQLModel
- greenlet

Persistent database connections require a lifespan object, otherwise you will receive timeout warnings.


```python
from contextlib import asynccontextmanager
import air


@asynccontextmanager
async def lifespan(app: air.Air):
    async_engine = air.db.sql.create_async_engine()
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    yield
    await async_engine.dispose()


app = air.Air(lifespan=lifespan)
```

---

"""

from collections.abc import AsyncGenerator
from enum import IntEnum
from os import getenv

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine as _create_async_engine,
)
from sqlmodel import create_engine as _create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DEBUG = getenv("DEBUG", "false").lower() in ("1", "true", "yes")
"""Environment variable for setting DEBUG loglevel."""
DATABASE_URL = getenv("DATABASE_URL", "")
"""Standard database url environment variable."""
ASYNC_DATABASE_URL = DATABASE_URL.split("?")[0]
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql:", "postgresql+asyncpg:")
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sqlite:", "sqlite+aiosqlite:")


class EchoEnum(IntEnum):
    FALSE = 0
    TRUE = 1


class FutureEnum(IntEnum):
    FALSE = 0
    TRUE = 1


class PoolPrePingEnum(IntEnum):
    FALSE = 0
    TRUE = 1


def create_sync_engine(
    url: str = DATABASE_URL,
    echo: EchoEnum = EchoEnum.TRUE if DEBUG else EchoEnum.FALSE,
):
    """Convenience wrapper for SQLModel/SQLAlchemy's create_engine function. Useful for database scripts or synchronous views.

    Args:
        url: Database URL connection string, defaults to DATABASE_URL environment variable
        echo: Enables logging of all SQL statements executed by the engine, which can be useful for debugging.

    Example:

        TODO
    """
    return _create_engine(url=url, echo=echo)


def create_async_engine(
    url: str = ASYNC_DATABASE_URL,  # Async connection string
    echo: EchoEnum = EchoEnum.TRUE if DEBUG else EchoEnum.FALSE,
    future: FutureEnum = FutureEnum.TRUE,
    pool_pre_ping: PoolPrePingEnum = PoolPrePingEnum.TRUE,
):
    """Convenience wrapper for SQLModel/SQLAlchemy's create_async_engine function. Usually set within an Air app's lifetime object.

    Args:
        url: Database URL connection string, defaults to DATABASE_URL environment variable
        echo: Enables logging of all SQL statements executed by the engine, which can be useful for debugging.
        future: In SQLAlchemy, the future=True argument for create_async_engine enables 2.0-style behaviors and API conventions while still running under SQLAlchemy 1.4.
        pool_pre_ping: Makes the engine test a connection with a lightweight SELECT 1 before using it, ensuring stale or dropped connections are detected and replaced automatically.

    Example:

        from contextlib import asynccontextmanager
        import air

        @asynccontextmanager
        async def lifespan(app: air.Air):
            async_engine = air.db.sql.create_async_engine()
            async with async_engine.begin() as conn:
                await conn.run_sync(lambda _: None)
            yield
            await async_engine.dispose()

        app = air.Air(lifespan=lifespan)
    """
    return _create_async_engine(url=url, echo=echo, future=future, pool_pre_ping=pool_pre_ping)


async def create_async_session(
    url: str = ASYNC_DATABASE_URL,  # Database URL
    echo: EchoEnum = EchoEnum.TRUE if DEBUG else EchoEnum.FALSE,
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
        future=FutureEnum.TRUE,
    )
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_async_session(
    url: str = ASYNC_DATABASE_URL, echo: EchoEnum = EchoEnum.TRUE if DEBUG else EchoEnum.FALSE
) -> AsyncGenerator[AsyncSession, None]:
    """Used with fastapi.Depends to instantiate db session in a view.

    Example:

        # Assumes environment variable DATABASE_URL has been set
        import air
        from fastapi import Depends

        app = air.Air()

        @app.page
        def index(session = Depends(air.db.sql.get_async_session)):
            return air.H1(session.user['username'])

        @app.page
        def home(session = air.db.sql.async_session_dependency):
            return air.H1(session.user['username'])
    """
    session_factory = await create_async_session(url, echo)
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()


async_session_dependency = Depends(get_async_session)
"Shortcut for `Depends(get_async_session)` that only works if DATABASE_URL env var is set."
