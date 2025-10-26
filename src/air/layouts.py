"""Tools for building layouts and several simple layouts for quick prototyping."""

from typing import Any

from .tags import Body, Children, Head, Header, Html, Link, Main, Script, Style
from .tags.types import HEAD_TAG_TYPES, AttributesType


def filter_body_tags(tags: list[Any]) -> list:
    """Given a list of tags, only list the ones that belong in body of an HTML document."""
    return [t for t in tags if not isinstance(t, HEAD_TAG_TYPES)]


def filter_head_tags(tags: list[Any]) -> list:
    """Given a list of tags, only list the ones that belong in head of an HTML document."""
    return [t for t in tags if isinstance(t, HEAD_TAG_TYPES)]


def _header(tags: list[Any]) -> Header | str:
    """Extracts the air.Header tag from a set of tags."""
    for tag in tags:
        if isinstance(tag, Header):
            return tag
    return ""


def mvpcss(*children: Any, is_htmx: bool = False, **kwargs: AttributesType) -> Html | Children:
    """Renders the basic layout with MVP.css and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. `Header` and `Nav` tags are placed in the top of the body above the `Main` tag
    4. If `is_htmx` is True, then the layout isn't included. This is to support the `hx_boost`
        feature of HTMX

    The `mvpcss` function is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `mvpcss` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged MVP.css implementation,
        you'll have to create your own layouts.

    Args:
        children: These typically inherit from air.Tag but can be anything
        is_htmx: Whether or not HTMX sent the request from the page

    Example:

        from fastapi import Depends
        import air

        app = air.Air()


        @app.page
        async def index(is_htmx: bool = Depends(air.is_htmx_request)):
            return air.layouts.mvpcss(
                air.Title("Home"),
                air.Article(
                    air.H1("Welcome to Air"), air.P(air.A("Click to go to Dashboard", href="/dashboard")), hx_boost="true"
                ),
                is_htmx=is_htmx
            )


        @app.page
        async def dashboard(is_htmx: bool = Depends(air.is_htmx_request)):
            return air.layouts.mvpcss(
                air.Title("Dashboard"), air.Article(air.H1("Dashboard"), air.P(air.A("Go home", href="/")), hx_boost="true"),
                is_htmx=is_htmx
            )

    """
    body_tags = filter_body_tags(children)
    head_tags = filter_head_tags(children)

    if is_htmx:
        return Children(Main(*body_tags), *head_tags)

    return Html(
        Head(
            Link(rel="stylesheet", href="https://unpkg.com/mvp.css"),
            Style("footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}"),
            Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
            *head_tags,
        ),
        Body(
            _header(body_tags),
            Main(*[x for x in body_tags if not isinstance(x, Header)]),
        ),
    )


def picocss(*children: Any, is_htmx: bool = False, **kwargs: AttributesType) -> Html | Children:
    """Renders the basic layout with PicoCSS and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. If `is_htmx` is True, then the layout isn't included. This is to support the `hx_boost`
        feature of HTMX

    Note: `PicoCSS` is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `pico` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged PicoCSS implementation,
        you'll have to create your own layouts.

    Args:
        children: These typically inherit from air.Tag but can be anything
        is_htmx: Whether or not HTMX sent the request from the page

    """
    body_tags = filter_body_tags(children)
    head_tags = filter_head_tags(children)

    if is_htmx:
        return Children(Main(*body_tags, class_="container"), *head_tags)

    return Html(
        Head(
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
            ),
            Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
            *head_tags,
        ),
        Body(Main(*body_tags, class_="container")),
    )
