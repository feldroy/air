from __future__ import annotations

import logging
from typing import Any, Protocol, cast

from air.caches.base import CacheInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _SyncRedisClient(Protocol):
    def get(self, key: str) -> bytes | None: ...
    def setex(self, key: str, time: int, value: bytes) -> Any: ...
    def delete(self, key: str) -> Any: ...
    def flushdb(self, *, asynchronous: bool = True) -> Any: ...
    def ping(self) -> Any: ...


class _AsyncRedisClient(Protocol):
    async def get(self, key: str) -> bytes | None: ...
    async def setex(self, key: str, time: int, value: bytes) -> Any: ...
    async def delete(self, key: str) -> Any: ...
    async def flushdb(self, *, asynchronous: bool = True) -> Any: ...
    async def ping(self) -> Any: ...


class RedisCache(CacheInterface):
    """Redis-backed cache implementation."""

    def __init__(
        self,
        url: str = "redis://localhost:6379",
        default_ttl: int = 300,
        **redis_kwargs: dict[str, Any],
    ) -> None:
        self.url = url
        self.default_ttl = default_ttl
        self.redis_kwargs = redis_kwargs
        self._client: _SyncRedisClient
        self._async_client: _AsyncRedisClient

        self._initialize_clients()

    def _initialize_clients(self) -> None:
        """
        Initialize Redis clients with error handling.

        Raises:
            ImportError: If the redis library is not installed.
            ConnectionError: For any other connection-related issues.
        """

        try:
            import redis  # noqa: PLC0415
            import redis.asyncio as aioredis  # noqa: PLC0415

            self._client = cast(_SyncRedisClient, redis.from_url(self.url, **self.redis_kwargs))
            self._async_client = cast(_AsyncRedisClient, aioredis.from_url(self.url, **self.redis_kwargs))

            # Test connection
            self._client.ping()

        except ImportError:
            logger.exception("Redis library not installed. Install with: pip install redis")
            raise
        except Exception as exc:
            logger.exception(f"Failed to connect to Redis at {self.url}")
            raise ConnectionError from exc

    def get(self, key: str) -> bytes | None:
        """
        Retrieve cached value.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        try:
            return self._client.get(key=key)
        except Exception as e:
            logger.exception("Redis get failed for key '%s'", key, exc_info=e)
            return None

    async def aget(self, key: str) -> bytes | None:
        """
        Retrieve cached value.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        try:
            return await self._async_client.get(key=key)
        except Exception as e:
            logger.exception("Redis aget failed for key '%s'", key, exc_info=e)
            return None

    def set(self, key: str, value: bytes, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (bytes): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        try:
            self._client.setex(key=key, time=ttl, value=value)
        except Exception as e:
            logger.exception("Redis set failed for key '%s'", key, exc_info=e)

    async def aset(self, key: str, value: bytes, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (bytes): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        try:
            await self._async_client.setex(key=key, time=ttl, value=value)
        except Exception as e:
            logger.exception("Redis aset failed for key '%s'", key, exc_info=e)

    def delete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        try:
            self._client.delete(key)
        except Exception as e:
            logger.exception("Redis delete failed for key '%s'", key, exc_info=e)

    async def adelete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        try:
            await self._async_client.delete(key)
        except Exception as e:
            logger.exception("Redis adelete failed for key '%s'", key, exc_info=e)

    def clear(self, **_kwargs: Any) -> None:
        """
        Clear all cache entries.

        Args:
            **_kwargs: Ignored for Redis backend.
        """

        try:
            self._client.flushdb(asynchronous=False)
        except Exception as e:
            logger.exception("Redis clear failed", exc_info=e)

    async def aclear(self, **_kwargs: Any) -> None:
        """
        Clear all cache entries asynchronously.

        Args:
            **_kwargs: Ignored for Redis backend.
        """

        try:
            await self._async_client.flushdb(asynchronous=True)
        except Exception as e:
            logger.exception("Redis aclear failed", exc_info=e)
