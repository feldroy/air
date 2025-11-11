from fastapi.testclient import TestClient

from .exception_handlers__default_404_exception_handler import app


def test_exception_handling_404() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 404
    assert response.text == "<p>404 Not Found</p>"
