from fastapi.testclient import TestClient

from .dependencies___is_htmx_request import app


def test_is_htmx_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.get("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"
