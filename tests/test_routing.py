import pytest
from fastapi.testclient import TestClient

import air


def test_air_routing():
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index():
        return air.H1("Hello, World!")

    @router.page
    def home():
        return air.H1("Hello, Air!")

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"

    response = client.get("/home")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, Air!</h1>"


def test_air_routing_prefix():
    app = air.Air()

    router = air.AirRouter()

    @app.page
    def index():
        return air.H1("Hello, World!")

    @router.page
    def home():
        return air.H1("Hello, Air!")

    with pytest.raises(AssertionError):
        app.include_router(router, prefix="/")
