import sys
from typing import AsyncGenerator
from fastapi import Depends, FastAPI

_missing = None
try:
    import sqlmodel
except ImportError:
    _missing = ImportError("The feature you’re trying to use requires 'sqlmodel'.")
    if sys.version_info.minor >= 11:
        _missing.add_note('Install it with: "uv add sqlmodel"')
    else:
        _missing.msg += '\nInstall it with: "uv add sqlmodel"'


def _sql_import_error(*args, **kwargs):
    raise _missing


# Public API
if _missing:
    # put in placeholder objects that raise when used
    create_engine = _sql_import_error
    create_async_engine, async_sessionmaker = _sql_import_error, _sql_import_error
    AsyncSession = _sql_import_error
else:
    from sqlalchemy.engine import create_engine as create_engine
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlmodel.ext.asyncio.session import AsyncSession


async_engine = create_async_engine(
    "postgresql+asyncpg://username@localhost/my-database",  # Async connection string
    echo=True,  # Optional: Set to False in production
    future=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def _get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


get_async_session = Depends(_get_async_session)