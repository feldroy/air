from fastapi.testclient import TestClient

from .models__AirModel__to_form import app


def test_form_renders_with_all_parameters() -> None:
    """Test that form renders with name, includes, and widget parameters"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    # Check the form demonstrates all parameters
    assert "Contact Form" in response.text
    assert "demonstrates name, includes, and widget parameters" in response.text
    # Check custom widget styling
    assert "Custom form styling:" in response.text
    assert 'class="custom-form"' in response.text
    # Check includes parameter, only name and email fields rendered
    assert 'name="name"' in response.text
    assert 'name="email"' in response.text
    # Phone should NOT be rendered due to includes parameter
    assert 'name="phone"' not in response.text


def test_form_submit_valid_data() -> None:
    """Test form submission with valid data"""
    client = TestClient(app)
    response = client.post(
        "/submit",
        data={"name": "John Doe", "email": "john@example.com"},
    )
    assert response.status_code == 200
    assert "Success" in response.text
    assert "John Doe" in response.text
    assert "john@example.com" in response.text


def test_form_submit_invalid_data() -> None:
    """Test form submission with missing required field"""
    client = TestClient(app)
    response = client.post("/submit", data={})
    assert response.status_code == 200
    assert "Error" in response.text
    assert "Errors:" in response.text
