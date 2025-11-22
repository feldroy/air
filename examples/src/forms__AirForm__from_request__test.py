from fastapi.testclient import TestClient

from .forms__AirForm__from_request import app


def test_from_request_with_valid_data() -> None:
    """Test from_request method with valid form data"""
    client = TestClient(app)
    response = client.post("/flight", data={"flight_number": "AA123", "destination": "New York"})
    assert response.status_code == 200
    assert "Flight Submitted" in response.text
    assert "AA123" in response.text
    assert "New York" in response.text


def test_from_request_with_invalid_data() -> None:
    """Test from_request method with invalid form data"""
    client = TestClient(app)
    response = client.post("/flight", data={"flight_number": "AA123"})  # Missing destination
    assert response.status_code == 200
    assert "Validation Failed" in response.text
    assert "Errors: 1" in response.text


def test_from_request_with_empty_data() -> None:
    """Test from_request method with empty form data"""
    client = TestClient(app)
    response = client.post("/flight", data={})
    assert response.status_code == 200
    assert "Validation Failed" in response.text
    assert "Errors: 2" in response.text
