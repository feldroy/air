from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

import air


def test_middleware_with_sync_handler() -> None:
    """Middleware on the event loop works with sync handlers in a threadpool (#1067)."""
    app = air.Air()

    # Middleware that adds a custom header to every response.
    class AddHeaderMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: object) -> Response:
            response = await call_next(request)  # type: ignore[misc]
            response.headers["X-Custom"] = "middleware-ran"
            return response

    app.add_middleware(AddHeaderMiddleware)

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
        assert response.headers["X-Custom"] == "middleware-ran"
        assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_session_middleware() -> None:
    app = air.Air()
    app.add_middleware(air.SessionMiddleware, secret_key="change-me")

    @app.page
    async def check(request: air.Request) -> air.Html | air.Children:
        return air.layouts.mvpcss(
            air.H1(request.session.get("timestamp")),
        )

    @app.page
    async def reset(request: air.Request) -> air.P:
        request.session.pop("timestamp")
        return air.P("Reset")

    @app.get("/{timestamp}")
    async def home(request: air.Request, timestamp: int) -> air.Html | air.Children:
        request.session["timestamp"] = timestamp
        return air.layouts.mvpcss(
            air.H1(request.session.get("timestamp")),
        )

    client = TestClient(app)

    response = client.get("/123456")
    assert response.status_code == 200
    assert "123456" in response.text

    response = client.get("/check")
    assert response.status_code == 200
    assert "123456" in response.text

    response = client.get("/reset")
    response = client.get("/check")
    assert response.status_code == 200
    assert "123456" not in response.text
    assert "None" in response.text

    response = client.get("/654321")
    assert response.status_code == 200
    assert "654321" in response.text

    response = client.get("/check")
    assert response.status_code == 200
    assert "654321" in response.text


def _build_csrf_app() -> air.Air:
    app = air.Air()
    app.add_middleware(air.CSRFMiddleware)
    jinja = air.JinjaRenderer(directory="tests/templates")

    @app.get("/form")
    def form(request: air.Request) -> HTMLResponse:
        return jinja(request, name="csrf_form.html")

    @app.post("/submit")
    async def submit(request: air.Request) -> air.P:
        form_data = await request.form()
        return air.P(f"Hello {form_data.get('name', '')}")

    return app


def test_csrf_middleware_accepts_valid_form_token() -> None:
    app = _build_csrf_app()
    client = TestClient(app)

    form_response = client.get("/form")
    token = form_response.cookies.get("air_csrf_token")
    assert token is not None

    response = client.post("/submit", data={"csrf_token": token, "name": "Cheddar"})
    assert response.status_code == 200
    assert "Hello Cheddar" in response.text


def test_csrf_middleware_rejects_missing_form_token() -> None:
    app = _build_csrf_app()
    client = TestClient(app)

    client.get("/form")
    response = client.post("/submit", data={"name": "Brie"})
    assert response.status_code == 403
    assert response.text == "CSRF verification failed."


def test_csrf_middleware_rejects_invalid_form_token() -> None:
    app = _build_csrf_app()
    client = TestClient(app)

    client.get("/form")
    response = client.post("/submit", data={"csrf_token": "bad-token", "name": "Gouda"})
    assert response.status_code == 403
    assert response.text == "CSRF verification failed."


def test_csrf_middleware_accepts_header_token() -> None:
    app = _build_csrf_app()
    client = TestClient(app)

    form_response = client.get("/form")
    token = form_response.cookies.get("air_csrf_token")
    assert token is not None

    response = client.post("/submit", data={"name": "Swiss"}, headers={"X-CSRF-Token": token})
    assert response.status_code == 200
    assert "Hello Swiss" in response.text
