from time import sleep

from fastapi.testclient import TestClient

import air
from air.caches import InMemoryCache


def test_air_page_caching_basic() -> None:
    """Test basic page caching with Air."""
    app = air.Air(cache=InMemoryCache())
    call_count = 0

    @app.page(cache_ttl=60)
    def cached_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    client = TestClient(app)

    response1 = client.get("/cached-page")
    assert response1.status_code == 200
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/cached-page")
    assert response2.status_code == 200
    assert "Call count: 1" in response2.text
    assert call_count == 1


def test_air_page_caching_with_async() -> None:
    """Test page caching with async functions."""
    app = air.Air(cache=InMemoryCache())
    call_count = 0

    @app.page(cache_ttl=60)
    async def async_cached_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Async call count: {call_count}")

    client = TestClient(app)

    response1 = client.get("/async-cached-page")
    assert response1.status_code == 200
    assert "Async call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/async-cached-page")
    assert response2.status_code == 200
    assert "Async call count: 1" in response2.text
    assert call_count == 1


def test_air_page_without_caching() -> None:
    """Test that pages without cache_ttl are not cached."""
    app = air.Air(cache=InMemoryCache())
    call_count = 0

    @app.page
    def uncached_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    client = TestClient(app)

    response1 = client.get("/uncached-page")
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/uncached-page")
    assert "Call count: 2" in response2.text
    assert call_count == 2


def test_air_page_caching_ttl_expiration() -> None:
    """Test that cached pages expire after TTL."""
    app = air.Air(cache=InMemoryCache())
    call_count = 0

    @app.page(cache_ttl=1)
    def ttl_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    client = TestClient(app)

    response1 = client.get("/ttl-page")
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/ttl-page")
    assert "Call count: 1" in response2.text
    assert call_count == 1

    sleep(1.1)

    response3 = client.get("/ttl-page")
    assert "Call count: 2" in response3.text
    assert call_count == 2


def test_air_page_caching_serialization() -> None:
    """Test that page content is properly serialized and deserialized."""
    app = air.Air(cache=InMemoryCache())

    @app.page(cache_ttl=60)
    def complex_page() -> air.Div:
        return air.Div(
            air.H1("Title"),
            air.P("Paragraph"),
            air.Ul(air.Li("Item 1"), air.Li("Item 2")),
        )

    client = TestClient(app)

    response1 = client.get("/complex-page")
    assert response1.status_code == 200
    html1 = response1.text

    response2 = client.get("/complex-page")
    assert response2.status_code == 200
    html2 = response2.text

    assert html1 == html2
    assert "<h1>Title</h1>" in html1
    assert "<p>Paragraph</p>" in html1


def test_air_without_cache_configured() -> None:
    """Test that pages work normally when no cache is configured."""
    app = air.Air()
    call_count = 0

    @app.page(cache_ttl=60)
    def page_without_cache() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Call count: {call_count}")

    client = TestClient(app)

    response1 = client.get("/page-without-cache")
    assert "Call count: 1" in response1.text
    assert call_count == 1

    response2 = client.get("/page-without-cache")
    assert "Call count: 2" in response2.text
    assert call_count == 2
