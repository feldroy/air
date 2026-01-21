from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse
from starlette.routing import BaseRoute, NoMatchFound

import air
from air import H1
from air.responses import AirResponse
from air.routing import AirRoute


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
    assert not router.prefix


def test_air_router_get_with_awaitable_result() -> None:
    """Test GET method with async function that returns awaitable result"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/async-test")
    async def async_endpoint() -> air.H1:
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
    async def async_post_endpoint() -> air.H1:
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


def test_air_router_get_with_url_method() -> None:
    """Test GET method with url helper function"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/url-helper-test")
    def url_helper_endpoint() -> H1:
        return air.H1(f"Item URL: {url_helper_endpoint_with_params.url(item_id=42)}")

    @router.get("/url-helper-test-with-params/{item_id}")
    def url_helper_endpoint_with_params(item_id: int) -> H1:
        return air.H1("Item URL with params")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/url-helper-test")
    assert response.status_code == 200
    assert response.text == "<h1>Item URL: /url-helper-test-with-params/42</h1>"


def test_air_router_get_with_url_method_throws_error() -> None:
    """Test GET method with url helper function throwing error on missing params"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/url-helper-error-test")
    def url_helper_error_endpoint() -> H1:
        try:
            return air.H1(f"Item URL: {url_helper_error_endpoint_with_params.url()}")
        except NoMatchFound as e:
            return air.H1(f"Error: {type(e).__name__}")

    @router.get("/url-helper-error-test-with-params/{item_id}")
    def url_helper_error_endpoint_with_params(item_id: int) -> H1:
        return air.H1("Item URL with params")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/url-helper-error-test")
    assert response.text == "<h1>Error: NoMatchFound</h1>"


def test_air_router_get_url_method_different_path() -> None:
    """Test GET method with url helper function using different path"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/")
    def index() -> H1:
        return air.H1(f"Profile URL: {profile_page.url(username='johndoe')}")

    @router.get("/profile/{username}")
    def profile_page(username: str) -> H1:
        return air.H1(f"Profile page {username}")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>Profile URL: /profile/johndoe</h1>"


def test_air_router_url_helper_supports_query_params() -> None:
    """Test URL helper with query_params argument"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/items/{item_id}")
    def get_item(
        item_id: int,
        tags: list[str] | None = air.Query(None),  # noqa: B008
        page: int = 1,
    ) -> air.P:
        return air.P(f"Item {item_id} tags {tags} page {page}")

    app.include_router(router)

    url = get_item.url(item_id=5, query_params={"tags": ["a", "b"], "page": 2})
    assert url == "/items/5?tags=a&tags=b&page=2"

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == "<p>Item 5 tags [&#x27;a&#x27;, &#x27;b&#x27;] page 2</p>"


def test_air_router_url_helper_empty_query_params() -> None:
    """Test URL helper returns base path when query_params is empty or contains empty lists."""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/items/{item_id}")
    def get_item(
        item_id: int,
        tags: list[str] | None = air.Query(None),  # noqa: B008
        page: int = 1,
    ) -> air.P:
        return air.P(f"Item {item_id} tags {tags} page {page}")

    app.include_router(router)

    assert get_item.url(item_id=5, query_params={}) == "/items/5"
    assert get_item.url(item_id=5, query_params={"tags": []}) == "/items/5"

    client = TestClient(app)
    response = client.get(get_item.url(item_id=5))
    assert response.status_code == 200
    assert response.text == "<p>Item 5 tags None page 1</p>"


def test_air_router_url_helper_supports_query_params_with_query() -> None:
    """Test URL helper with query_params argument when parameters use Query()."""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/items/{item_id}")
    def get_item(
        item_id: int,
        tags: list[str] | None = air.Query(None),  # noqa: B008
        page: int = air.Query(1),
    ) -> air.P:
        return air.P(f"Item {item_id} tags {tags} page {page}")

    app.include_router(router)

    url = get_item.url(item_id=5, query_params={"tags": ["a", "b"], "page": 2})
    assert url == "/items/5?tags=a&tags=b&page=2"

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == "<p>Item 5 tags [&#x27;a&#x27;, &#x27;b&#x27;] page 2</p>"


def test_air_router_post_with_url_method() -> None:
    """Test POST method with url helper function"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-url-helper-test")
    def post_url_helper_endpoint() -> H1:
        return air.H1(f"Item URL: {post_url_helper_endpoint_with_params.url(item_id=99)}")

    @router.post("/post-url-helper-test-with-params/{item_id}")
    def post_url_helper_endpoint_with_params(item_id: int) -> H1:
        return air.H1("POST Item URL with params")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-url-helper-test")
    assert response.status_code == 200
    assert response.text == "<h1>Item URL: /post-url-helper-test-with-params/99</h1>"


def test_air_router_post_with_url_method_throws_error() -> None:
    """Test POST method with url helper function throwing error on missing params"""
    app = air.Air()
    router = air.AirRouter()

    @router.post("/post-url-helper-error-test")
    def post_url_helper_error_endpoint() -> H1:
        try:
            return air.H1(f"Item URL: {post_url_helper_error_endpoint_with_params.url()}")
        except NoMatchFound as e:
            return air.H1(f"Error: {type(e).__name__}")

    @router.post("/post-url-helper-error-test-with-params/{item_id}")
    def post_url_helper_error_endpoint_with_params(item_id: int) -> H1:
        return air.H1("POST Item URL with params")

    app.include_router(router)
    client = TestClient(app)

    response = client.post("/post-url-helper-error-test")
    assert response.text == "<h1>Error: NoMatchFound</h1>"


def test_air_router_post_url_method_different_path() -> None:
    """Test POST method with url helper function using different path"""
    app = air.Air()
    router = air.AirRouter()

    @router.get("/")
    def index() -> air.P:
        return air.P(save_profile_details.url(username="johndoe2"))

    @router.post("/save-profile/{username}")
    def save_profile_details(username: str) -> H1:
        return air.H1(f"Profile for {username} saved successfully")

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<p>/save-profile/johndoe2</p>"


def test_air_router_patch_endpoint() -> None:
    app = air.Air()
    router = air.AirRouter()

    @router.patch("/items/{item_id}")
    def update_item(item_id: int) -> air.H1:
        return air.H1(f"Updated item {item_id}")

    app.include_router(router)

    client = TestClient(app)
    # response = client.patch("/items/42")
    response = client.patch(update_item.url(item_id=42))
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Updated item 42</h1>"


def test_air_router_put_endpoint() -> None:
    app = air.Air()
    router = air.AirRouter()

    @router.put("/items/{item_id}")
    def put_item(item_id: int) -> air.H1:
        return air.H1(f"Updated item {item_id}")

    app.include_router(router)

    client = TestClient(app)
    response = client.put(put_item.url(item_id=42))
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Updated item 42</h1>"


def test_air_router_delete_endpoint() -> None:
    app = air.Air()
    router = air.AirRouter()

    @router.delete("/items/{item_id}")
    def delete_item(item_id: int) -> air.H1:
        return air.H1(f"Updated item {item_id}")

    app.include_router(router)

    client = TestClient(app)
    response = client.delete(delete_item.url(item_id=42))
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Updated item 42</h1>"


def test_air_router_default_404_handler() -> None:
    """Test that AirRouter correctly configures the default 404 handler."""
    router = air.AirRouter(prefix="/api")

    @router.get("/exists")
    def exists() -> air.H1:
        return air.H1("exists")

    client = TestClient(router)
    response = client.get("/api/not-found")
    assert response.status_code == 404
    assert "The requested resource was not found on this server." in response.text


def test_air_router_proxy_properties() -> None:
    """Test that AirRouter proxy properties correctly delegate to internal router."""

    def sample_dependency() -> str:
        return "dependency"

    @asynccontextmanager
    async def lifespan(app: air.AirRouter) -> AsyncGenerator:
        yield

    router = air.AirRouter(
        prefix="/api",
        tags=["test-tag"],
        dependencies=[Depends(sample_dependency)],
        responses={404: {"description": "Not found"}},
        deprecated=True,
        include_in_schema=False,
        redirect_slashes=False,
        route_class=AirRoute,
        lifespan=lifespan,
    )

    @router.get("/test")
    def test_endpoint() -> air.H1:
        return air.H1("test")

    # Test routes property
    assert isinstance(router.routes, list)
    assert len(router.routes) > 0
    assert all(isinstance(r, BaseRoute) for r in router.routes)

    # Test tags property
    assert router.tags == ["test-tag"]

    # Test dependencies property
    assert router.dependencies is not None
    assert len(router.dependencies) == 1

    # Test responses property
    assert router.responses == {404: {"description": "Not found"}}

    # Test callbacks property (empty list by default)
    assert router.callbacks == []

    # Test deprecated property
    assert router.deprecated is True

    # Test include_in_schema property
    assert router.include_in_schema is False

    # Test default_response_class property
    assert router.default_response_class == AirResponse

    # Test redirect_slashes property
    assert router.redirect_slashes is False

    # Test route_class property
    assert router.route_class == AirRoute

    # Test on_startup property (empty by default when using lifespan)
    assert isinstance(router.on_startup, list)

    # Test on_shutdown property (empty by default when using lifespan)
    assert isinstance(router.on_shutdown, list)

    # Test lifespan_context property
    assert router.lifespan_context is not None

    # Test dependency_overrides_provider property (None by default)
    assert router.dependency_overrides_provider is None

    # Test generate_unique_id_function property
    assert router.generate_unique_id_function is not None
