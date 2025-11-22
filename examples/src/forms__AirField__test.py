"""Tests for the AirField + AirForm example."""

from fastapi.testclient import TestClient

from examples.src.forms__AirField import app

client = TestClient(app)


def test_contact_form_renders_with_html5_attributes() -> None:
    """GET / should render the form with HTML5 attributes from AirField."""
    response = client.get("/")
    assert response.status_code == 200
    text = response.text

    # Page heading
    assert "Contact Form Example Using AirField" in text

    # Name field: label + minlength/maxlength
    assert '<label for="name">Full Name</label>' in text
    assert 'name="name"' in text
    assert 'minlength="2"' in text
    assert 'maxlength="50"' in text

    # Email field: label + type=email
    assert '<label for="email">Email Address</label>' in text
    assert 'name="email"' in text
    assert 'type="email"' in text

    # Message field: label + minlength/maxlength
    assert '<label for="message">Message</label>' in text
    assert 'name="message"' in text
    assert 'minlength="10"' in text
    assert 'maxlength="500"' in text

    # Preferred Date & Time: custom HTML5 type
    assert 'name="preferred_datetime"' in text
    assert 'type="datedatetime-local"' in text


def test_contact_form_valid_submit() -> None:
    """POST /submit with valid data should show the success page."""
    response = client.post(
        "/submit",
        data={
            "name": "John Doe",
            "email": "john@example.com",
            "message": "This is a valid message.",
            "preferred_datetime": "2025-01-01T10:00",
        },
    )
    assert response.status_code == 200
    text = response.text

    assert "Thanks for your message!" in text
    assert "John Doe" in text
    assert "john@example.com" in text
    assert "This is a valid message." in text
    assert "2025-01-01T10:00" in text


def test_contact_form_invalid_submit_shows_errors() -> None:
    """POST /submit with missing data should re-render with errors."""
    response = client.post("/submit", data={})
    assert response.status_code == 200
    text = response.text

    # We should be on the error page, not the success page
    assert "Please fix the errors below." in text
    assert "Thanks for your message!" not in text

    # Air's default_form_widget should mark invalid fields and show messages
    assert 'aria-invalid="true"' in text
    assert "This field is required." in text
