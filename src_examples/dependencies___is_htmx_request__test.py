from fastapi.testclient import TestClient

from .dependencies___is_htmx_request import app


def test_is_htmx_get_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.get("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_get_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"


def test_is_htmx_post_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.post("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_post_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.post("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"


def test_is_htmx_patch_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.patch("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_patch_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.patch("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"


def test_is_htmx_put_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.put("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_put_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.put("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"


def test_is_htmx_delete_request_with_htmx_header() -> None:
    client = TestClient(app)

    response = client.delete("/", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: True</h1>"


def test_is_htmx_delete_request_without_htmx_header() -> None:
    client = TestClient(app)

    response = client.delete("/")
    assert response.status_code == 200
    assert response.text == "<h1>Is HTMX request?: False</h1>"
