from fastapi.testclient import TestClient

from .applications__Air__page import app


def test_page_routes() -> None:
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>I am the home page</h1>"

    response = client.get("/data")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>I am the data page</h1>"

    response = client.get("/about-us")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>I am the about page</h1>"
