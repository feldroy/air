from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker  # type: ignore [import-error]
from sqlmodel.ext.asyncio.session import AsyncSession  # type: ignore [import-error]

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
