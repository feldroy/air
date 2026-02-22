from fastapi import Depends, FastAPI
from fastapi.routing import APIRouter
from fastapi.testclient import TestClient
from starlette.requests import Request

import air
from air.exception_handlers import (
    DEFAULT_EXCEPTION_HANDLERS,
    default_500_exception_handler,
)


def test_air_app_factory() -> None:
    app = air.Air()

    # @app.get("/test", response_class=AirResponse)
    @app.get("/test")
    def page() -> air.H1:
        return air.H1("Hello, World!")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_air_plus_fastapi() -> None:
    app = FastAPI()
    html = air.Air()

    @app.get("/api")
    def api() -> dict[str, str]:
        return {"text": "hello, world"}

    @html.get("/page")
    def page() -> air.H1:
        return air.H1("Hello, World!")

    @html.get("/html-page")
    def html_page() -> str:
        return "<h1>Hello, World!</h1>"

    # Combine into one app
    app.mount("/", html)

    client = TestClient(app)

    # Test the API
    response = client.get("/api")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"text": "hello, world"}

    # Test the page
    response = client.get("/page")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"

    # Test the page with HTML
    response = client.get("/html-page")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_page_decorator() -> None:
    app = air.Air()
    page = app.page

    @page
    def index() -> air.H1:
        return air.H1("Home page")

    @page
    def about_us() -> str:
        return "<h1>About page</h1>"

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Home page</h1>"

    response = client.get("/about-us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>About page</h1>"


def test_page_decorator_with_default_path_separator() -> None:
    app = air.Air()  # default path_separator "-"
    page = app.page

    @page
    def contact_us() -> str:
        return "<h1>Contact page</h1>"

    client = TestClient(app)
    response = client.get("/contact-us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Contact page</h1>"


def test_page_decorator_with_path_separator() -> None:
    app = air.Air(path_separator="/")
    page = app.page

    @page
    def contact_us() -> str:
        return "<h1>Contact page</h1>"

    client = TestClient(app)
    response = client.get("/contact/us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Contact page</h1>"


def test_air_404_response() -> None:
    app = air.Air()

    client = TestClient(app)
    response = client.get("/nonexistent")

    assert response.status_code == 404
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet"><style>footer, header,'
        " main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script "
        'src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" '
        'integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>'
        "<title>404 Not Found</title></head><body><main><h1>404 Not Found</h1>"
        "<p>The requested resource was not found on this server.</p><p>URL: http://testserver/nonexistent</p>"
        "</main></body></html>"
    )


def test_default_500_exception_handler() -> None:
    # Create a mock request and exception
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "server": ("testserver", 80),
        "headers": [],
    }
    request = Request(scope)
    exc = Exception("Test exception")

    # Call the handler
    response = default_500_exception_handler(request, exc)

    # Check the response
    assert response.status_code == 500
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.body == b'<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet">'
        b"<style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script"
        b' src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous"'
        b' integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>'
        b"<title>500 Internal Server Error</title></head><body><main><h1>500 Internal Server Error</h1>"
        b"<p>An internal server error occurred.</p></main></body></html>"
    )


def test_injection_of_default_exception_handlers() -> None:
    def handler(request: air.Request, exc: Exception) -> air.AirResponse:
        return air.AirResponse()

    custom_exception_handlers = {
        405: handler,
    }

    app = air.Air(exception_handlers=custom_exception_handlers)

    # Check injection of both custom and default exception handlers
    expected_handlers = {**DEFAULT_EXCEPTION_HANDLERS, **custom_exception_handlers}
    assert set(expected_handlers) <= set(app.exception_handlers)
    assert app.exception_handlers[405] is handler


def test_url_helper_method() -> None:
    """Test that route decorators have .url() method for URL generation."""
    app = air.Air()

    @app.get("/users/{user_id}/posts/{post_id}")
    def get_post(user_id: int, post_id: int) -> air.H1:
        return air.H1(f"User {user_id}, Post {post_id}")

    @app.page
    def about() -> air.H1:
        return air.H1("About")

    assert get_post.url(user_id=123, post_id=456) == "/users/123/posts/456"
    assert about.url() == "/about"

    client = TestClient(app)
    url = get_post.url(user_id=1, post_id=2)
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == "<h1>User 1, Post 2</h1>"


def test_url_helper_supports_query_params() -> None:
    app = air.Air()

    @app.get("/search")
    def search(q: str, page: int = 1) -> air.H1:
        return air.H1(f"Search: {q} page {page}")

    url = search.url(query_params={"q": "air", "page": 3})
    assert url == "/search?q=air&page=3"

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == "<h1>Search: air page 3</h1>"


def test_url_helper_supports_query_params_with_query() -> None:
    app = air.Air()

    @app.get("/search")
    def search(q: str, page: int = air.Query(1)) -> air.H1:
        return air.H1(f"Search: {q} page {page}")

    url = search.url(query_params={"q": "air", "page": 3})
    assert url == "/search?q=air&page=3"

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == "<h1>Search: air page 3</h1>"


def test_patch_endpoint() -> None:
    app = air.Air()

    @app.patch("/items/{item_id}")
    def update_item(item_id: int) -> air.H1:
        return air.H1(f"Updated item {item_id}")

    client = TestClient(app)
    response = client.patch("/items/42")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Updated item 42</h1>"


def test_put_endpoint() -> None:
    app = air.Air()

    @app.put("/items/{item_id}")
    def replace_item(item_id: int) -> air.H1:
        return air.H1(f"Replaced item {item_id}")

    client = TestClient(app)
    response = client.put("/items/42")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Replaced item 42</h1>"


def test_delete_endpoint() -> None:
    app = air.Air()

    @app.delete("/items/{item_id}")
    def delete_item(item_id: int) -> air.H1:
        return air.H1(f"Deleted item {item_id}")

    client = TestClient(app)
    response = client.delete("/items/42")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Deleted item 42</h1>"


def test_app_state() -> None:
    """Test that app.state property exposes application state."""
    app = air.Air()
    app.state.counter = 0

    @app.get("/count")
    def count() -> air.H1:
        app.state.counter += 1
        return air.H1(f"Count: {app.state.counter}")

    client = TestClient(app)
    response = client.get("/count")
    assert response.text == "<h1>Count: 1</h1>"
    assert app.state.counter == 1


def test_app_router() -> None:
    """Test that app.router property exposes the APIRouter."""
    app = air.Air()

    @app.get("/test")
    def page() -> air.H1:
        return air.H1("Test")

    assert isinstance(app.router, APIRouter)
    assert len(app.router.routes) > 0


def test_app_routes() -> None:
    """Test that app.routes property exposes the list of routes."""
    app = air.Air()

    @app.get("/test")
    def page() -> air.H1:
        return air.H1("Test")

    routes = app.routes
    assert isinstance(routes, list)
    assert any(getattr(r, "path", None) == "/test" for r in routes)


def test_app_debug() -> None:
    """Test that app.debug property exposes and sets debug mode."""
    app = air.Air(debug=False)
    assert app.debug is False

    app.debug = True
    assert app.debug is True


def test_app_dependency_overrides() -> None:
    """Test that app.dependency_overrides property works for testing."""
    app = air.Air()

    def get_db() -> str:
        return "real_db"

    def mock_db() -> str:
        return "mock_db"

    @app.get("/db")
    def db_endpoint(db: str = Depends(get_db)) -> air.H1:
        return air.H1(f"DB: {db}")

    client = TestClient(app)
    response = client.get("/db")
    assert response.text == "<h1>DB: real_db</h1>"

    app.dependency_overrides[get_db] = mock_db
    response = client.get("/db")
    assert response.text == "<h1>DB: mock_db</h1>"


def test_fastapi_app_property() -> None:
    """Test that fastapi_app property exposes the underlying FastAPI instance."""
    app = air.Air()

    assert isinstance(app.fastapi_app, FastAPI)
    assert app.fastapi_app is app._app


def test_sync_endpoint_returns_html() -> None:
    """Sync endpoints produce correct HTML (#1067)."""
    app = air.Air()

    @app.get("/sync")
    def sync_page() -> air.H1:
        return air.H1("Sync")

    @app.get("/async")
    async def async_page() -> air.H1:
        return air.H1("Async")

    client = TestClient(app)
    for path in ["/sync", "/async"]:
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_sync_endpoint_not_on_event_loop() -> None:
    """Sync endpoints run in a threadpool, not blocking the event loop (#1067)."""
    import asyncio  # noqa: PLC0415

    app = air.Air()
    has_loop: dict[str, bool] = {}

    @app.get("/sync")
    def sync_page() -> air.H1:
        try:
            asyncio.get_running_loop()
            has_loop["sync"] = True
        except RuntimeError:
            has_loop["sync"] = False
        return air.H1("Sync")

    @app.get("/async")
    async def async_page() -> air.H1:
        try:
            asyncio.get_running_loop()
            has_loop["async"] = True
        except RuntimeError:
            has_loop["async"] = False
        return air.H1("Async")

    client = TestClient(app)
    client.get("/sync")
    client.get("/async")

    assert has_loop["sync"] is False, "sync handler should not be on the event loop"
    assert has_loop["async"] is True, "async handler should be on the event loop"


def test_sync_endpoint_exception_propagates() -> None:
    """Exceptions in sync handlers propagate through the threadpool (#1067)."""
    app = air.Air()

    @app.get("/error")
    def error_page() -> air.H1:
        msg = "sync handler error"
        raise ValueError(msg)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/error")
    assert response.status_code == 500


def test_custom_kwargs_forwarded() -> None:
    """Route kwargs like status_code and tags reach FastAPI."""
    app = air.Air()

    @app.post("/created", status_code=201, tags=["items"])
    def create_item() -> air.H1:
        return air.H1("Created")

    client = TestClient(app)
    response = client.post("/created")
    assert response.status_code == 201
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Created</h1>"


def test_custom_response_class() -> None:
    """Custom response_class is used instead of AirResponse."""
    app = air.Air()

    class WrappingResponse(air.AirResponse):
        """Custom response that wraps content in an <article> tag."""

        def render(self, tag: object) -> bytes:
            return str(air.Article(tag)).encode()

    @app.get("/custom", response_class=WrappingResponse)
    def custom_page() -> air.H1:
        return air.H1("Inside article")

    client = TestClient(app)
    response = client.get("/custom")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<article><h1>Inside article</h1></article>"


def test_response_passthrough_sync_and_async() -> None:
    """Response objects pass through without conversion."""
    app = air.Air()

    @app.get("/sync-redirect")
    def sync_redirect() -> air.RedirectResponse:
        return air.RedirectResponse("/target")

    @app.get("/async-redirect")
    async def async_redirect() -> air.RedirectResponse:
        return air.RedirectResponse("/target")

    client = TestClient(app)
    for path in ["/sync-redirect", "/async-redirect"]:
        response = client.get(path, follow_redirects=False)
        assert response.status_code == 307
