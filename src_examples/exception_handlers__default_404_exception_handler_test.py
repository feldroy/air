from fastapi.testclient import TestClient

from .dependencies___is_htmx_request import app

def test_exception_handling_404() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 404
    assert response.text == "<h1>404 Not Found</h1>"