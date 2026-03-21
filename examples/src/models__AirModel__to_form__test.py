from fastapi.testclient import TestClient

from .models__AirModel__to_form import app


def test_form_renders_with_excludes_and_widget() -> None:
    """Test that form renders with excludes and widget parameters"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    # Check the form demonstrates excludes and widget parameters
    assert "Contact Form" in response.text
    assert "demonstrates excludes and widget parameters" in response.text
    # Check custom widget styling
    assert "Custom form styling:" in response.text
    assert 'class="custom-form"' in response.text
    # Check excludes parameter: name and email rendered, phone excluded from display
    assert 'name="name"' in response.text
    assert 'name="email"' in response.text
    assert 'name="phone"' not in response.text


def test_form_submit_valid_data() -> None:
    """Test form submission with valid data"""
    client = TestClient(app)
    response = client.post(
        "/submit",
        data={"name": "Audrey", "email": "audreyfeldroy@example.com"},
    )
    assert response.status_code == 200
    assert "Success" in response.text
    assert "Audrey" in response.text
    assert "audreyfeldroy@example.com" in response.text


def test_form_submit_invalid_data() -> None:
    """Test form submission with missing required field"""
    client = TestClient(app)
    response = client.post("/submit", data={})
    assert response.status_code == 200
    assert "Error" in response.text
    assert "Errors:" in response.text
