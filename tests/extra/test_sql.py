import pytest
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from air import db


def test_create_sync_engine() -> None:
    engine = db.sql.create_sync_engine()
    assert isinstance(engine, Engine)


def test_create_async_engine() -> None:
    engine = db.sql.create_async_engine()
    assert isinstance(engine, AsyncEngine)


@pytest.mark.asyncio
async def test_create_async_session() -> None:
    session_factory = await db.sql.create_async_session()
    assert isinstance(session_factory, async_sessionmaker)


@pytest.mark.asyncio
async def test_get_async_session() -> None:
    """Test that get_async_session yields an AsyncSession and properly closes it."""
    # Test the async generator the way it's meant to be used with async context manager
    async for session in db.sql.get_async_session():
        # Check that we got an AsyncSession
        assert isinstance(session, AsyncSession)
        assert session.is_active is True
        # Test that we can use the session
        from sqlalchemy import text

        await session.exec(text("SELECT 1"))
        # Let the async for complete naturally to trigger the finally block


@pytest.mark.asyncio
async def test_get_async_session_with_custom_params() -> None:
    """Test get_async_session with custom URL and echo parameters."""
    # Test with custom parameters
    async for session in db.sql.get_async_session(url="sqlite+aiosqlite:///:memory:", echo=db.sql.EchoEnum.FALSE):
        assert isinstance(session, AsyncSession)
        break
