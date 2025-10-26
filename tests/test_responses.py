from typing import Any

from fastapi.testclient import TestClient

import air
from air import H1, AirResponse, Article, Body, Div, Html, Main


def test_TagResponse_obj() -> None:
    """Test the TagResponse class."""
    app = air.Air()

    @app.get("/test")
    def test_endpoint() -> AirResponse:
        return air.TagResponse(air.H1("Hello, World!"))

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_TagResponse_compatibility() -> None:
    """Test for non-proxied TagResponse that should still work if used directly."""
    # import to check backward compatibility
    from air.responses import TagResponse

    app = air.Air()

    @app.get("/test_tag", response_class=TagResponse)
    def test_tag_endpoint() -> Div:
        return air.Div(air.H1("Hi from TagResponse!"), air.Br())

    client = TestClient(app)

    response = client.get("/test_tag")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<div><h1>Hi from TagResponse!</h1><br></div>"


def test_AirResponse() -> None:
    """Test the AirResponse class."""
    app = air.Air()

    @app.get("/test_tag", response_class=air.AirResponse)
    def test_tag_endpoint() -> H1:
        return air.H1("Hello, World!")

    @app.get("/test_html", response_class=air.AirResponse)
    def test_html_endpoint() -> str:
        return "<h1>Hello, World!</h1>"

    client = TestClient(app)
    response = client.get("/test_tag")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"

    response = client.get("/test_html")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Hello, World!</h1>"


def test_AirResponse_type() -> None:
    """Test the AirResponse class."""

    app = air.Air()

    @app.get("/test", response_class=air.AirResponse)
    def test_endpoint() -> Main:
        return air.Main(
            air.H1("Hello, clean HTML response!"),
            air.P("This is a paragraph in the response."),
        )

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text == "<main><h1>Hello, clean HTML response!</h1><p>This is a paragraph in the response.</p></main>"
    )


def test_AirResponse_html() -> None:
    """Test the AirResponse class."""

    app = air.Air()

    @app.get("/test", response_class=air.AirResponse)
    def test_endpoint() -> Html:
        return air.Html(
            air.Head(),
            air.Body(
                air.Main(
                    air.H1("Hello, clean HTML response!"),
                    air.P("This is a paragraph in the response."),
                )
            ),
        )

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == "<!doctype html><html><head></head><body><main><h1>Hello, clean HTML response!</h1><p>This is a paragraph in the response.</p></main></body></html>"
    )


def test_strings_and_tag_children() -> None:
    app = air.Air()

    @app.get("/test", response_class=air.AirResponse)
    def test_endpoint() -> Html:
        return air.Html(air.Body(air.P("This isn't a ", air.Strong("cut off"), " sentence")))

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == "<!doctype html><html><body><p>This isn&#x27;t a <strong>cut off</strong> sentence</p></body></html>"
    )


def test_custom_name_in_response() -> None:
    app = air.Air()

    def Card(sentence: str) -> Article:
        return air.Article(air.Header("Header"), sentence, air.Footer("Footer"))

    @app.get("/test", response_class=air.AirResponse)
    def test_endpoint() -> Article:
        return Card("This is a sentence")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<article><header>Header</header>This is a sentence<footer>Footer</footer></article>"


def test_AirResponse_with_layout_strings() -> None:
    class CustomLayoutResponse(air.AirResponse):
        def render(self, content: Any) -> bytes:
            content = super().render(content)
            return f"<html><body><h1>Custom Layout</h1>{content}</body></html>".encode()

    app = air.Air()

    @app.get("/test", response_class=CustomLayoutResponse)
    def test_endpoint() -> Main:
        return air.Main(air.H2("Hello, World!"))

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<html><body><h1>Custom Layout</h1>b'<main><h2>Hello, World!</h2></main>'</body></html>"


def test_AirResponse_with_layout_names() -> None:
    class CustomLayoutResponse(air.AirResponse):
        def render(self, content: Any) -> bytes:
            content = super().render(content).decode("utf-8")
            return air.Html(air.Raw(content)).render().encode("utf-8")

    app = air.Air()

    @app.get("/test", response_class=CustomLayoutResponse)
    def test_endpoint() -> Body:
        return air.Body(air.Main(air.H1("Hello, World!")))

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><body><main><h1>Hello, World!</h1></main></body></html>"


def test_SSEResponse() -> None:
    """Test the SSEResponse class."""
    app = air.Air()

    async def event_generator():
        yield air.P("Hello")
        yield air.P("World")

    @app.get("/test")
    async def test_endpoint():
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == "event: message\ndata: <p>Hello</p>\n\nevent: message\ndata: <p>World</p>\n\n"


def test_SSEResponse_multiline_tag_content() -> None:
    """Test the SSEResponse class."""
    app = air.Air()

    async def event_generator():
        yield air.P("Hello\nWorld")
        yield air.P("World\nHello")

    @app.get("/test")
    async def test_endpoint():
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert (
        response.text
        == "event: message\ndata: <p>Hello\ndata: World</p>\n\nevent: message\ndata: <p>World\ndata: Hello</p>\n\n"
    )


def test_SSEResponse_string_content() -> None:
    app = air.Air()

    async def event_generator():
        yield "Hello\nWorld"
        yield "Air is cool\nTry it out!"

    @app.get("/test")
    async def test_endpoint():
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert (
        response.text
        == "event: message\ndata: Hello\ndata: World\n\nevent: message\ndata: Air is cool\ndata: Try it out!\n\n"
    )


def test_SSEResponse_bytes_content() -> None:
    app = air.Air()

    async def event_generator():
        yield b"already encoded"

    @app.get("/test")
    async def test_endpoint():
        return air.SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/test")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == "already encoded"


def test_RedirectResponse() -> None:
    """Test the RedirectResponse class."""
    app = air.Air()

    @app.get("/test2")
    async def another_test_endpoint():
        return air.AirResponse()

    @app.get("/test")
    async def test_endpoint():
        return air.RedirectResponse("/test2")

    client = TestClient(app)
    response = client.get("/test", follow_redirects=False)
    assert response.status_code == 303

    # check if redirect works
    response = client.get("/test", follow_redirects=True)
    assert response.status_code == 200
    assert "/test2" in response.url.path
