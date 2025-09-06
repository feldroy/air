from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine,  async_sessionmaker  # type: ignore [import-error]
from sqlmodel.ext.asyncio.session import AsyncSession  # type: ignore [import-error]

# async_engine = create_async_engine(
#     "postgresql+asyncpg://username@localhost/my-database",  # Async connection string
#     echo=True,  # Optional: Set to False in production
#     future=True,
# )

async def create_async_session(
        url, # Database URL
        echo=False # Optional: Set to False in production
    ):
    """
    
    Example:

        # With SQLite in memory
        async_session = create_async_session(':memory:')
        async with async_session() as session:
            session.add()
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



async def _get_async_session(url, echo) -> AsyncGenerator[AsyncSession, None]:
    async with create_async_session(url, echo) as session:
        yield session

# TODO pass arguments - this won't work
get_async_session = Depends(_get_async_session)
