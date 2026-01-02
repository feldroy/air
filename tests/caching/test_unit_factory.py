from unittest.mock import patch

from air.caches import CacheFactory, InMemoryCache
from tests.caching.conftest import create_memcached_mocks, create_redis_mocks


def test_cache_factory_creates_memory_cache() -> None:
    """Test CacheFactory creates InMemoryCache."""
    cache = CacheFactory.create(config={"engine": "memory"})
    assert isinstance(cache, InMemoryCache)


def test_cache_factory_creates_redis_cache() -> None:
    """Test CacheFactory creates RedisCache with mocked redis module."""
    mock_redis_module, mock_aioredis_module, _, _ = create_redis_mocks()

    with patch.dict("sys.modules", {"redis": mock_redis_module, "redis.asyncio": mock_aioredis_module}):
        from air.caches import RedisCache  # noqa: PLC0415

        cache = CacheFactory.create(config={"engine": "redis", "url": "redis://localhost:6379"})
        assert isinstance(cache, RedisCache)


def test_cache_factory_creates_memcached_cache() -> None:
    """Test CacheFactory creates MemcachedCache with mocked pylibmc module."""
    mock_pylibmc_module, _ = create_memcached_mocks()

    with patch.dict("sys.modules", {"pylibmc": mock_pylibmc_module}):
        from air.caches import MemcachedCache  # noqa: PLC0415

        cache = CacheFactory.create(config={"engine": "memcached", "server": "127.0.0.1:11211"})
        assert isinstance(cache, MemcachedCache)


def test_cache_factory_fallback_on_invalid_engine() -> None:
    """Test CacheFactory falls back to InMemoryCache on invalid engine."""
    cache = CacheFactory.create(config={"engine": "invalid"})
    assert isinstance(cache, InMemoryCache)


def test_cache_factory_fallback_on_missing_dependencies() -> None:
    """Test CacheFactory falls back when backend dependencies are missing."""
    with patch("air.caches.factory.RedisCache", side_effect=ImportError):
        cache = CacheFactory.create(config={"engine": "redis", "url": "redis://localhost:6379"})
        assert isinstance(cache, InMemoryCache)
