from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import air
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


def test_jinja_plus_airtags():
    app = Air()

    jinja = Jinja2Renderer(directory="tests/templates")

    @app.page
    def index(request: Request):
        return jinja(
            request,
            name="jinja_airtags.html",
            title="Jinja+Air Tags",
            content=air.Main(air.P("Air Tags work great with Jinja")).render(),
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert (
        response.text
        == """<html>\n    <head>\n        <title>Jinja+Air Tags</title>\n    </head>\n    <body>\n        <h1>Jinja+Air Tags</h1>\n        <main><p>Air Tags work great with Jinja</p></main>\n    </body>\n</html>"""
    )
