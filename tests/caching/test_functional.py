import pytest
from fastapi.testclient import TestClient

import air
from air.caches import InMemoryCache


@pytest.mark.parametrize(
    "cache",
    [
        InMemoryCache(),
    ],
)
def test_cache_backend_functionality(cache: InMemoryCache) -> None:
    """Test basic functionality across all cache backends."""
    app = air.Air(cache=cache)
    call_count = 0

    @app.page(cache_ttl=60)
    def backend_test_page() -> air.H1:
        nonlocal call_count
        call_count += 1
        return air.H1(f"Backend test: {call_count}")

    client = TestClient(app)

    response1 = client.get("/backend-test-page")
    assert response1.status_code == 200
    assert call_count == 1

    response2 = client.get("/backend-test-page")
    assert response2.status_code == 200
    assert call_count == 1
