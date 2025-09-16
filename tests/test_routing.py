import pytest
from fastapi.testclient import TestClient

import air


def test_air_routing() -> None:
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index():
        return air.H1("Hello, World!")

    @router.page
    def home():
        return air.H1("Hello, Air!")

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"

    response = client.get("/home")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, Air!</h1>"


def test_air_routing_prefix() -> None:
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index():
        return air.H1("Hello, World!")

    @router.page
    def home():
        return air.H1("Hello, Air!")

    with pytest.raises(AssertionError):
        app.include_router(router, prefix="/")


def test_air_router_default_none() -> None:
    """Test AirRouter when default parameter is None"""
    router = air.AirRouter(default=None)
    # Verify that when default=None, it gets set to Air class
    assert router.default is air.Air


def test_air_router_default_not_none() -> None:
    """Test AirRouter when default parameter is not None (covers other branch)"""

    def custom_default() -> str:
        return "custom"

    router = air.AirRouter(default=custom_default)
    # Verify that when default is provided, it's preserved
    assert router.default is custom_default


def test_air_router_prefix_validation() -> None:
    """Test prefix validation assertions"""
    # Test prefix must start with '/'
    with pytest.raises(AssertionError, match="A path prefix must start with '/'"):
        air.AirRouter(prefix="invalid")

    # Test prefix must not end with '/'
    with pytest.raises(AssertionError, match="A path prefix must not end with '/'"):
        air.AirRouter(prefix="/valid/")

    # Test valid prefix to cover the prefix validation lines
    router = air.AirRouter(prefix="/api")
    assert router.prefix == "/api"


def test_air_router_no_prefix() -> None:
    """Test AirRouter when no prefix is provided (covers other branch of prefix check)"""
    router = air.AirRouter()  # No prefix
    assert router.prefix == ""
