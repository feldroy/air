"""Tests for AirForm example."""

from fastapi.testclient import TestClient

from examples.src.forms__AirForm import app

client = TestClient(app)


def test_flight_form_valid():
    """Test flight form with valid data."""
    response = client.post("/flight", data={"flight_number": "AA123", "destination": "LAX"})
    assert response.status_code == 200
    assert "AA123" in response.text


def test_flight_form_invalid():
    """Test flight form with missing data."""
    response = client.post("/flight", data={})
    assert response.status_code == 200
    assert "2" in response.text


def test_flight_form_depends_valid():
    """Test flight form with dependency injection."""
    response = client.post("/flight-depends", data={"flight_number": "UA456", "destination": "SFO"})
    assert response.status_code == 200
    assert "UA456" in response.text
