"""Tests for Air.get example."""

from fastapi.testclient import TestClient

from examples.src.applications__Air__get import app

client = TestClient(app)


def test_hello_world() -> None:
    """Test basic GET endpoint."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert "Hello, World!" in response.text


def test_get_user() -> None:
    """Test GET endpoint with path parameter."""
    response = client.get("/users/123")
    assert response.status_code == 200
    assert "User ID: 123" in response.text
    assert "user profile page" in response.text
