from typing import AsyncIterator
import asyncpg
from ..applications import Air
from contextlib import asynccontextmanager
from typing import Callable
from os import getenv

DATABASE_URL = getenv('DATABASE_URL')


def make_lifespan(dsn: str, *, min_size: int = 1, max_size: int = 10) -> Callable:
    @asynccontextmanager
    async def lifespan(app: Air) -> AsyncIterator[None]:
        app.state.pool = await asyncpg.create_pool(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
        )
        try:
            yield
        finally:
            await app.state.pool.close()

    return lifespan



@asynccontextmanager
async def connect(database_url: str | None = DATABASE_URL):
    """Usage:
    
    async with connect() as conn:
        rows = await conn.fetch(stmt, *args)    
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        yield conn
    finally:
        await conn.close() 