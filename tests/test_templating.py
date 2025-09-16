import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import air
from air import Air, JinjaRenderer

from .components import index as index_callable  # pyrefly: ignore


def test_JinjaRenderer():
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

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
    assert response.text == "<html>\n<title>Test Page</title>\n<h1>Hello, World!</h1>\n</html>"


def test_JinjaRenderer_no_context():
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_JinjaRenderer_with_Air():
    """Test the JinjaRenderer class with air.Air."""
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request):
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_JinjaRenderer_with_kwargs():
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

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
    assert response.text == "<html>\n<title>Test Page</title>\n<h1>Hello, World!</h1>\n</html>"


def test_jinja_plus_airtags():
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

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


def test_jinja_plus_airtags_autorender():
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request):
        return jinja(
            request,
            name="jinja_airtags.html",
            title="Jinja+Air Tags",
            content=air.Main(air.P("Air Tags work great with Jinja")),
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert (
        response.text
        == """<html>\n    <head>\n        <title>Jinja+Air Tags</title>\n    </head>\n    <body>\n        <h1>Jinja+Air Tags</h1>\n        <main><p>Air Tags work great with Jinja</p></main>\n    </body>\n</html>"""
    )


def test_JinjaRenderer_with_context_processors():
    """Test JinjaRenderer with context_processors parameter"""

    def add_globals(request):
        return {"global_var": "test_value"}

    jinja = JinjaRenderer(directory="tests/templates", context_processors=[add_globals])

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_JinjaRenderer_with_env():
    """Test JinjaRenderer with custom env parameter"""
    import jinja2

    # Create environment with loader since we can't pass directory and env together
    from jinja2 import FileSystemLoader

    env = jinja2.Environment(loader=FileSystemLoader("tests/templates"))
    jinja = JinjaRenderer(directory=None, env=env)

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_Renderer():
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def jinja(request: Request):
        return render(
            name="home.html",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    @app.page
    def airtag(request: Request):
        return render(
            name=".components.index",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    client = TestClient(app)

    response = client.get("/jinja")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title>Test Page</title>\n<h1>Hello, World!</h1>\n</html>"

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><title>Test Page</title><h1>Hello, World!</h1></html>"


def test_Renderer_without_request_for_components():
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def airtag(request: Request):
        return render(
            name=".components.index",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    client = TestClient(app)

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><title>Test Page</title><h1>Hello, World!</h1></html>"


def test_renderer_with_installed_package_and_children():
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="air")

    @app.page
    def airtag(request: Request):
        return render(
            ".layouts.mvpcss",
            air.Title("Test Page"),
            air.H1("Hello, World"),
            request=request,
        )

    @app.page
    def airtag_without_request():
        return render(".layouts.mvpcss", air.Title("Test Page"), air.H1("Hello, World"))

    client = TestClient(app)

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet" /><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm" crossorigin="anonymous"></script><title>Test Page</title></head><body><main><h1>Hello, World</h1></main></body></html>'
    )

    response = client.get("/airtag-without-request")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet" /><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm" crossorigin="anonymous"></script><title>Test Page</title></head><body><main><h1>Hello, World</h1></main></body></html>'
    )


def test_render_with_callable():
    """Test the Renderer class with callable."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="air")

    @app.page
    def layout(request: Request):
        return render(air.layouts.mvpcss, air.Title("Test Page"), air.H1("Hello, World"))

    @app.page
    def component(request: Request):
        return render(index_callable, title="Test Page", content="Hello, World!")

    client = TestClient(app)

    response = client.get("/layout")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet" /><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm" crossorigin="anonymous"></script></head><body><main></main></body></html>'
    )

    response = client.get("/component")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><title>Test Page</title><h1>Hello, World!</h1></html>"


def test_render_failing_name():
    render = air.Renderer(directory="tests/templates", package="air")

    with pytest.raises(air.RenderException):
        render(name="dummy")


def test_render_callable_wrong_type():
    render = air.Renderer(directory="tests/templates")

    def wrong_type():
        return 5

    with pytest.raises(TypeError):
        render(wrong_type)
