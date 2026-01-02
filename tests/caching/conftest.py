from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock

if TYPE_CHECKING:
    from air.caches import MemcachedCache, RedisCache

try:
    from air.caches import RedisCache

    REDIS_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    REDIS_AVAILABLE = False
    RedisCache = None  # type: ignore[assignment, misc]

try:
    from air.caches import MemcachedCache

    MEMCACHED_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    MEMCACHED_AVAILABLE = False
    MemcachedCache = None  # type: ignore[assignment, misc]


def create_redis_mocks() -> tuple[Mock, Mock, Mock, AsyncMock]:
    """
    Create mocked Redis modules and clients for testing.

    Returns:
        tuple: (mock_redis_module, mock_aioredis_module, mock_sync_client, mock_async_client)
    """
    mock_redis_module = Mock()
    mock_aioredis_module = Mock()
    mock_sync_client = Mock()
    mock_async_client = AsyncMock()

    mock_sync_client.ping.return_value = True
    mock_redis_module.from_url.return_value = mock_sync_client
    mock_redis_module.asyncio = mock_aioredis_module
    mock_aioredis_module.from_url.return_value = mock_async_client

    return mock_redis_module, mock_aioredis_module, mock_sync_client, mock_async_client


def create_memcached_mocks() -> tuple[Mock, Mock]:
    """Create mocked Memcached module and client for testing.

    Returns:
        tuple: (mock_pylibmc_module, mock_memcached_client)
    """
    mock_pylibmc_module = Mock()
    mock_memcached_client = Mock()
    mock_pylibmc_module.Client.return_value = mock_memcached_client

    return mock_pylibmc_module, mock_memcached_client
