from fastapi.testclient import TestClient

import air
from air.caches import InMemoryCache


def test_ttl_override_per_page() -> None:
    """Test that different pages can have different TTLs."""
    app = air.Air(cache=InMemoryCache())
    count_60 = 0
    count_120 = 0

    @app.page(cache_ttl=60)
    def page_60s() -> air.H1:
        nonlocal count_60
        count_60 += 1
        return air.H1(f"60s: {count_60}")

    @app.page(cache_ttl=120)
    def page_120s() -> air.H1:
        nonlocal count_120
        count_120 += 1
        return air.H1(f"120s: {count_120}")

    client = TestClient(app)

    client.get("/page-60s")
    client.get("/page-120s")

    assert count_60 == 1
    assert count_120 == 1

    client.get("/page-60s")
    client.get("/page-120s")

    assert count_60 == 1
    assert count_120 == 1


def test_ttl_different_between_app_and_router() -> None:
    """Test that app pages and router pages can have different TTLs."""
    app = air.Air(cache=InMemoryCache())
    router = air.AirRouter()
    app_count = 0
    router_count = 0

    @app.page(cache_ttl=30)
    def app_page() -> air.H1:
        nonlocal app_count
        app_count += 1
        return air.H1(f"App: {app_count}")

    @router.page(cache_ttl=90)
    def router_page() -> air.H1:
        nonlocal router_count
        router_count += 1
        return air.H1(f"Router: {router_count}")

    app.include_router(router)
    client = TestClient(app)

    client.get("/app-page")
    client.get("/router-page")

    assert app_count == 1
    assert router_count == 1
