import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse, JSONResponse
from staticware import StaticFiles

import air
from air import Air, JinjaRenderer, Request

TEST_STATIC_DIR = "tests/static_test_files"


def test_static_hashes_files() -> None:
    """Test that StaticFiles computes hashes for files."""
    static = StaticFiles(TEST_STATIC_DIR)

    assert "styles.css" in static.file_map
    assert "images/logo.png" in static.file_map

    # Verify hash format: name.hash.ext
    hashed = static.file_map["styles.css"]
    assert hashed.startswith("styles.")
    assert hashed.endswith(".css")
    parts = hashed.split(".")
    assert len(parts) == 3
    assert len(parts[1]) == 8  # default hash length


def test_static_url() -> None:
    """Test that url() returns correct hashed URL."""
    static = StaticFiles(TEST_STATIC_DIR, prefix="/static")

    url = static.url("styles.css")
    assert url.startswith("/static/styles.")
    assert url.endswith(".css")

    # Test with leading slash
    url2 = static.url("/styles.css")
    assert url == url2


def test_static_url_subdirectory() -> None:
    """Test url() with files in subdirectories."""
    static = StaticFiles(TEST_STATIC_DIR)

    url = static.url("images/logo.png")
    assert url.startswith("/static/images/logo.")
    assert url.endswith(".png")


def test_static_url_unknown_file() -> None:
    """Test url() returns original path for unknown files."""
    static = StaticFiles(TEST_STATIC_DIR)

    url = static.url("nonexistent.js")
    assert url == "/static/nonexistent.js"


def test_static_serves_hashed_file() -> None:
    """Test serving files with hashed URLs."""
    app = Air()
    static = StaticFiles(TEST_STATIC_DIR)
    app.mount("/static", static, name="static")

    client = TestClient(app)
    url = static.url("styles.css")
    response = client.get(url)

    assert response.status_code == 200
    assert "body { color: red; }" in response.text
    assert response.headers["cache-control"] == "public, max-age=31536000, immutable"


def test_static_serves_unhashed_file() -> None:
    """Test serving files with direct (unhashed) URLs."""
    app = Air()
    static = StaticFiles(TEST_STATIC_DIR)
    app.mount("/static", static, name="static")

    client = TestClient(app)
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "body { color: red; }" in response.text
    # No aggressive caching for unhashed URLs
    assert "immutable" not in response.headers.get("cache-control", "")


def test_static_404_for_missing() -> None:
    """Test 404 for missing files."""
    app = Air()
    static = StaticFiles(TEST_STATIC_DIR)
    app.mount("/static", static, name="static")

    client = TestClient(app)
    response = client.get("/static/nonexistent.css")

    assert response.status_code == 404


def test_static_auto_registers_jinja_global() -> None:
    """Test that JinjaRenderer registers static() when passed an app with static."""
    app = Air()
    app.static = StaticFiles(TEST_STATIC_DIR)
    jinja = JinjaRenderer(directory="tests/templates", app=app)

    assert "static" in jinja.templates.env.globals
    static_func = cast("Callable[[str], str]", jinja.templates.env.globals["static"])
    url = static_func("styles.css")
    assert url.startswith("/static/styles.")
    assert url.endswith(".css")


def test_static_custom_prefix() -> None:
    """Test StaticFiles with custom URL prefix."""
    app = Air()
    static = StaticFiles(TEST_STATIC_DIR, prefix="/assets")
    app.mount("/assets", static, name="static")

    url = static.url("styles.css")
    assert url.startswith("/assets/styles.")

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200


def test_static_custom_hash_length() -> None:
    """Test StaticFiles with custom hash length."""
    static = StaticFiles(TEST_STATIC_DIR, hash_length=16)

    hashed = static.file_map["styles.css"]
    parts = hashed.split(".")
    assert len(parts[1]) == 16


def test_static_hash_is_content_based() -> None:
    """Test that hash changes when file content changes."""
    content = Path(TEST_STATIC_DIR, "styles.css").read_bytes()
    expected_hash = hashlib.sha256(content).hexdigest()[:8]

    static = StaticFiles(TEST_STATIC_DIR)
    hashed = static.file_map["styles.css"]

    assert expected_hash in hashed


def test_static_in_template(tmp_path: Path) -> None:
    """Test using static() in a Jinja template."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "with_static.html"
    template_file.write_text('<link href="{{ static(\'styles.css\') }}" rel="stylesheet">')

    app = Air()
    app.static = StaticFiles(TEST_STATIC_DIR)
    jinja = JinjaRenderer(directory=str(template_dir), app=app)

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
        return jinja(request, "with_static.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert "/static/styles." in response.text
    assert '.css" rel="stylesheet">' in response.text


def test_static_nonexistent_directory() -> None:
    """Test StaticFiles handles nonexistent directory gracefully."""
    static = StaticFiles("nonexistent_directory_12345")

    assert len(static.file_map) == 0
    assert len(static._reverse) == 0

    # url() still works, returns original path
    url = static.url("styles.css")
    assert url == "/static/styles.css"


@pytest.mark.asyncio
async def test_static_ignores_non_http_scope() -> None:
    """Test that StaticFiles passes through non-HTTP scopes without responding."""
    static = StaticFiles(TEST_STATIC_DIR)
    scope = {"type": "websocket", "path": "/static/styles.css"}
    received: list[dict] = []

    async def receive() -> dict:
        return {}

    async def send(message: dict) -> None:
        received.append(message)

    await static(scope, receive, send)

    # Non-HTTP scopes should be ignored (no response sent)
    assert received == []


@pytest.mark.asyncio
async def test_static_returns_404_for_path_outside_prefix() -> None:
    """Test that StaticFiles returns 404 for paths outside its prefix."""
    static = StaticFiles(TEST_STATIC_DIR, prefix="/static")
    scope = {"type": "http", "path": "/other/styles.css"}
    received: list[dict] = []

    async def receive() -> dict:
        return {}

    async def send(message: dict) -> None:
        received.append(message)

    await static(scope, receive, send)

    assert received[0]["status"] == 404


def test_static_returns_404_for_deleted_file(tmp_path: Path) -> None:
    """Test that StaticFiles returns 404 when a hashed file is deleted after startup."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    temp_file = static_dir / "temp.css"
    temp_file.write_text("body { color: blue; }")

    app = Air()
    static = StaticFiles(str(static_dir))
    app.mount("/static", static, name="static")

    hashed_url = static.url("temp.css")
    temp_file.unlink()

    client = TestClient(app)
    response = client.get(hashed_url)

    assert response.status_code == 404


def test_air_auto_detects_static_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that Air auto-detects and mounts static/ when it exists."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "app.js").write_text("console.log('hello');")

    monkeypatch.chdir(tmp_path)
    app = Air()

    assert app.static is not None
    assert isinstance(app.static, StaticFiles)

    client = TestClient(app)
    response = client.get("/static/app.js")
    assert response.status_code == 200


def test_air_no_static_when_directory_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that Air.static is None when no static/ directory exists."""
    monkeypatch.chdir(tmp_path)
    app = Air()

    assert app.static is None


def test_jinja_renderer_auto_wires_static_from_app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that JinjaRenderer auto-wires static() when passed an app with static files."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "app.css").write_text("body { margin: 0; }")

    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "page.html").write_text("<link href=\"{{ static('app.css') }}\">")

    monkeypatch.chdir(tmp_path)

    app = Air()
    jinja = JinjaRenderer(directory=str(template_dir), app=app)

    @app.get("/")
    def page(request: Request) -> HTMLResponse:
        return jinja(request, "page.html")

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "/static/app." in response.text
    assert '.css">' in response.text


# =============================================================================
# StaticRewriteMiddleware tests
# =============================================================================


def test_rewrite_middleware_rewrites_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Normal HTML paths like /static/styles.css get rewritten to hashed versions."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/")
    def page() -> str:
        return '<link href="/static/styles.css" rel="stylesheet">'

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "/static/styles.css" not in response.text
    assert "/static/styles." in response.text
    assert '.css" rel="stylesheet">' in response.text


def test_rewrite_middleware_skips_non_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """JSON and other non-HTML responses are passed through unchanged."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/api")
    def api() -> JSONResponse:
        return JSONResponse({"url": "/static/styles.css"})

    client = TestClient(app)
    response = client.get("/api")

    assert response.status_code == 200
    assert response.json()["url"] == "/static/styles.css"


def test_rewrite_middleware_leaves_unknown_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Paths not in the file_map are left as-is."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/")
    def page() -> str:
        return '<script src="/static/unknown.js"></script>'

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert '/static/unknown.js"' in response.text


def test_rewrite_middleware_does_not_double_rewrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Already-hashed paths are not rewritten again."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    hashed = app.static.file_map["styles.css"]

    @app.get("/")
    def page() -> str:
        return f'<link href="/static/{hashed}">'

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert f"/static/{hashed}" in response.text


def test_rewrite_middleware_handles_subdirectories(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Paths with subdirectories like /static/css/app.css get rewritten."""
    static_dir = tmp_path / "static"
    css_dir = static_dir / "css"
    css_dir.mkdir(parents=True)
    (css_dir / "app.css").write_text("body { margin: 0; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/")
    def page() -> str:
        return '<link href="/static/css/app.css">'

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "/static/css/app.css" not in response.text
    assert "/static/css/app." in response.text
    assert '.css">' in response.text


def test_rewrite_middleware_works_with_air_tags(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Auto-rewriting works with Air tags, not just Jinja."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/")
    def page() -> air.Html:
        return air.Html(
            air.Head(air.Link(rel="stylesheet", href="/static/styles.css")),
            air.Body(air.H1("Hello")),
        )

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "/static/styles.css" not in response.text
    assert "/static/styles." in response.text


def test_rewrite_middleware_multiple_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Multiple static paths in one response all get rewritten."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "styles.css").write_text("body { color: red; }")
    (static_dir / "app.js").write_text("console.log('hi');")

    monkeypatch.chdir(tmp_path)
    app = Air()

    @app.get("/")
    def page() -> str:
        return '<link href="/static/styles.css"><script src="/static/app.js"></script>'

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "/static/styles.css" not in response.text
    assert "/static/app.js" not in response.text
    assert "/static/styles." in response.text
    assert "/static/app." in response.text
