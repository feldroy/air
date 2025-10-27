from __future__ import annotations

import pytest
from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from air.applications import Air
from air.exceptions import ObjectDoesNotExist
from air.ext import sqlmodel
from air.ext.sqlmodel import create_async_session


def test_create_sync_engine() -> None:
    engine = sqlmodel.create_sync_engine()
    assert isinstance(engine, Engine)


def test_create_async_engine() -> None:
    engine = sqlmodel.create_async_engine()
    assert isinstance(engine, AsyncEngine)


@pytest.mark.asyncio
async def test_create_async_session() -> None:
    session_factory = await sqlmodel.create_async_session()
    assert isinstance(session_factory, async_sessionmaker)


@pytest.mark.asyncio
async def test_get_async_session() -> None:
    """Test that get_async_session yields an AsyncSession and properly closes it."""
    # Test the async generator the way it's meant to be used with async context manager
    async for session in sqlmodel.get_async_session():
        # Check that we got an AsyncSession
        assert isinstance(session, AsyncSession)
        assert session.is_active is True
        # Test that we can use the session

        await session.exec(text("SELECT 1"))
        # Let the async for complete naturally to trigger the finally block


@pytest.mark.asyncio
async def test_get_async_session_with_custom_params() -> None:
    """Test get_async_session with custom URL and echo parameters."""
    # Test with custom parameters
    async for session in sqlmodel.get_async_session(url="sqlite+aiosqlite:///:memory:", echo=sqlmodel._EchoEnum.FALSE):
        assert isinstance(session, AsyncSession)
        break


@pytest.mark.asyncio
async def test_get_object_or_404():
    """Use sqlite in memory to test the quality of the get_object_or_404 function."""

    # Define a simple test model
    class TestUser(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str
        email: str

    # Create in-memory async engine and session
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = await create_async_session("sqlite+aiosqlite:///:memory:", async_engine=async_engine)

    async with async_session_maker() as session:  # pyrefly:ignore[bad-context-manager]
        # Add test data
        user1 = TestUser(id=1, name="John Doe", email="john@example.com")
        user2 = TestUser(id=2, name="Jane Smith", email="jane@example.com")
        session.add(user1)
        session.add(user2)
        await session.commit()

        # Test successful retrieval
        found_user = await sqlmodel.get_object_or_404(session, TestUser, TestUser.id == 1)
        assert found_user.id == 1
        assert found_user.name == "John Doe"
        assert found_user.email == "john@example.com"

        # Test with multiple conditions
        found_user2 = await sqlmodel.get_object_or_404(
            session, TestUser, TestUser.id == 2, TestUser.name == "Jane Smith"
        )
        assert found_user2.id == 2
        assert found_user2.name == "Jane Smith"

        # Test ObjectDoesNotExist exception for non-existent record
        with pytest.raises(ObjectDoesNotExist) as exc_info:
            await sqlmodel.get_object_or_404(session, TestUser, TestUser.id == 999)

        assert exc_info.value.status_code == 404

        # Test ObjectDoesNotExist exception with multiple conditions
        with pytest.raises(ObjectDoesNotExist) as exc_info:
            await sqlmodel.get_object_or_404(session, TestUser, TestUser.id == 1, TestUser.name == "Wrong Name")

        assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_async_db_lifespan():
    """Test the async_db_lifespan context manager."""
    app = Air()

    # Test that the lifespan runs without error
    async with sqlmodel.async_db_lifespan(app):
        # Inside the lifespan context, we should be able to proceed normally
        pass
    # The lifespan should complete successfully
