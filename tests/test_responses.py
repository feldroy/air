from collections.abc import AsyncGenerator
from typing import override

from fastapi import status
from fastapi.testclient import TestClient

import air
from air import H1, AirResponse, Article, BaseTag, Div, Html, Main
from air.responses import TagResponse

from .utils import clean_doc


class CustomLayoutResponse(air.AirResponse):
    @override
    def render(self, tag: BaseTag | str) -> bytes | memoryview:  # ty: ignore[invalid-method-override]
        return super().render(air.Html(air.Body(tag)))


def test_tag_response_obj() -> None:
    """Test the TagResponse class."""
    app = air.Air()

    @app.get("/tag-response")
    def tag_response() -> AirResponse:
        return air.TagResponse(air.H1("Hello, World!"))

    client = TestClient(app)
    response = client.get("/tag-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_tag_response_compatibility() -> None:
    """Test for non-proxied TagResponse that should still work if used directly."""
    # import to check backward compatibility

    app = air.Air()

    @app.get("/non-proxied-tag-response", response_class=TagResponse)
    def non_proxied_tag_response() -> Div:
        return air.Div(air.H1("Hi from TagResponse!"), air.Br())

    client = TestClient(app)

    response = client.get("/non-proxied-tag-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<div><h1>Hi from TagResponse!</h1><br></div>"


def test_air_response() -> None:
    """Test the AirResponse class."""
    app = air.Air()

    @app.get("/tag-page", response_class=air.AirResponse)
    def tag_page() -> H1:
        return air.H1("Hello, World!")

    @app.get("/html-page", response_class=air.AirResponse)
    def html_page() -> str:
        return "<h1>Hello, World!</h1>"

    client = TestClient(app)
    response = client.get("/tag-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"

    response = client.get("/html-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_air_response_type() -> None:
    """Test the AirResponse class."""

    app = air.Air()

    @app.get("/tag-page", response_class=air.AirResponse)
    def tag_page() -> Main:
        return air.Main(
            air.H1("Hello, clean HTML response!"),
            air.P("This is a paragraph in the response."),
        )

    client = TestClient(app)
    response = client.get("/tag-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text == "<main><h1>Hello, clean HTML response!</h1><p>This is a paragraph in the response.</p></main>"
    )


def test_air_response_html() -> None:
    """Test the AirResponse class."""

    app = air.Air()

    @app.get("/tag-page", response_class=air.AirResponse)
    def tag_page() -> str:
        return air.Html(
            air.Head(),
            air.Body(
                air.Main(
                    air.H1("Hello, clean HTML response!"),
                    air.P("This is a paragraph in the response."),
                )
            ),
        ).pretty_render()

    client = TestClient(app)
    response = client.get("/tag-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    expected_html = clean_doc(
        """
        <!doctype html>
        <html>
          <head></head>
          <body>
            <main>
              <h1>Hello, clean HTML response!</h1>
              <p>This is a paragraph in the response.</p>
            </main>
          </body>
        </html>
        """
    )
    actual_html = response.text
    assert actual_html == expected_html


def test_strings_and_tag_children() -> None:
    app = air.Air()

    @app.get("/tag-page", response_class=air.AirResponse)
    def tag_page() -> Html:
        return air.Html(air.Body(air.P("This isn't a ", air.Strong("cut off"), " sentence")))

    client = TestClient(app)
    response = client.get("/tag-page")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == "<!doctype html><html><body><p>This isn&#x27;t a <strong>cut off</strong> sentence</p></body></html>"
    )


def test_custom_name_in_response() -> None:
    app = air.Air()

    def card(sentence: str) -> Article:
        return air.Article(air.Header("Header"), sentence, air.Footer("Footer"))

    @app.get("/tag-page", response_class=air.AirResponse)
    def tag_page() -> Article:
        return card("This is a sentence")

    client = TestClient(app)
    response = client.get("/tag-page")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<article><header>Header</header>This is a sentence<footer>Footer</footer></article>"


def test_air_response_with_layout_strings() -> None:
    app = air.Air()

    @app.get("/tag-page", response_class=CustomLayoutResponse)
    def tag_page() -> Main:
        return air.Main(air.H2("Hello, World!"))

    client = TestClient(app)
    response = client.get("/tag-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><body><main><h2>Hello, World!</h2></main></body></html>"


def test_air_response_with_layout_names() -> None:
    app = air.Air()

    @app.get("/tag-page", response_class=CustomLayoutResponse)
    def tag_page() -> air.Main:
        return air.Main(air.H1("Hello, World!"))

    client = TestClient(app)
    response = client.get("/tag-page")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><body><main><h1>Hello, World!</h1></main></body></html>"


def test_sse_response() -> None:
    """Test the SSEResponse class."""
    app = air.Air()

    async def event_generator() -> AsyncGenerator[air.P]:
        yield air.P("Hello")
        yield air.P("World")

    @app.get("/sse-response")
    async def sse_response() -> air.SSEResponse:
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/sse-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == "event: message\ndata: <p>Hello</p>\n\nevent: message\ndata: <p>World</p>\n\n"


def test_sse_response_multiline_tag_content() -> None:
    """Test the SSEResponse class."""
    app = air.Air()

    async def event_generator() -> AsyncGenerator[air.P]:
        yield air.P("Hello\nWorld")
        yield air.P("World\nHello")

    @app.get("/sse-response")
    async def sse_response() -> air.SSEResponse:
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/sse-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert (
        response.text
        == "event: message\ndata: <p>Hello\ndata: World</p>\n\nevent: message\ndata: <p>World\ndata: Hello</p>\n\n"
    )


def test_sse_response_string_content() -> None:
    app = air.Air()

    async def event_generator() -> AsyncGenerator[str]:
        yield "Hello\nWorld"
        yield "Air is cool\nTry it out!"

    @app.get("/sse-response")
    async def sse_response() -> air.SSEResponse:
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/sse-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert (
        response.text
        == "event: message\ndata: Hello\ndata: World\n\nevent: message\ndata: Air is cool\ndata: Try it out!\n\n"
    )


def test_sse_response_bytes_content() -> None:
    app = air.Air()

    async def event_generator() -> AsyncGenerator[bytes]:
        yield b"already encoded"

    @app.get("/sse-response")
    async def sse_response() -> air.SSEResponse:
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/sse-response")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == "already encoded"


def test_redirect_response() -> None:
    """Test the RedirectResponse class."""
    app = air.Air()

    @app.get("/air-response")
    async def air_response() -> air.AirResponse:
        return air.AirResponse()

    @app.get("/redirect-response")
    async def redirect_response() -> air.RedirectResponse:
        return air.RedirectResponse("/air-response")

    client = TestClient(app)
    response = client.get("/redirect-response", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    # check if redirect works
    response = client.get("/redirect-response", follow_redirects=True)
    assert response.status_code == 200
    assert "/air-response" in response.url.path
