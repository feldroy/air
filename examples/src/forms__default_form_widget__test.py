from fastapi.testclient import TestClient

from .forms__default_form_widget import app


def test_form_renders_with_prepopulated_data() -> None:
    """Test that default_form_widget renders form with custom layout using includes"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Flight Booking" in response.text
    # Check fieldset structure
    assert "<legend>Flight Information</legend>" in response.text
    assert "<legend>Passenger Count</legend>" in response.text
    # Check pre-populated flight_number
    assert 'value="AA123"' in response.text
    # Check form has all fields
    assert 'name="flight_number"' in response.text
    assert 'name="destination"' in response.text
    assert 'name="passengers"' in response.text


def test_form_submit_with_valid_data() -> None:
    """Test form submission with valid data"""
    client = TestClient(app)
    response = client.post(
        "/submit",
        data={"flight_number": "UA456", "destination": "London", "passengers": "2"},
    )
    assert response.status_code == 200
    assert "Flight Booked" in response.text
    assert "UA456" in response.text
    assert "London" in response.text
    assert "2" in response.text


def test_form_submit_with_invalid_data() -> None:
    """Test form re-renders with custom layout and errors when data is invalid"""
    client = TestClient(app)
    response = client.post("/submit", data={"flight_number": "UA456"})  # Missing required fields
    assert response.status_code == 200
    assert "Please fix the errors" in response.text
    # Check fieldsets are preserved on error
    assert "<legend>Flight Information</legend>" in response.text
    assert "<legend>Passenger Count</legend>" in response.text
    # Check submitted data is preserved
    assert 'value="UA456"' in response.text
    # Check error indicators are present
    assert 'aria-invalid="true"' in response.text


def test_form_submit_with_empty_data() -> None:
    """Test form re-renders with errors when all fields are empty"""
    client = TestClient(app)
    response = client.post("/submit", data={})
    assert response.status_code == 200
    assert "Please fix the errors" in response.text
    assert 'aria-invalid="true"' in response.text
