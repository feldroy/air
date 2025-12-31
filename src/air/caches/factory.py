import logging
from typing import Any

from .base import CacheInterface
from .memcached import MemcachedCache
from .memory import InMemoryCache
from .redis import RedisCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheFactory:
    """Factory for creating cache backends with automatic fallback."""

    @staticmethod
    def create(config: dict[str, Any] | None = None) -> CacheInterface:
        """
        Create a cache backend from configuration.

        Args:
            config: Cache configuration dict with 'engine' key. \
                Supported engines: "memory", "redis" (or "valkey"), "memcached".
                Example: {"engine": "redis", "url": "redis://localhost:6379"}

        Returns:
            CacheInterface implementation

        Falls back to InMemoryCache if:
        - config is None
        - engine dependencies not installed
        - connection to external cache fails
        """

        if config is None:
            logger.info("No cache config provided, using in-memory cache")
            return InMemoryCache()

        engine = config.get("engine", "memory").lower()

        if engine == "memory":
            return InMemoryCache(
                default_ttl=config.get("default_ttl", 300),
                max_size=config.get("max_size", 1000),
            )

        if engine in ("redis", "valkey"):
            try:
                return RedisCache(
                    url=config.get("url", "redis://localhost:6379"),
                    default_ttl=config.get("default_ttl", 300),
                    **config.get("redis_kwargs", {}),
                )
            except (ImportError, ConnectionError) as e:
                logger.warning(f"Failed to initialize Redis cache: {e}. Falling back to in-memory cache.")
                return InMemoryCache()

        elif engine == "memcached":
            try:
                return MemcachedCache(
                    servers=config.get("servers", ["127.0.0.1:11211"]),
                    default_ttl=config.get("default_ttl", 300),
                    **config.get("memcached_kwargs", {}),
                )
            except (ImportError, ConnectionError) as e:
                logger.warning(f"Failed to initialize Memcached cache: {e}. Falling back to in-memory cache.")
                return InMemoryCache()

        else:
            logger.warning(f"Unknown cache engine '{engine}'. Falling back to in-memory cache.")
            return InMemoryCache()
