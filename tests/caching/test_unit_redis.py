from unittest.mock import patch

import pytest

from tests.caching.conftest import create_redis_mocks


@pytest.mark.asyncio
async def test_redis_cache_mocked_get_set() -> None:
    """Test RedisCache get/set with mocked Redis client."""
    mock_redis_module, mock_aioredis_module, _, mock_async_client = create_redis_mocks()

    mock_async_client.get.return_value = b"cached_value"
    mock_async_client.setex.return_value = True

    with patch.dict("sys.modules", {"redis": mock_redis_module, "redis.asyncio": mock_aioredis_module}):
        from air.caches import RedisCache  # noqa: PLC0415

        cache = RedisCache(url="redis://localhost:6379")

        await cache.aset("test_key", b"test_value", ttl=60)
        mock_async_client.setex.assert_called_once_with(key="test_key", time=60, value=b"test_value")

        result = await cache.aget("test_key")
        mock_async_client.get.assert_called_once_with(key="test_key")
        assert result == b"cached_value"


@pytest.mark.asyncio
async def test_redis_cache_initialization_fallback() -> None:
    """Test RedisCache falls back gracefully when Redis connection fails."""
    mock_redis_module, mock_aioredis_module, mock_sync_client, _ = create_redis_mocks()

    mock_sync_client.ping.side_effect = Exception("Connection failed")

    with patch.dict("sys.modules", {"redis": mock_redis_module, "redis.asyncio": mock_aioredis_module}):
        from air.caches import RedisCache  # noqa: PLC0415

        with pytest.raises(ConnectionError):
            RedisCache(url="redis://invalid-host:9999")
