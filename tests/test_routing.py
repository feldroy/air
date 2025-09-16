import pytest
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse

import air


def test_air_routing():
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


def test_air_routing_prefix():
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


def test_air_router_default_none():
    """Test AirRouter when default parameter is None"""
    router = air.AirRouter(default=None)
    # Verify that when default=None, it gets set to Air class
    assert router.default is air.Air


def test_air_router_default_not_none():
    """Test AirRouter when default parameter is not None (covers other branch)"""

    def custom_default():
        return "custom"

    router = air.AirRouter(default=custom_default)
    # Verify that when default is provided, it's preserved
    assert router.default is custom_default


def test_air_router_prefix_validation():
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


def test_air_router_no_prefix():
    """Test AirRouter when no prefix is provided (covers other branch of prefix check)"""
    router = air.AirRouter()  # No prefix
    assert router.prefix == ""


def test_air_router_get_with_awaitable_result():
    """Test GET method with async function that returns awaitable result"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/async-test")
    async def async_endpoint():
        return air.H1("Async Hello!")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/async-test")
    assert response.status_code == 200
    assert response.text == "<h1>Async Hello!</h1>"


def test_air_router_get_with_response_object():
    """Test GET method that returns Response object directly"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/response-test")
    def response_endpoint():
        return HTMLResponse(content="<p>Custom Response</p>")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/response-test")
    assert response.status_code == 200
    assert response.text == "<p>Custom Response</p>"


def test_air_router_post_basic():
    """Test POST method basic functionality"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-test")
    def post_endpoint():
        return air.H1("POST Response")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-test")
    assert response.status_code == 200
    assert response.text == "<h1>POST Response</h1>"


def test_air_router_post_with_awaitable_result():
    """Test POST method with async function that returns awaitable result"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/async-post")
    async def async_post_endpoint():
        return air.H1("Async POST!")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/async-post")
    assert response.status_code == 200
    assert response.text == "<h1>Async POST!</h1>"


def test_air_router_post_with_response_object():
    """Test POST method that returns Response object directly"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-response-test")
    def post_response_endpoint():
        return HTMLResponse(content="<p>Custom POST Response</p>")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-response-test")
    assert response.status_code == 200
    assert response.text == "<p>Custom POST Response</p>"
