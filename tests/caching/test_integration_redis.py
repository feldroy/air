from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

import air


@pytest.mark.asyncio
async def test_redis_cache_mocked_integration() -> None:
    """Test RedisCache integration with Air using mocked client."""
    mock_redis_module = Mock()
    mock_aioredis_module = Mock()

    mock_sync_client = Mock()
    mock_async_client = AsyncMock()
    stored_data = {}

    mock_sync_client.ping.return_value = True

    async def mock_get(key: str) -> bytes | None:
        return stored_data.get(key)

    async def mock_setex(key: str, time: int, value: bytes) -> bool:
        _ = time
        stored_data[key] = value
        return True

    mock_async_client.get.side_effect = mock_get
    mock_async_client.setex.side_effect = mock_setex
    mock_redis_module.from_url.return_value = mock_sync_client
    mock_redis_module.asyncio = mock_aioredis_module
    mock_aioredis_module.from_url.return_value = mock_async_client

    with patch.dict("sys.modules", {"redis": mock_redis_module, "redis.asyncio": mock_aioredis_module}):
        from air.caches import RedisCache  # noqa: PLC0415

        cache = RedisCache(url="redis://localhost:6379")

        app = air.Air(cache=cache)
        call_count = 0

        @app.page(cache_ttl=60)
        def redis_test_page() -> air.H1:
            nonlocal call_count
            call_count += 1
            return air.H1(f"Redis test: {call_count}")

        client = TestClient(app)

        response1 = client.get("/redis-test-page")
        assert response1.status_code == 200
        assert call_count == 1

        response2 = client.get("/redis-test-page")
        assert response2.status_code == 200
        assert call_count == 1
