# Caching

Air provides built-in caching support for the `@app.page()` decorator, allowing you to cache rendered pages with configurable time-to-live (TTL) values. This can significantly improve performance for pages with expensive rendering operations.

## Overview

Air's caching system provides:

- **Multiple backends**: In-memory, Redis, and Memcached support
- **Simple decorator syntax**: Just add `cache_ttl` parameter to `@app.page()`
- **Zero dependencies for basic usage**: In-memory cache works out of the box
- **Graceful fallback**: Cache failures never break page rendering
- **Automatic cache sharing**: Cache instances propagate through `include_router()`

## Quick Start

The simplest way to use caching is with the built-in in-memory cache:

```python
import air
from air.caches import InMemoryCache

app = air.Air(cache=InMemoryCache())


@app.page(cache_ttl=60)  # Cache for 60 seconds
def about_page():
    return air.H1("About Page")
```

## Cache Backends

### In-Memory Cache

The in-memory cache stores data in your application's memory using an LRU (Least Recently Used) eviction policy. Perfect for single-instance deployments and development.

```python title="cache_inmemory.py"
from time import time

import uvicorn

import air
from air.caches import InMemoryCache

app = air.Air(cache=InMemoryCache())


@app.page(cache_ttl=60)  # 1 minute TTL
def about_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_inmemory_about_page_renders", 0) + 1
    globals()["_inmemory_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About — cache test"),
        air.H1(f"About Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P(
            "If this page is cached the render count will not increase until the TTL expires."
        ),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("InMemory Cache Sample"),
        air.H1("InMemory Cache Sample"),
        air.A("Go to About Page", href=about_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("cache_inmemory:app", host="127.0.0.1", port=8005, reload=True)
```

**Features:**

- No external dependencies required
- LRU eviction when max size reached (default: 100 items)
- Perfect for development and single-instance deployments

**Limitations:**

- Cache doesn't persist across restarts
- Not shared across multiple application instances

### Redis Cache

Redis provides persistent, distributed caching across multiple application instances. Ideal for production deployments.

```python title="cache_redis.py"
from time import time

import uvicorn

import air
from air.caches import RedisCache

app = air.Air(cache=RedisCache(url="redis://localhost:6379"))


@app.page(cache_ttl=60)  # 1 minute TTL
def about_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_redis_about_page_renders", 0) + 1
    globals()["_redis_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About — cache test"),
        air.H1(f"About Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P(
            "If this page is cached the render count will not increase until the TTL expires."
        ),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("Redis Cache Sample"),
        air.H1("Redis Cache Sample"),
        air.A("Go to About Page", href=about_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("cache_redis:app", host="127.0.0.1", port=8005, reload=True)
```

**Installation:**

```sh
uv add redis # when using uv
# pip install redis # when using plain pip
```

**Features:**

- Distributed caching across multiple instances
- Persistent cache (survives application restarts)
- High performance and scalability

### Memcached Cache

Memcached provides fast, distributed caching with a simple key-value interface.

```python title="cache_memcached.py"
from time import time

import uvicorn

import air
from air.caches import MemcachedCache

app = air.Air(
    cache=MemcachedCache(
        server="127.0.0.1:11211",
        username="your_username",  # Optional: for authenticated servers
        password="your_password",  # Optional: for authenticated servers
    )
)


@app.page(cache_ttl=60)  # 1 minute TTL
def about_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_memcached_about_page_renders", 0) + 1
    globals()["_memcached_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About — cache test"),
        air.H1(f"About Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P(
            "If this page is cached the render count will not increase until the TTL expires."
        ),
        air.A("Go back to home page", href=index.url()),
    )


@app.page(cache_ttl=30)  # 30 seconds TTL
async def aabout_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_memcached_async_about_page_renders", 0) + 1
    globals()["_memcached_async_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About (async) — cache test"),
        air.H1(f"About (async) Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P(
            "If this page is cached the render count will not increase until the TTL expires."
        ),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("Memcached Cache Sample"),
        air.H1("Memcached Cache Sample"),
        air.A("Go to About Page", href=about_page.url()),
        air.Br(),
        air.A("Go to About (async) Page", href=aabout_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run(
        "cache_memcached:app", host="127.0.0.1", port=8005, reload=True
    )
```

**Installation:**

```sh
uv add pylibmc # when using uv
# pip install pylibmc # when using plain pip
```

**Features:**

- Simple, fast distributed caching
- Battle-tested in production environments
- Lower memory overhead than Redis for simple caching

**Configuration options:**

- `server`: Server address as a string (e.g., `"127.0.0.1:11211"`). Defaults to `"127.0.0.1:11211"`.
- `default_ttl`: Default time-to-live in seconds. Defaults to `300`.
- `username`: Optional username for authenticated Memcached servers
- `password`: Optional password for authenticated Memcached servers
- `behaviors`: Optional dict of pylibmc behaviors (defaults: `{"tcp_nodelay": True, "ketama": True}`)
- `**memcached_kwargs`: Additional `pylibmc` client parameters

## Cache Factory

The `CacheFactory` provides a flexible way to create cache instances based on configuration, making it easy to switch between backends.

```python title="cache_factory.py"
from time import time

import uvicorn

import air
from air.caches import CacheFactory

app = air.Air(
    cache=CacheFactory.create(
        config={"engine": "redis", "url": "redis://localhost:6379"},
    )
)


@app.page(cache_ttl=60)  # 1 minute TTL
def about_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_factory_about_page_renders", 0) + 1
    globals()["_factory_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About — cache test"),
        air.H1(f"About Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P(
            "If this page is cached the render count will not increase until the TTL expires."
        ),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("Cache Factory Sample"),
        air.H1("Cache Factory Sample"),
        air.A("Go to About Page", href=about_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("cache_factory:app", host="127.0.0.1", port=8005, reload=True)
```

**Supported engines:**

- `"memory"` - In-memory cache
- `"redis"` - Redis cache
- `"memcached"` - Memcached cache

The factory automatically falls back to `InMemoryCache` if the requested backend is unavailable.

## Using Cache with Routers

Cache instances are automatically shared with routers when using `include_router()`:

```python
import air
from air.caches import RedisCache

app = air.Air(cache=RedisCache(url="redis://localhost:6379"))
router = air.AirRouter()


@router.page(cache_ttl=30)
def router_page():
    return air.H1("Cached router page")


# Router automatically inherits the app's cache
app.include_router(router)
```

## Decorator Syntax

The `@app.page()` decorator supports two syntaxes:

**Without arguments:**

```python
@app.page
def index():
    return air.H1("Not cached")
```

**With cache TTL:**

```python
@app.page(cache_ttl=60)
def cached_page():
    return air.H1("Cached for 60 seconds")
```

## How Caching Works

1. **Cache key generation**: Air generates a unique cache key using an MD5 hash of the function name and arguments. The cache key format is `__air:{func_name}:{args_hash}` where `args_hash` is an MD5 hash of the JSON-serialized arguments.
2. **Serialization**: Page content is serialized using Python's `pickle` module
3. **Storage**: Serialized content is stored in the configured cache backend with the specified TTL
4. **Retrieval**: On subsequent requests, Air checks the cache first before rendering the page
5. **Graceful degradation**: If cache operations fail, the page renders normally without caching

## Limitations

Current caching implementation has these limitations:

- **Page-level caching only**: The `cache_ttl` parameter is only available on `@app.page()` or `router.page()` decorator, not on other route decorators like `@app.get()` or `@app.post()`
- **No per-user caching**: All users see the same cached content for a given page (though cache keys include function arguments, so parameterized routes cache per unique parameter combination)
- **No cache invalidation API**: Cache entries expire based on TTL only
- **Pickle serialization**: Uses Python's pickle, which has security implications if cache is compromised
