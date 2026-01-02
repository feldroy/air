from typing import Any
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import air
from air.caches import InMemoryCache


@pytest.mark.asyncio
async def test_cache_get_failure_graceful_degradation() -> None:
    """Test that cache get failures don't break page rendering."""
    mock_cache = Mock(spec=InMemoryCache)
    mock_cache.aget.side_effect = Exception("Cache connection failed")
    mock_cache.aset.return_value = None

    app = air.Air(cache=mock_cache)
    call_count = 0

    @app.page(cache_ttl=60)
    def failing_cache_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    client = TestClient(app)

    response = client.get("/failing-cache-page")
    assert response.status_code == 200
    assert "Call count: 1" in response.text


@pytest.mark.asyncio
async def test_cache_set_failure_graceful_degradation() -> None:
    """Test that cache set failures don't break page rendering."""
    mock_cache = Mock(spec=InMemoryCache)
    mock_cache.aget.return_value = None
    mock_cache.aset.side_effect = Exception("Cache write failed")

    app = air.Air(cache=mock_cache)

    @app.page(cache_ttl=60)
    def set_failing_page() -> air.H1:
        return air.H1("Content")

    client = TestClient(app)

    response = client.get("/set-failing-page")
    assert response.status_code == 200
    assert "Content" in response.text


def test_pickle_serialization_failure_graceful_degradation() -> None:
    """Test graceful handling of pickle serialization failures."""
    app = air.Air(cache=InMemoryCache())

    class UnpicklableClass:
        """Class that cannot be pickled."""

        def __reduce__(self) -> tuple[Any, ...]:
            msg = "Cannot pickle this object"
            raise TypeError(msg)

    @app.page(cache_ttl=60)
    def unpicklable_page() -> air.H1:
        obj = UnpicklableClass()
        return air.H1(f"Object: {obj}")

    client = TestClient(app)

    response = client.get("/unpicklable-page")
    assert response.status_code == 200
