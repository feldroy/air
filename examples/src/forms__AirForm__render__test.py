"""Tests for the AirForm.render example."""

from fastapi.testclient import TestClient

from .forms__AirForm__render import app

client = TestClient(app)


def test_contact_form_renders() -> None:
    """GET /contact should render the form."""
    response = client.get("/contact")
    assert response.status_code == 200
    assert "Contact us" in response.text
    assert "<form" in response.text


def test_contact_form_valid_submission() -> None:
    """Submitting valid data should show the success page."""
    response = client.post(
        "/contact",
        data={
            "name": "Alice",
            "email": "alice@example.com",
            "message": "Hello from tests!",
        },
    )
    assert response.status_code == 200
    assert "Thank you for your message!" in response.text


def test_contact_form_invalid_submission() -> None:
    """Submitting empty data should show the error page with error count."""
    response = client.post("/contact", data={})
    assert response.status_code == 200
    assert "Please fix the errors below." in response.text
    # Three required fields => three validation errors
    assert "Found 3 validation error(s)." in response.text
