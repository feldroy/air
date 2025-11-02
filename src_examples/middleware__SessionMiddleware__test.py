from fastapi.testclient import TestClient

from .middleware__SessionMiddleware import app


def test_session_persistence() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    first_timestamp = response.text
    assert "first-visited" in response.text or "<h1>" in response.text

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == first_timestamp


def test_session_reset() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    first_timestamp = response.text

    response = client.get("/reset")
    assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 200
    second_timestamp = response.text
    assert first_timestamp != second_timestamp
