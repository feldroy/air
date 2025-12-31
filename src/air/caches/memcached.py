from __future__ import annotations

import logging
from typing import Any, Protocol, cast

from air.caches.base import CacheInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _SyncMemcachedClient(Protocol):
    def ping(self) -> None: ...

    def get(self, key: str) -> bytes | None: ...

    def set(self, key: str, time: int, val: Any) -> None: ...

    def delete(self, key: str) -> None: ...

    def flush_all(self, delay: int = 0, *, noreply: bool | None = None) -> bool | None: ...


class _AsyncMemcachedClient(Protocol):
    async def get(self, key: str) -> bytes | None: ...

    async def set(self, key: str, time: int, val: Any) -> None: ...

    async def delete(self, key: str) -> None: ...

    async def flush_all(self, delay: int = 0, *, noreply: bool | None = None) -> bool | None: ...


class MemcachedCache(CacheInterface):
    """Memcached-backed cache implementation."""

    def __init__(
        self,
        server: str | None = None,
        default_ttl: int = 300,
        **memcached_kwargs: Any,
    ) -> None:
        self.server = server or "127.0.0.1:11211"
        self.default_ttl = default_ttl
        self.memcached_kwargs = memcached_kwargs
        self._client: _SyncMemcachedClient

        self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Initialize Memcached client with error handling.

        Raises:
            ImportError: If the pylibmc library is not installed.
            ConnectionError: For any other connection-related issues.
        """

        try:
            import pylibmc  # noqa: PLC0415

            username = self.memcached_kwargs.get("username", None)
            password = self.memcached_kwargs.get("password", None)
            behaviors = self.memcached_kwargs.get(
                "behaviors",
                {"tcp_nodelay": True, "ketama": True},
            )

            self._client = cast(
                _SyncMemcachedClient,
                pylibmc.Client(
                    [self.server],
                    binary=True,
                    behaviors=behaviors,
                    username=username,
                    password=password,
                ),
            )

        except ImportError:
            logger.exception("Memcached library not installed. Install with: pip install pylibmc")
            raise
        except Exception as exc:
            logger.exception("Failed to connect to Memcached server at %s", self.server)
            raise ConnectionError from exc

    def get(self, key: str) -> bytes | None:
        """
        Retrieve cached value.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        try:
            return self._client.get(key)
        except Exception as e:
            logger.exception("Memcached get failed for key '%s'", key, exc_info=e)
            return None

    async def aget(self, key: str) -> bytes | None:
        """
        Retrieve cached value.

        Returns:
            bytes | None: The cached value or None if not found/expired.
        """

        return self.get(key)

    def set(self, key: str, value: Any, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (Any): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        try:
            self._client.set(key=key, time=ttl, val=value)
        except Exception as e:
            logger.exception(f"Memcached set failed for key '{key}'", exc_info=e)

    async def aset(self, key: str, value: Any, ttl: int) -> None:
        """
        Store value with TTL.

        Args:
            key (str): The cache key.
            value (Any): The value to store.
            ttl (int): Time-to-live in seconds.
        """

        self.set(key, value, ttl)

    def delete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        try:
            self._client.delete(key)
        except Exception as e:
            logger.exception(f"Memcached delete failed for key '{key}'", exc_info=e)

    async def adelete(self, key: str) -> None:
        """
        Delete specific cache entry.

        Args:
            key (str): The cache key to delete.
        """

        self.delete(key)

    def clear(self, **kwargs: Any) -> bool | None:
        """
        Clear all cache entries.

        Args:
            **kwargs: Memcached-specific options:
                - delay (int): Number of seconds to wait before flushing. Default: 0.
                - noreply (bool): If True, the server will not send a reply. Default: False.

        Returns:
            bool | None: The server response or None.
        """

        delay = kwargs.get("delay", 0)
        noreply = kwargs.get("noreply", False)

        try:
            return self._client.flush_all(delay=delay, noreply=noreply)
        except Exception as e:
            logger.exception("Memcached clear failed", exc_info=e)
            return None

    async def aclear(self, **kwargs: Any) -> bool | None:
        """
        Clear all cache entries asynchronously.

        Args:
            **kwargs: Memcached-specific options:
                - delay (int): Number of seconds to wait before flushing. Default: 0.
                - noreply (bool): If True, the server will not send a reply. Default: False.

        Returns:
            bool | None: The server response or None.
        """

        return self.clear(**kwargs)
