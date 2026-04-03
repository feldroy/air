"""Tests for database auto-discovery in Air.

When DATABASE_URL is set and asyncpg is installed, Air auto-creates
an AirDB instance and wires up the lifespan to open/close the pool.
"""

from __future__ import annotations

import builtins
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, patch

from starlette.testclient import TestClient

import air
from air import Air
from air.model import AirDB

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from pathlib import Path

    import pytest


# ---------------------------------------------------------------------------
# Fake asyncpg pool for testing without a real database
# ---------------------------------------------------------------------------


class FakePool:
    """Minimal pool double that satisfies AirDB.connect() and close()."""

    def __init__(self) -> None:
        self.closed = False

    async def close(self) -> None:
        self.closed = True

    async def execute(self, sql: str, *args: Any) -> None:
        pass

    async def fetch(self, sql: str, *args: Any) -> list:
        return []

    async def fetchrow(self, sql: str, *args: Any) -> None:
        return None

    async def fetchval(self, sql: str, *args: Any) -> None:
        return None


# ---------------------------------------------------------------------------
# Auto-discovery: DATABASE_URL + airmodel installed
# ---------------------------------------------------------------------------


def test_db_is_none_without_database_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Without DATABASE_URL, app.db should be None."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    app = Air()

    assert app.db is None


def test_db_is_none_when_asyncpg_not_installed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """With DATABASE_URL but asyncpg not importable, app.db should be None."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    real_import = builtins.__import__

    def mock_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "asyncpg":
            msg = "mocked"
            raise ImportError(msg)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)

    app = Air()

    assert app.db is None


def test_db_created_with_database_url_and_airmodel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """With DATABASE_URL and airmodel installed, app.db should be an AirDB instance."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    app = Air()

    assert isinstance(app.db, AirDB)


def test_db_lifespan_opens_and_closes_pool(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The composed lifespan should open a pool on startup and close it on shutdown."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    fake_pool = FakePool()

    with patch("asyncpg.create_pool", new_callable=AsyncMock, return_value=fake_pool):
        app = Air()

        assert app.db is not None

        @app.get("/")
        def index() -> air.P:
            return air.P("ok")

        with TestClient(app) as client:
            # Pool should be connected during lifespan
            assert app.db.pool is fake_pool
            response = client.get("/")
            assert response.status_code == 200

        # After TestClient exits, pool should be closed and disconnected
        assert fake_pool.closed
        assert app.db.pool is None


def test_db_lifespan_composes_with_user_lifespan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A user-provided lifespan should still run inside the database lifespan."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    fake_pool = FakePool()
    startup_ran = False
    shutdown_ran = False

    @asynccontextmanager
    async def user_lifespan(app: Any) -> AsyncIterator[None]:
        nonlocal startup_ran, shutdown_ran
        startup_ran = True
        yield
        shutdown_ran = True

    with patch("asyncpg.create_pool", new_callable=AsyncMock, return_value=fake_pool):
        app = Air(lifespan=user_lifespan)

        @app.get("/")
        def index() -> air.P:
            return air.P("ok")

        with TestClient(app) as client:
            assert startup_ran
            response = client.get("/")
            assert response.status_code == 200

        assert shutdown_ran
        assert fake_pool.closed


def test_no_database_url_preserves_user_lifespan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Without DATABASE_URL, user lifespan should work unchanged."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    startup_ran = False

    @asynccontextmanager
    async def user_lifespan(app: Any) -> AsyncIterator[None]:
        nonlocal startup_ran
        startup_ran = True
        yield

    app = Air(lifespan=user_lifespan)

    @app.get("/")
    def index() -> air.P:
        return air.P("ok")

    with TestClient(app) as client:
        assert startup_ran
        response = client.get("/")
        assert response.status_code == 200

    assert app.db is None
