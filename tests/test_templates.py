from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from air import Air, Jinja2Renderer


def test_Jinja2Renderer():
    """Test the Jinja2Renderer class."""
    app = FastAPI()

    jinja = Jinja2Renderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(
            request,
            name="home.html",
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == "<html>\n<title>Test Page</title>\n<h1>Hello, World!</h1>\n</html>"
    )


def test_Jinja2Renderer_no_context():
    """Test the Jinja2Renderer class."""
    app = FastAPI()

    jinja = Jinja2Renderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_Jinja2Renderer_with_Air():
    """Test the Jinja2Renderer class with air.Air."""
    app = Air()

    jinja = Jinja2Renderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_Jinja2Renderer_with_kwargs():
    app = FastAPI()

    jinja = Jinja2Renderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(
            request,
            name="home.html",
            context={"title": "Test Page"},
            content="Hello, World!",  # This gets added to the context
        )

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == "<html>\n<title>Test Page</title>\n<h1>Hello, World!</h1>\n</html>"
    )
