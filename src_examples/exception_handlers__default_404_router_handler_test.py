from fastapi.testclient import TestClient

from .exception_handlers__default_404_router_handler import app

def test_default_404_router_handler() -> None:
    client = TestClient(app)
    response = client.get("/example")
    assert response.status_code == 404
    assert response.text == "<p>I am an example route.</p>"