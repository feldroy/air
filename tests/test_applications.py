from fastapi import FastAPI
from fastapi.testclient import TestClient

import air


def test_air_app_factory():
    app = air.Air()

    @app.get("/test")
    def test_endpoint():
        return air.H1("Hello, World!")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_air_plus_fastapi():
    app = FastAPI()
    html = air.Air()

    @app.get("/api")
    def test_api():
        return {"text": "hello, world"}

    @html.get("/page")
    def test_page():
        return air.H1("Hello, World!")

    @html.get("/page-html")
    def test_page_html():
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


def test_page_decorator():
    app = air.Air()
    page = app.page

    @page
    def index():
        return air.H1("Home page")

    @page
    def about_us():
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


def test_air_404_response():
    app = air.Air()

    client = TestClient(app)
    response = client.get("/nonexistent")

    assert response.status_code == 404
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet" /><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><title>404 Not Found</title></head><body><main><h1>404 Not Found</h1><p>The requested resource was not found on this server.</p><p>URL: http://testserver/nonexistent</p></main></body></html>'
    )


def test_default_500_exception_handler():
    from starlette.requests import Request

    from air.applications import default_500_exception_handler

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
        response.body
        == b'<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet" /><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><title>500 Internal Server Error</title></head><body><main><h1>500 Internal Server Error</h1><p>An internal server error occurred.</p></main></body></html>'
    )
