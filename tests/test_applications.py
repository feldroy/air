from fastapi import FastAPI
from fastapi.testclient import TestClient

import air


def test_air_app_factory() -> None:
    app = air.Air()

    # @app.get("/test", response_class=AirResponse)
    @app.get("/test")
    def test_endpoint() -> air.H1:
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
    def test_api() -> dict[str, str]:
        return {"text": "hello, world"}

    @html.get("/page")
    def test_page() -> air.H1:
        return air.H1("Hello, World!")

    @html.get("/page-html")
    def test_page_html() -> str:
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
    response = client.get("/page-html")
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
    from starlette.requests import Request

    from air.exception_handlers import default_500_exception_handler

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
    from air.exception_handlers import DEFAULT_EXCEPTION_HANDLERS

    def handler(request: air.Request, exc: Exception) -> air.AirResponse:
        return air.AirResponse()

    CUSTOM_EXCEPTION_HANDLERS = {
        405: handler,
    }

    app = air.Air(exception_handlers=CUSTOM_EXCEPTION_HANDLERS)

    # Check injection of both custom and default exception handlers
    expected_handlers = {**DEFAULT_EXCEPTION_HANDLERS, **CUSTOM_EXCEPTION_HANDLERS}
    assert set(expected_handlers) <= set(app.exception_handlers)
    assert app.exception_handlers[405] is handler
