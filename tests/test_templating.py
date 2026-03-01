import sys
import types
from unittest.mock import Mock

import jinja2
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from full_match import match as full_match
from jinja2 import FileSystemLoader
from starlette.datastructures import URL
from starlette.responses import HTMLResponse

import air
from air import Air, JinjaRenderer, Request

from .components import index as index_callable
from .utils import clean_doc, clean_doc_with_broken_lines


def test_jinja_renderer() -> None:
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
        return jinja(
            request,
            name="home.html",
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n  <title>Test Page</title>\n  <h1>Hello, World!</h1>\n</html>"


def test_jinja_renderer_no_context() -> None:
    """Test the JinjaRenderer class."""
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n  <title></title>\n  <h1></h1>\n</html>"


def test_jinja_renderer_with_air() -> None:
    """Test the JinjaRenderer class with air.Air."""
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
        return jinja(request, name="home.html")

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n  <title></title>\n  <h1></h1>\n</html>"


def test_jinja_renderer_with_kwargs() -> None:
    app = FastAPI()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/test")
    def page(request: Request) -> HTMLResponse:
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
    assert response.text == "<html>\n  <title>Test Page</title>\n  <h1>Hello, World!</h1>\n</html>"


def test_jinja_plus_airtags() -> None:
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request) -> HTMLResponse:
        return jinja(
            request,
            name="jinja_airtags.html",
            title="Jinja+Air Tags",
            content=air.Main(air.P("Air Tags work great with Jinja")).render(),
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    actual_html = response.text
    expected_html = clean_doc(
        """
        <html>
          <head>
            <title>Jinja+Air Tags</title>
          </head>
          <body>
            <h1>Jinja+Air Tags</h1>
            <main><p>Air Tags work great with Jinja</p></main>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html.rstrip()


def test_jinja_plus_airtags_autorender() -> None:
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request) -> HTMLResponse:
        return jinja(
            request,
            name="jinja_airtags.html",
            title="Jinja+Air Tags",
            content=air.Main(air.P("Air Tags work great with Jinja")),
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    actual_html = response.text
    expected_html = clean_doc(
        """
        <html>
          <head>
            <title>Jinja+Air Tags</title>
          </head>
          <body>
            <h1>Jinja+Air Tags</h1>
            <main><p>Air Tags work great with Jinja</p></main>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html.rstrip()


def test_jinja_renderer_with_context_processors() -> None:
    """Test JinjaRenderer with context_processors parameter"""

    def add_globals(request: Request) -> dict[str, str]:
        return {"global_var": "test_value"}

    jinja = JinjaRenderer(directory="tests/templates", context_processors=[add_globals])

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_jinja_renderer_with_env() -> None:
    """Test JinjaRenderer with custom env parameter"""

    # Create environment with loader since we can't pass directory and env together
    env = jinja2.Environment(loader=FileSystemLoader("tests/templates"))
    jinja = JinjaRenderer(directory=None, env=env)

    # Just test that it initializes correctly
    assert jinja.templates is not None


def test_jinja_csrf_helpers_render_token_and_hidden_input() -> None:
    app = Air()
    app.add_middleware(air.CSRFMiddleware)
    jinja = JinjaRenderer(directory="tests/templates")

    @app.get("/form")
    def form(request: Request) -> HTMLResponse:
        return jinja(request, name="csrf_form.html")

    client = TestClient(app)
    response = client.get("/form")

    assert response.status_code == 200
    token = response.cookies.get("air_csrf_token")
    assert token is not None
    assert f'name="csrf_token" value="{token}"' in response.text
    assert f'<p id="token">{token}</p>' in response.text


def test_renderer() -> None:
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def jinja(request: Request) -> str | HTMLResponse:
        return render(
            name="home.html",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    @app.page
    def airtag(request: Request) -> str | HTMLResponse:
        return render(
            name=".components.index",
            request=request,
            context={"title": "Test Page", "content": "Hello, World!"},
        )

    client = TestClient(app)

    response = client.get("/jinja")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html>\n  <title>Test Page</title>\n  <h1>Hello, World!</h1>\n</html>"

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><title>Test Page</title><h1>Hello, World!</h1></html>"


def test_renderer_without_request_for_components() -> None:
    """Test the Renderer class."""
    app = air.Air()

    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def airtag(request: Request) -> str | HTMLResponse:
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
    def airtag(request: Request) -> str | HTMLResponse:
        return render(
            ".layouts.mvpcss",
            air.Title("Test Page"),
            air.H1("Hello, World"),
            request=request,
        )

    @app.page
    def airtag_without_request() -> str | HTMLResponse:
        return render(".layouts.mvpcss", air.Title("Test Page"), air.H1("Hello, World"))

    client = TestClient(app)

    response = client.get("/airtag")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    actual_html = response.text
    expected_html = clean_doc_with_broken_lines(
        r"""
        <!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet"><style>footer, header,\
            main { padding: 1rem; } nav {margin-bottom: 1rem;}</style><script\
            src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous"\
            integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script><title>Test\
            Page</title></head><body><main><h1>Hello, World</h1></main></body></html>
        """
    )
    assert actual_html == expected_html.rstrip()

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
    def layout(request: Request) -> str | HTMLResponse:
        return render(air.layouts.mvpcss, air.Title("Test Page"), air.H1("Hello, World"))

    @app.page
    def component(request: Request) -> str | HTMLResponse:
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

    with pytest.raises(
        ValueError,
        match=full_match("No callable or Jinja template found."),
    ):
        render(name="dummy")


def test_render_callable_wrong_type() -> None:
    render = air.Renderer(directory="tests/templates")

    def wrong_type() -> int:
        return 5

    with pytest.raises(TypeError):
        render(wrong_type)


def test_renderer_with_context_processors() -> None:
    """Test Renderer with context_processors parameter to cover the else branch"""

    def add_globals(request: Request) -> dict[str, str]:
        return {"global_var": "test_value"}

    render = air.Renderer(directory="tests/templates", context_processors=[add_globals])

    # Just test that it initializes correctly
    assert render.templates is not None


def test_renderer_render_template_with_air_tags() -> None:
    """Test _render_template method with Air Tags in context"""
    app = air.Air()
    render = air.Renderer(directory="tests/templates")

    @app.page
    def context_with_tags(request: Request) -> str | HTMLResponse:
        return render(
            name="home.html",
            request=request,
            context={"title": "Test", "content": air.P("Test content")},
        )

    client = TestClient(app)
    response = client.get("/context-with-tags")

    assert response.status_code == 200
    assert "Test content" in response.text


def test_renderer_tag_callable_with_both_args_and_context() -> None:
    """Test case where filtered_context and args are both truthy"""
    app = air.Air()
    render = air.Renderer(directory="tests/templates", package="tests")

    # Function that can be called with only keyword args to test the specific line 205
    def callable_function(title: str | None = None) -> str:
        return f"<p>{title}</p>"

    # Create a test module to simulate the import
    test_module = types.ModuleType("test_module")
    test_module.test_func = callable_function
    sys.modules["tests.test_module"] = test_module

    @app.page
    def page(request: Request) -> str | HTMLResponse:
        return render(
            ".test_module.test_func",
            "Hello",  # This is args - will be ignored due to line 205 behavior
            request=request,
            title="World",  # This goes to filtered_context
        )

    client = TestClient(app)
    response = client.get("/page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<p>World</p>" in response.text

    # Clean up the module
    del sys.modules["tests.test_module"]


def test_renderer_import_module_fallback() -> None:
    """Test the ModuleNotFoundError fallback in _import_module"""
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


def test_renderer_filter_context_with_request() -> None:
    """Test _filter_context_for_callable when callable expects request parameter"""
    render = air.Renderer(directory="tests/templates")

    def callable_function(request: Request, title: str) -> str:
        return f"<p>{title}</p>"

    context = {"title": "Test", "extra": "ignored"}
    request = Request({"type": "http", "method": "GET", "path": "/"})

    filtered = render._filter_context_for_callable(callable_function, context, request)

    assert "title" in filtered
    assert "request" in filtered
    assert "extra" not in filtered
    assert filtered["request"] is request
    assert filtered["title"] == "Test"


def test_jinja_renderer_only_stringifies_tags_by_default() -> None:
    app = air.Air()
    render = air.Renderer(directory="tests/templates", package="tests")

    @app.page
    def page(request: Request) -> str | HTMLResponse:
        return render(
            name="lists_and_dicts.html",
            request=request,
            title="World",  # This goes to filtered_context
            meta={"title": "Lists and Dicts"},
            items=["One", "Two", "Three"],
        )

    client = TestClient(app)
    response = client.get("/page")

    assert "<h1>Lists and Dicts</h1>" in response.text
    assert "<li>One</li>" in response.text
    assert "<li>Two</li>" in response.text
    assert "<li>Three</li>" in response.text


def test_jinja_renderer_as_string_returns_safestr() -> None:
    """Test that as_string=True returns a SafeStr."""
    jinja = JinjaRenderer(directory="tests/templates")
    mock_request = Mock(spec=Request)
    mock_request.url = URL("http://localhost/test")

    result = jinja(
        mock_request,
        name="jinja_airtags.html",
        title="Test Title",
        content="<p>Test content</p>",
        as_string=True,
    )

    assert isinstance(result, air.SafeStr)
    assert "<h1>Test Title</h1>" in result
    assert "<p>Test content</p>" in result


def test_jinja_renderer_as_string_false_returns_html_response() -> None:
    """Test that as_string=False (default) returns HTMLResponse."""
    jinja = JinjaRenderer(directory="tests/templates")
    mock_request = Mock(spec=Request)
    mock_request.url = URL("http://localhost/test")

    result = jinja(
        mock_request,
        name="jinja_airtags.html",
        title="Test Title",
        content="<p>Test content</p>",
        as_string=False,
    )

    assert isinstance(result, HTMLResponse)


def test_jinja_renderer_as_string_embedded_in_airtags() -> None:
    """Test that SafeStr from as_string=True can be embedded in AirTags."""
    app = Air()

    jinja = JinjaRenderer(directory="tests/templates")

    @app.page
    def index(request: Request) -> air.BaseTag:
        jinja_content = jinja(
            request,
            name="jinja_airtags.html",
            title="Embedded Jinja",
            content="<p>Hello from Jinja</p>",
            as_string=True,
        )
        return air.layouts.mvpcss(
            air.Title("Wrapper Page"),
            jinja_content,
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Embedded Jinja</h1>" in response.text
    assert "<p>Hello from Jinja</p>" in response.text
    assert "<title>Wrapper Page</title>" in response.text
