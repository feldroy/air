import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.templating import _TemplateResponse

import air
from air import Air, JinjaRenderer, Request

from .components import index as index_callable  # pyrefly: ignore


def test_JinjaRenderer() -> None:
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request) -> _TemplateResponse:
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


def test_JinjaRenderer_no_context() -> None:
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request) -> _TemplateResponse:
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_JinjaRenderer_with_Air() -> None:
    """Test the JinjaRenderer class with air.Air."""
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request) -> _TemplateResponse:
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n<title></title>\n<h1></h1>\n</html>"


def test_JinjaRenderer_with_kwargs() -> None:
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def test_endpoint(request: Request) -> _TemplateResponse:
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


def test_jinja_plus_airtags() -> None:
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request) -> _TemplateResponse:
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


def test_jinja_plus_airtags_autorender() -> None:
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request) -> _TemplateResponse:
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


def test_JinjaRenderer_with_context_processors() -> None:
    """Test JinjaRenderer with context_processors parameter"""

    def add_globals(request: Request) -> dict[str, str]:
        return {"global_var": "test_value"}

    jinja = JinjaRenderer(directory="tests/templates", context_processors=[add_globals])

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_JinjaRenderer_with_env() -> None:
    """Test JinjaRenderer with custom env parameter"""
    import jinja2

    # Create environment with loader since we can't pass directory and env together
    from jinja2 import FileSystemLoader

    env = jinja2.Environment(loader=FileSystemLoader("tests/templates"))
    jinja = JinjaRenderer(directory=None, env=env)

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_Renderer() -> None:
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def jinja(request: Request) -> str:
        return render(
            name="home.html",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    @app.page
    def airtag(request: Request) -> str:
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


def test_Renderer_without_request_for_components() -> None:
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def airtag(request: Request) -> str:
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


def test_renderer_with_installed_package_and_children() -> None:
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="air")

    @app.page
    def airtag(request: Request) -> str:
        return render(
            ".layouts.mvpcss",
            air.Title("Test Page"),
            air.H1("Hello, World"),
            request=request,
        )

    @app.page
    def airtag_without_request() -> str:
        return render(".layouts.mvpcss", air.Title("Test Page"), air.H1("Hello, World"))

    client = TestClient(app)

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet"><style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script><title>Test Page</title></head><body><main><h1>Hello, World</h1></main></body></html>'
    )

    response = client.get("/airtag-without-request")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        "</script><title>Test Page</title></head><body><main><h1>Hello, World</h1></main></body></html>"
        in response.text
    )


def test_render_with_callable() -> None:
    """Test the Renderer class with callable."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="air")

    @app.page
    def layout(request: Request) -> str:
        return render(air.layouts.mvpcss, air.Title("Test Page"), air.H1("Hello, World"))

    @app.page
    def component(request: Request) -> str:
        return render(index_callable, title="Test Page", content="Hello, World!")

    client = TestClient(app)

    response = client.get("/layout")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "</script></head><body><main></main></body></html>" in response.text

    response = client.get("/component")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><title>Test Page</title><h1>Hello, World!</h1></html>"


def test_render_failing_name() -> None:
    render = air.Renderer(directory="tests/templates", package="air")

    with pytest.raises(air.RenderException):
        render(name="dummy")


def test_render_callable_wrong_type() -> None:
    render = air.Renderer(directory="tests/templates")

    def wrong_type() -> int:
        return 5

    with pytest.raises(TypeError):
        render(wrong_type)


def test_Renderer_with_context_processors() -> None:
    """Test Renderer with context_processors parameter to cover the else branch"""

    def add_globals(request: Request) -> dict[str, str]:
        return {"global_var": "test_value"}

    render = air.Renderer(directory="tests/templates", context_processors=[add_globals])

    # Just test that it initializes correctly
    assert render.templates is not None


def test_Renderer_render_template_with_air_tags() -> None:
    """Test _render_template method with Air Tags in context"""
    app = air.Air()
    render = air.Renderer(directory="tests/templates")

    @app.page
    def test_with_tags(request: Request) -> str:
        return render(
            name="home.html",
            request=request,
            context={"title": "Test", "content": air.P("Test content")},
        )

    client = TestClient(app)
    response = client.get("/test-with-tags")

    assert response.status_code == 200
    assert "Test content" in response.text


def test_Renderer_tag_callable_with_both_args_and_context() -> None:
    """Test case where filtered_context and args are both truthy"""
    app = air.Air()
    render = air.Renderer(directory="tests/templates", package="tests")

    # Function that can be called with only keyword args to test the specific line 205
    def test_callable(title: str | None = None) -> str:
        return f"<p>{title}</p>"

    # Create a test module to simulate the import
    import sys
    import types

    test_module = types.ModuleType("test_module")
    test_module.test_func = test_callable
    sys.modules["tests.test_module"] = test_module

    @app.page
    def test_page(request: Request) -> str:
        return render(
            ".test_module.test_func",
            "Hello",  # This is args - will be ignored due to line 205 behavior
            request=request,
            title="World",  # This goes to filtered_context
        )

    client = TestClient(app)
    response = client.get("/test-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<p>World</p>" in response.text

    # Clean up the module
    del sys.modules["tests.test_module"]


def test_Renderer_import_module_fallback() -> None:
    """Test the ModuleNotFoundError fallback in _import_module"""
    import sys
    import types

    # Create a mock module that exists as a relative import but not absolute
    mock_module = types.ModuleType("mock_module")
    mock_module.test_func = lambda: "test"
    sys.modules["tests.mock_module"] = mock_module

    try:
        render = air.Renderer(directory="tests/templates", package="tests")

        # This should use the fallback path: try absolute import (fail), then relative import (succeed)
        result_module = render._import_module("mock_module")
        assert result_module is mock_module
    finally:
        # Clean up
        if "tests.mock_module" in sys.modules:
            del sys.modules["tests.mock_module"]


def test_Renderer_filter_context_with_request() -> None:
    """Test _filter_context_for_callable when callable expects request parameter"""
    render = air.Renderer(directory="tests/templates")

    def test_callable(request: Request, title: str) -> str:
        return f"<p>{title}</p>"

    context = {"title": "Test", "extra": "ignored"}
    request = Request({"type": "http", "method": "GET", "path": "/"})

    filtered = render._filter_context_for_callable(test_callable, context, request)

    assert "title" in filtered
    assert "request" in filtered
    assert "extra" not in filtered
    assert filtered["request"] is request
    assert filtered["title"] == "Test"


def test_jinja_renderer_only_stringifies_tags_by_default() -> None:
    app = air.Air()
    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def test_page(request: Request) -> str:
        return render(
            name="lists_and_dicts.html",
            request=request,
            title="World",  # This goes to filtered_context
            meta={"title": "Lists and Dicts"},
            items=["One", "Two", "Three"],
        )

    client = TestClient(app)
    response = client.get("/test-page")

    assert "<h1>Lists and Dicts</h1>" in response.text
    assert "<li>One</li>" in response.text
    assert "<li>Two</li>" in response.text
    assert "<li>Three</li>" in response.text
