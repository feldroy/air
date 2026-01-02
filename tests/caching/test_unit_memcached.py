from unittest.mock import patch

import pytest

from tests.caching.conftest import create_memcached_mocks


@pytest.mark.asyncio
async def test_memcached_cache_mocked_get_set() -> None:
    """Test MemcachedCache get/set with mocked client."""
    mock_pylibmc_module, mock_memcached_client = create_memcached_mocks()
    mock_memcached_client.get.return_value = b"cached_value"
    mock_memcached_client.set.return_value = True

    with patch.dict("sys.modules", {"pylibmc": mock_pylibmc_module}):
        from air.caches import MemcachedCache  # noqa: PLC0415

        cache = MemcachedCache(server="127.0.0.1:11211")

        await cache.aset("test_key", b"test_value", ttl=60)
        mock_memcached_client.set.assert_called_once_with(key="test_key", time=60, val=b"test_value")

        result = await cache.aget("test_key")
        mock_memcached_client.get.assert_called_once_with("test_key")
        assert result == b"cached_value"


@pytest.mark.asyncio
async def test_memcached_cache_initialization_fallback() -> None:
    """Test MemcachedCache falls back gracefully when connection fails."""
    mock_pylibmc_module, _ = create_memcached_mocks()
    mock_pylibmc_module.Client.side_effect = Exception("Connection failed")

    with patch.dict("sys.modules", {"pylibmc": mock_pylibmc_module}):
        from air.caches import MemcachedCache  # noqa: PLC0415

        with pytest.raises(ConnectionError):
            MemcachedCache(server="invalid-host:11211")
