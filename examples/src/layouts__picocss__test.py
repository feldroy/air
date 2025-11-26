from fastapi.testclient import TestClient

from .layouts__picocss import app


def test_index_renders_full_layout() -> None:
    """Test that index page renders full HTML layout with PicoCSS"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    # Check full HTML structure
    assert "<html" in response.text
    assert "<head>" in response.text
    assert "<body>" in response.text
    # Check PicoCSS is included
    assert "picocss" in response.text or "pico" in response.text
    # Check HTMX is included
    assert "htmx.org" in response.text
    # Check content
    assert "Welcome to Air" in response.text
    assert "/dashboard" in response.text


def test_dashboard_renders_full_layout() -> None:
    """Test that dashboard page renders full HTML layout"""
    client = TestClient(app)
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "<html" in response.text
    assert "Dashboard" in response.text
    assert 'href="/"' in response.text


def test_htmx_request_returns_partial() -> None:
    """Test that HTMX request returns partial content without full layout"""
    client = TestClient(app)
    response = client.get("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    # Should NOT have full HTML structure
    assert "<html" not in response.text
    assert "<head>" not in response.text
    # Should still have the content
    assert "Welcome to Air" in response.text
    assert "<main" in response.text


def test_htmx_dashboard_returns_partial() -> None:
    """Test that HTMX dashboard request returns partial content"""
    client = TestClient(app)
    response = client.get("/dashboard", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert "<html" not in response.text
    assert "Dashboard" in response.text
