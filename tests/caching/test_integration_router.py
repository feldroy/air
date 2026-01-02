from fastapi.testclient import TestClient

import air
from air.caches import InMemoryCache


def test_router_cache_sharing_basic() -> None:
    """Test that routers inherit cache from app."""
    app = air.Air(cache=InMemoryCache())
    router = air.AirRouter()
    call_count = 0

    @router.page(cache_ttl=60)
    def router_cached_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Router call count: {call_count}")

    app.include_router(router)
    client = TestClient(app)

    response1 = client.get("/router-cached-page")
    assert response1.status_code == 200
    assert "Router call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/router-cached-page")
    assert response2.status_code == 200
    assert "Router call count: 1" in response2.text
    assert call_count == 1


def test_router_cache_sharing_decorator_before_include() -> None:
    """Test router cache sharing when decorator is applied before include_router.

    This is a regression test for the issue where decorators are evaluated at definition
    time (when router._cache is None), but include_router() (which shares the cache)
    happens later. The fix defers the cache check to runtime.
    """
    app = air.Air(cache=InMemoryCache())
    router = air.AirRouter()

    call_count = 0

    @router.page(cache_ttl=60)
    def early_decorated_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    app.include_router(router)

    client = TestClient(app)

    response1 = client.get("/early-decorated-page")
    assert response1.status_code == 200
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/early-decorated-page")
    assert response2.status_code == 200
    assert "Call count: 1" in response2.text
    assert call_count == 1


def test_router_cache_with_async_functions() -> None:
    """Test router cache sharing with async functions."""
    app = air.Air(cache=InMemoryCache())
    router = air.AirRouter()
    call_count = 0

    @router.page(cache_ttl=60)
    async def async_router_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Async router call: {call_count}")

    app.include_router(router)
    client = TestClient(app)

    response1 = client.get("/async-router-page")
    assert "Async router call: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/async-router-page")
    assert "Async router call: 1" in response2.text
    assert call_count == 1


def test_router_without_cache_configured() -> None:
    """Test router when app has no cache configured."""
    app = air.Air()
    router = air.AirRouter()
    call_count = 0

    @router.page(cache_ttl=60)
    def router_no_cache() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    app.include_router(router)
    client = TestClient(app)

    response1 = client.get("/router-no-cache")
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/router-no-cache")
    assert "Call count: 2" in response2.text
    assert call_count == 2


def test_multiple_routers_share_cache() -> None:
    """Test that multiple routers share the same cache instance."""
    app = air.Air(cache=InMemoryCache())
    router1 = air.AirRouter(prefix="/api")
    router2 = air.AirRouter(prefix="/web")

    app.include_router(router1)
    app.include_router(router2)

    assert router1._cache is app._cache
    assert router2._cache is app._cache
    assert router1._cache is router2._cache
