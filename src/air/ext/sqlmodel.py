from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import IntEnum as _IntEnum
from os import getenv as _getenv

from fastapi import Depends
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as _async_sessionmaker,
    create_async_engine as _create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.sql.elements import BinaryExpression as _BinaryExpression
from sqlmodel import (
    SQLModel,
    create_engine as _create_engine,
    select,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from ..applications import Air as _AirApp
from ..exceptions import ObjectDoesNotExist

DEBUG = _getenv("DEBUG", "false").lower() in ("1", "true", "yes")
"""Environment variable for setting DEBUG loglevel."""
DATABASE_URL = _getenv("DATABASE_URL", "")
"""Standard database url environment variable."""
ASYNC_DATABASE_URL = DATABASE_URL.split("?")[0]
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql:", "postgresql+asyncpg:")
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sqlite:", "sqlite+aiosqlite:")


class _EchoEnum(_IntEnum):
    FALSE = 0
    TRUE = 1


class _FutureEnum(_IntEnum):
    FALSE = 0
    TRUE = 1


class _PoolPrePingEnum(_IntEnum):
    FALSE = 0
    TRUE = 1


def create_sync_engine(
    url: str = DATABASE_URL,
    echo: _EchoEnum = _EchoEnum.TRUE if DEBUG else _EchoEnum.FALSE,
) -> Engine:
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
    echo: _EchoEnum = _EchoEnum.TRUE if DEBUG else _EchoEnum.FALSE,
    future: _FutureEnum = _FutureEnum.TRUE,
    pool_pre_ping: _PoolPrePingEnum = _PoolPrePingEnum.TRUE,
) -> AsyncEngine:
    """Convenience wrapper for SQLModel/SQLAlchemy's create_async_engine function. Usually set within an Air app's lifetime object.

    Args:
        url: Database URL connection string, defaults to DATABASE_URL environment variable
        echo: Enables logging of all SQL statements executed by the engine, which can be useful for debugging.
        future: In SQLAlchemy, the future=True argument for create_async_engine enables 2.0-style behaviors and API conventions while still running under SQLAlchemy 1.4.
        pool_pre_ping: Makes the engine test a connection with a lightweight SELECT 1 before using it, ensuring stale or dropped connections are detected and replaced automatically.
    """
    return _create_async_engine(url=url, echo=echo, future=future, pool_pre_ping=pool_pre_ping)


@asynccontextmanager
async def async_db_lifespan(app: _AirApp):
    """Application Lifespan object for ensuring that database connections remain active.

    Not including this can result in `sqlalchemy.exc.OperationalError` or `asyncpg.exceptions.ConnectionDoesNotExistError`
    errors when the database connection times out because of inactivity.

    Example:

        import air

        app = air.Air(lifespan=air.ext.sqlmodel.async_db_lifespan)
    """
    async_engine = create_async_engine()
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    yield
    await async_engine.dispose()


async def create_async_session(
    url: str = ASYNC_DATABASE_URL,  # Database URL
    echo: _EchoEnum = _EchoEnum.TRUE if DEBUG else _EchoEnum.FALSE,
    async_engine: AsyncEngine | None = None,
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
    if async_engine is None:
        async_engine = create_async_engine(
            url,  # Async connection string
            echo=echo,
            future=_FutureEnum.TRUE,
        )
    return _async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_async_session(
    url: str = ASYNC_DATABASE_URL, echo: _EchoEnum = _EchoEnum.TRUE if DEBUG else _EchoEnum.FALSE
) -> AsyncGenerator[AsyncSession]:
    """Builder function for `async_session_dependency`."""
    session_factory = await create_async_session(url, echo)
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()


async_session_dependency = Depends(get_async_session)
"""Dependency for accessing sessions in views.

Requires that environment variable DATABASE_URL has been set

Example:

    import air
    from db import Heroes

    app = air.Air()
    AsyncSession = air.ext.sqlmodel.AsyncSession


    @app.page
    async def index(session: AsyncSession = air.ext.sqlmodel.async_session_dependency):
        statement = select(tables.Heroes)
        heroes = await session.exec(statement=statement)
        return air.Ul(
            *[Li(hero) for hero in heroes]
        )
"""


async def get_object_or_404(session: AsyncSession, model: SQLModel, *args: _BinaryExpression):
    """Get a record or raise an exception.

    Args:
        session: An `AsyncSession` object.
        model: A SQLModel subclass, in the example inspired by SQLModel below we use Hero as a table object.
        *args: One or more SQLAlchemy BinaryExpressions. The classic example is `Hero.name=='Spiderman'` which will display as `<sqlalchemy.sql.elements.BinaryExpression object at 0x104ba0410>`..

    Example:

        import air
        from db import Hero

        app = air.Air()

        @app.get('/heroes/{name: str}')
        async def hero(name: str, session = Depends(air.ext.sqlmodel.get_async_session)):
            hero = await get_object_or_404(session, model, Hero.name==name)
            return air.layouts.mvpcss(
                air.H1(hero.name),
                air.P(hero.secret_identity)
            )

    """
    stmt = select(model)
    for arg in args:
        stmt = stmt.where(arg)
    results = await session.exec(stmt)
    if obj := results.one_or_none():
        return obj
    error = ObjectDoesNotExist(status_code=404)
    error.add_note(f"{model=}")
    error.add_note(f"{args=}")
    raise error
