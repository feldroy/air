"""Tests for the AirForm.widget example."""

from fastapi.testclient import TestClient

from .forms__AirForm__widget import app

client = TestClient(app)


def test_contact_page_renders_custom_widget() -> None:
    """The GET /contact page should render the custom widget wrapper."""
    response = client.get("/contact")
    assert response.status_code == 200
    assert "Contact Us" in response.text
    assert "Custom widget wrapper" in response.text


def test_contact_form_valid_submission() -> None:
    """Submitting valid data should show the success message."""
    response = client.post(
        "/contact",
        data={
            "name": "Alice",
            "email": "alice@example.com",
            "message": "Hello from Air!",
        },
    )
    assert response.status_code == 200
    assert "Thank you for your message!" in response.text


def test_contact_form_missing_data_shows_errors() -> None:
    """Submitting with missing data should show the error page."""
    response = client.post("/contact", data={})
    assert response.status_code == 200
    assert "Please fix the errors below." in response.text
    # All three fields are missing, so we should see 3 errors.
    assert "Found 3 validation error(s)." in response.text
