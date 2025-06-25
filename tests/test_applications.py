from fastapi import FastAPI
from fastapi.testclient import TestClient
import air


def test_air_app_factory():
    app = air.Air()

    @app.get("/test")
    def test_endpoint():
        return air.H1("Hello, World!")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_air_plus_fastapi():
    app = FastAPI()
    html = air.Air()

    @app.get("/api")
    def test_api():
        return {"text": "hello, world"}

    @html.get("/page")
    def test_page():
        return air.H1("Hello, World!")

    # Combine into one app
    app.mount("/", html)

    client = TestClient(app)

    # Test the API
    response = client.get("/api")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"text": "hello, world"}

    # Test the page
    response = client.get("/page")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"
