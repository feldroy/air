import pytest
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse

import air
from air import H1


def test_air_routing() -> None:
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index() -> H1:
        return air.H1("Hello, World!")

    @router.page
    def home() -> H1:
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


def test_air_routing_with_default_path_separator() -> None:
    app = air.Air()

    router = air.AirRouter()  # default path separator "-"

    @router.page
    def about_us() -> H1:
        return air.H1("About us!")

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/about-us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>About us!</h1>"


def test_air_routing_with_path_separator() -> None:
    app = air.Air()

    router = air.AirRouter(path_separator="/")

    @router.page
    def about_us() -> H1:
        return air.H1("About us!")

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/about/us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>About us!</h1>"


def test_air_routing_prefix() -> None:
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index() -> H1:
        return air.H1("Hello, World!")

    @router.page
    def home() -> H1:
        return air.H1("Hello, Air!")

    with pytest.raises(AssertionError):
        app.include_router(router, prefix="/")


def test_air_router_default_none() -> None:
    """Test AirRouter when default parameter is None"""
    router = air.AirRouter(default=None)
    # Verify that when default=None, it gets set to an ASGIApp
    # We have to use `callable()` instead of `issubclass` or `isinstance` because
    # python generics can't be type checked in this way and typing.get_origin
    # called on `router.default` returns `None` rather than anything meaningful.
    assert callable(router.default)


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


def test_air_router_get_with_awaitable_result() -> None:
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


def test_air_router_get_with_response_object() -> None:
    """Test GET method that returns Response object directly"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/response-test")
    def response_endpoint() -> HTMLResponse:
        return HTMLResponse(content="<p>Custom Response</p>")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/response-test")
    assert response.status_code == 200
    assert response.text == "<p>Custom Response</p>"


def test_air_router_post_basic() -> None:
    """Test POST method basic functionality"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-test")
    def post_endpoint() -> H1:
        return air.H1("POST Response")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-test")
    assert response.status_code == 200
    assert response.text == "<h1>POST Response</h1>"


def test_air_router_post_with_awaitable_result() -> None:
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


def test_air_router_post_with_response_object() -> None:
    """Test POST method that returns Response object directly"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-response-test")
    def post_response_endpoint() -> HTMLResponse:
        return HTMLResponse(content="<p>Custom POST Response</p>")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-response-test")
    assert response.status_code == 200
    assert response.text == "<p>Custom POST Response</p>"
