import pytest
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from air.db import sql


def test_create_sync_engine():
    engine = sql.create_sync_engine()
    assert isinstance(engine, Engine)


def test_create_async_engine():
    engine = sql.create_async_engine()
    assert isinstance(engine, AsyncEngine)


@pytest.mark.asyncio
async def test_create_async_session():
    session_factory = await sql.create_async_session()
    assert isinstance(session_factory, async_sessionmaker)
