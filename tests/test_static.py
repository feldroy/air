import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse

from air import Air, JinjaRenderer, Request
from air.static import Static, enable

TEST_STATIC_DIR = "tests/static_test_files"


def test_static_digest_hashes_files() -> None:
    """Test that Static computes hashes for files."""
    digest = Static(TEST_STATIC_DIR)

    assert "styles.css" in digest.file_map
    assert "images/logo.png" in digest.file_map

    # Verify hash format: name.hash.ext
    hashed = digest.file_map["styles.css"]
    assert hashed.startswith("styles.")
    assert hashed.endswith(".css")
    parts = hashed.split(".")
    assert len(parts) == 3
    assert len(parts[1]) == 8  # default hash length


def test_static_digest_url() -> None:
    """Test that url() returns correct hashed URL."""
    digest = Static(TEST_STATIC_DIR, prefix="/static")

    url = digest.url("styles.css")
    assert url.startswith("/static/styles.")
    assert url.endswith(".css")

    # Test with leading slash
    url2 = digest.url("/styles.css")
    assert url == url2


def test_static_digest_url_subdirectory() -> None:
    """Test url() with files in subdirectories."""
    digest = Static(TEST_STATIC_DIR)

    url = digest.url("images/logo.png")
    assert url.startswith("/static/images/logo.")
    assert url.endswith(".png")


def test_static_digest_url_unknown_file() -> None:
    """Test url() returns original path for unknown files."""
    digest = Static(TEST_STATIC_DIR)

    url = digest.url("nonexistent.js")
    assert url == "/static/nonexistent.js"


def test_static_digest_serves_hashed_file() -> None:
    """Test serving files with hashed URLs."""
    app = Air()
    digest = Static(TEST_STATIC_DIR, app=app)

    client = TestClient(app)
    url = digest.url("styles.css")
    response = client.get(url)

    assert response.status_code == 200
    assert "body { color: red; }" in response.text
    assert response.headers["cache-control"] == "public, max-age=31536000, immutable"


def test_static_digest_serves_unhashed_file() -> None:
    """Test serving files with direct (unhashed) URLs."""
    app = Air()
    Static(TEST_STATIC_DIR, app=app)

    client = TestClient(app)
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "body { color: red; }" in response.text
    # No aggressive caching for unhashed URLs
    assert "immutable" not in response.headers.get("cache-control", "")


def test_static_digest_404_for_missing() -> None:
    """Test 404 for missing files."""
    app = Air()
    Static(TEST_STATIC_DIR, app=app)

    client = TestClient(app)
    response = client.get("/static/nonexistent.css")

    assert response.status_code == 404


def test_static_digest_auto_registers_jinja_global() -> None:
    """Test that Static registers static() in Jinja globals."""
    app = Air()
    jinja = JinjaRenderer(directory="tests/templates")

    Static(TEST_STATIC_DIR, app=app, jinja=jinja)

    assert "static" in jinja.templates.env.globals
    static_func = jinja.templates.env.globals["static"]
    url = static_func("styles.css")
    assert url.startswith("/static/styles.")
    assert url.endswith(".css")


def test_static_digest_custom_prefix() -> None:
    """Test Static with custom URL prefix."""
    app = Air()
    digest = Static(TEST_STATIC_DIR, app=app, prefix="/assets")

    url = digest.url("styles.css")
    assert url.startswith("/assets/styles.")

    client = TestClient(app)
    response = client.get(url)
    assert response.status_code == 200


def test_static_digest_custom_hash_length() -> None:
    """Test Static with custom hash length."""
    digest = Static(TEST_STATIC_DIR, hash_length=16)

    hashed = digest.file_map["styles.css"]
    parts = hashed.split(".")
    assert len(parts[1]) == 16


def test_enable_creates_digest_when_directory_exists() -> None:
    """Test enable() returns Static when directory exists."""
    app = Air()
    jinja = JinjaRenderer(directory="tests/templates")

    result = enable(app, jinja, directory=TEST_STATIC_DIR)

    assert result is not None
    assert isinstance(result, Static)
    assert "static" in jinja.templates.env.globals


def test_enable_returns_none_when_directory_missing() -> None:
    """Test enable() returns None when directory doesn't exist."""
    app = Air()
    jinja = JinjaRenderer(directory="tests/templates")

    result = enable(app, jinja, directory="nonexistent_directory")

    assert result is None


def test_static_digest_hash_is_content_based() -> None:
    """Test that hash changes when file content changes."""
    # Read the actual file content and compute expected hash
    content = Path(TEST_STATIC_DIR, "styles.css").read_bytes()
    expected_hash = hashlib.sha256(content).hexdigest()[:8]

    digest = Static(TEST_STATIC_DIR)
    hashed = digest.file_map["styles.css"]

    assert expected_hash in hashed


def test_static_digest_in_template(tmp_path: Path) -> None:
    """Test using static() in a Jinja template."""
    # Create a temporary template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "with_static.html"
    template_file.write_text('<link href="{{ static(\'styles.css\') }}" rel="stylesheet">')

    app = Air()
    jinja = JinjaRenderer(directory=str(template_dir))
    Static(TEST_STATIC_DIR, app=app, jinja=jinja)

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
        return jinja(request, "with_static.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert "/static/styles." in response.text
    assert '.css" rel="stylesheet">' in response.text


def test_static_digest_nonexistent_directory() -> None:
    """Test Static handles nonexistent directory gracefully."""
    digest = Static("nonexistent_directory_12345")

    assert len(digest.file_map) == 0
    assert len(digest._reverse) == 0

    # url() still works, returns original path
    url = digest.url("styles.css")
    assert url == "/static/styles.css"
