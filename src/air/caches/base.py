from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CacheInterface(Protocol):
    """
    Protocol defining the cache interface for Air framework.
    """

    def get(self, key: str) -> bytes | None:
        """Retrieve cached value synchronously."""
        raise NotImplementedError

    async def aget(self, key: str) -> bytes | None:
        """Retrieve cached value asynchronously."""
        raise NotImplementedError

    def set(self, key: str, value: bytes, ttl: int) -> None:
        """Store value in cache synchronously with TTL in seconds."""
        raise NotImplementedError

    async def aset(self, key: str, value: bytes, ttl: int) -> None:
        """Store value in cache asynchronously with TTL in seconds."""
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """Delete a specific cache entry synchronously."""
        raise NotImplementedError

    async def adelete(self, key: str) -> None:
        """Delete a specific cache entry asynchronously."""
        raise NotImplementedError

    def clear(self, **kwargs: Any) -> Any:
        """Clear all cache entries synchronously.

        Args:
            **kwargs: Backend-specific options (e.g., delay, noreply for Memcached).
        """
        raise NotImplementedError

    async def aclear(self, **kwargs: Any) -> Any:
        """Clear all cache entries asynchronously.

        Args:
            **kwargs: Backend-specific options (e.g., delay, noreply for Memcached).
        """
        raise NotImplementedError
