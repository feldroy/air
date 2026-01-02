from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

import air


@pytest.mark.asyncio
async def test_memcached_cache_mocked_integration() -> None:
    """Test MemcachedCache integration with Air using mocked client."""
    mock_pylibmc_module = Mock()
    mock_memcached_client = Mock()
    stored_data = {}

    def mock_get(key: str) -> bytes | None:
        return stored_data.get(key)

    def mock_set(key: str, time: int, val: bytes) -> bool:
        _ = time
        stored_data[key] = val
        return True

    mock_memcached_client.get.side_effect = mock_get
    mock_memcached_client.set.side_effect = mock_set
    mock_pylibmc_module.Client.return_value = mock_memcached_client

    with patch.dict("sys.modules", {"pylibmc": mock_pylibmc_module}):
        from air.caches import MemcachedCache  # noqa: PLC0415

        cache = MemcachedCache(server="127.0.0.1:11211")

        app = air.Air(cache=cache)
        call_count = 0

        @app.page(cache_ttl=60)
        def memcached_test_page() -> air.H1:
            nonlocal call_count
            call_count += 1
            return air.H1(f"Memcached test: {call_count}")

        client = TestClient(app)

        response1 = client.get("/memcached-test-page")
        assert response1.status_code == 200
        assert call_count == 1

        response2 = client.get("/memcached-test-page")
        assert response2.status_code == 200
        assert call_count == 1
