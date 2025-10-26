"""Tests for Air.post example."""

from fastapi.testclient import TestClient

from src_examples.applications__Air__post import app

client = TestClient(app)


def test_submit_form():
    """Test basic POST endpoint."""
    response = client.post("/submit")
    assert response.status_code == 200
    assert "Form Submitted!" in response.text


def test_create_user():
    """Test POST endpoint with request body."""
    response = client.post("/users", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    assert "User Created" in response.text
    assert "John Doe" in response.text
    assert "john@example.com" in response.text
