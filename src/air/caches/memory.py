import logging
import time
from collections import OrderedDict
from threading import Lock
from typing import Any

from air.caches.base import CacheInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InMemoryCache(CacheInterface):
    """Thread-safe in-memory cache with LRU eviction."""

    def __init__(self, default_ttl: int = 300, max_size: int = 1000) -> None:
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: OrderedDict[str, tuple[bytes, float]] = OrderedDict()
        self._lock = Lock()

    def get(self, key: str) -> bytes | None:
        """
        Retrieve cached value, return None if expired or not found.

        Args:
            key (str): The cache key.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        with self._lock:
            if key not in self._cache:
                return None

            value, expires_at = self._cache[key]

            # Check expiration
            if time.time() > expires_at:
                del self._cache[key]
                return None

            # Move to end (LRU)
            self._cache.move_to_end(key)
            return value

    async def aget(self, key: str) -> bytes | None:
        """
        Retrieve cached value, return None if expired or not found.

        Args:
            key (str): The cache key.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        return self.get(key)

    def set(self, key: str, value: bytes, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (bytes): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        with self._lock:
            # Evict oldest if at capacity
            if len(self._cache) >= self.max_size and key not in self._cache:
                logger.warning(f"In-memory cache full (max_size={self.max_size}). Evicting oldest entry.")
                self._cache.popitem(last=False)

            expires_at = time.time() + ttl
            self._cache[key] = (value, expires_at)
            self._cache.move_to_end(key)

    async def aset(self, key: str, value: bytes, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (bytes): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        self.set(key, value, ttl)

    def delete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        with self._lock:
            self._cache.pop(key, None)

    async def adelete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        self.delete(key)

    def clear(self, **_kwargs: Any) -> None:
        """
        Clear all cache entries.

        Args:
            **_kwargs: Ignored for in-memory backend.
        """

        with self._lock:
            self._cache.clear()

    async def aclear(self, **_kwargs: Any) -> None:
        """
        Clear all cache entries.

        Args:
            **_kwargs: Ignored for in-memory backend.
        """

        self.clear()
