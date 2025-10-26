from fastapi.testclient import TestClient

from .exception_handlers__default_500_exception_handler import app

def test_exception_handling_500() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 500
    assert response.text == "<p>500 Internal Server Error</p>"