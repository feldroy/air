import asyncio
import threading

import pytest

from air.caches import InMemoryCache


@pytest.mark.asyncio
async def test_inmemory_cache_get_set() -> None:
    """Test basic get/set operations for InMemoryCache."""
    cache = InMemoryCache()

    await cache.aset("test_key", b"test_value", ttl=60)

    result = await cache.aget("test_key")
    assert result == b"test_value"


@pytest.mark.asyncio
async def test_inmemory_cache_get_nonexistent() -> None:
    """Test getting a non-existent key returns None."""
    cache = InMemoryCache()
    result = await cache.aget("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_inmemory_cache_ttl_expiration() -> None:
    """Test that cached values expire after TTL."""
    cache = InMemoryCache()

    await cache.aset("test_key", b"test_value", ttl=1)
    assert await cache.aget("test_key") == b"test_value"

    await asyncio.sleep(2)

    assert await cache.aget("test_key") is None


@pytest.mark.asyncio
async def test_inmemory_cache_lru_eviction() -> None:
    """Test LRU eviction when max_size is reached."""
    cache = InMemoryCache(max_size=3)

    await cache.aset("key1", b"value1", ttl=60)
    await cache.aset("key2", b"value2", ttl=60)
    await cache.aset("key3", b"value3", ttl=60)

    assert await cache.aget("key1") == b"value1"
    assert await cache.aget("key2") == b"value2"
    assert await cache.aget("key3") == b"value3"

    await cache.aset("key4", b"value4", ttl=60)

    assert await cache.aget("key1") is None
    assert await cache.aget("key2") == b"value2"
    assert await cache.aget("key2") == b"value2"
    assert await cache.aget("key3") == b"value3"
    assert await cache.aget("key4") == b"value4"


@pytest.mark.asyncio
async def test_inmemory_cache_concurrent_access() -> None:
    """Test concurrent access to InMemoryCache."""
    cache = InMemoryCache()
    errors = []

    async def worker(worker_id: int) -> None:
        try:
            for i in range(10):
                key = f"worker_{worker_id}_key_{i}"
                value = f"worker_{worker_id}_value_{i}".encode()
                await cache.aset(key, value, ttl=60)
                result = await cache.aget(key)
                assert result == value
        except Exception as e:  # noqa: BLE001
            errors.append(e)

    threads = []
    for i in range(5):
        thread = threading.Thread(target=lambda worker_id=i: __import__("asyncio").run(worker(worker_id)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert len(errors) == 0
