"""Tools for building layouts and several simple layouts for quick prototyping."""

from enum import Enum, auto
from typing import Any

from .tags import Body, Children, Head, Header, Html, Link, Main, Script, Style
from .tags.models.types import FOOTER_TAG_TYPES, HEAD_TAG_TYPES, HEADER_TAG_TYPES, AttributeType


def filter_body_tags(tags: tuple) -> list:
    """Given a list of tags, only list the ones that belong in body of an HTML document.

    Returns:
        List of tags that belong in the body of an HTML document.
    """
    return [t for t in tags if not isinstance(t, HEAD_TAG_TYPES)]


def filter_head_tags(tags: tuple) -> list:
    """Given a list of tags, only list the ones that belong in head of an HTML document.

    Returns:
        List of tags that belong in the head of an HTML document.
    """
    return [t for t in tags if isinstance(t, HEAD_TAG_TYPES)]


def filter_header_tags(tags: tuple) -> list:
    """Given a list of tags, only list the ones that belong in header of an HTML document.

    Returns:
        List of tags that belong in the header of an HTML document.
    """
    return [t for t in tags if isinstance(t, HEADER_TAG_TYPES)]


def filter_footer_tags(tags: tuple) -> list:
    """Given a list of tags, only list the ones that belong in footer of an HTML document.

    Returns:
        List of tags that belong in the footer of an HTML document.
    """
    return [t for t in tags if isinstance(t, FOOTER_TAG_TYPES)]


def _header(tags: tuple | list) -> Header | str:
    """Extracts the Header tag from a set of tags.

    Returns:
        The Header tag if found, otherwise an empty string.
    """
    for tag in tags:
        if isinstance(tag, Header):
            return tag
    return ""


class MuTheme(Enum):
    red = auto()
    pumpkin = auto()
    orange = auto()
    amber = auto()
    yellow = auto()
    lime = auto()
    green = auto()
    jade = auto()
    cyan = auto()
    azure = auto()  # default
    blue = auto()
    indigo = auto()
    violet = auto()
    purple = auto()
    fuchsia = auto()
    pink = auto()
    sand = auto()
    grey = auto()
    zinc = auto()
    slate = auto()


def mucss(
    *children: Any,
    theme: MuTheme = MuTheme.azure,
    force_dark_mode: bool = False,
    is_htmx: bool = False,
    **kwargs: AttributeType,
) -> Html | Children:
    """Renders the basic layout with μCSS and HTMX for quick prototyping.

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
        a. `Header` is placed above `Main`
        a. `Footer` is placed below `Main`
    3. If `is_htmx` is True, then the layout isn't included. This is to support the `hx_boost`
        feature of HTMX

    Args:
        children: These typically inherit from Tag but can be anything
        theme:
        force_dark_mode: For forcing dark-colored pages
        is_htmx: Whether or not HTMX sent the request from the page

    Returns:
        HTML document with MuCSS styling or Children for HTMX partial responses.

    Example:

        import air

        app = Air()


        @app.page
        async def index(request: Request) -> Html | Children:
            return layouts.MuCSS(
                Title("Home"),
                Article(
                    H1("Welcome to Air"),
                    P(A("Click to go to Dashboard", href="/dashboard")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        @app.page
        async def dashboard(request: Request) -> Html | Children:
            return layouts.MuCSS(
                Title("Dashboard"),
                Article(
                    H1("Dashboard"),
                    P(A("Go home", href="/")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="127.0.0.1", port=8000)
    """
    body_tags = filter_body_tags(filter_body_tags(children))
    head_tags = filter_head_tags(children)
    header_tags = filter_header_tags(children)
    footer_tags = filter_footer_tags(children)

    if is_htmx:
        return Children(Main(*body_tags, class_="container"), *head_tags)

    return Html(
        Head(
            Link(
                rel="stylesheet",
                href=f"https://unpkg.com/@digicreon/mucss/dist/mu.{theme}.css",
            ),
            Style("""
@media (max-width: 768px) {
  body {
    font-size: 18px;
    line-height: 1.7;
    padding: 0 14px;
  }

  h1, h2, h3 {
    line-height: 1.25;
  }

  pre, code {
    font-size: 0.9em;
    overflow-x: auto;
  }
}
"""),
            Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
            *head_tags,
        ),
        Body(
            *header_tags,
            Main(*body_tags, class_="container"),
            *footer_tags,
        ),
        data_theme="dark" if force_dark_mode else "",
    )


def mvpcss(*children: Any, is_htmx: bool = False, **kwargs: AttributeType) -> Html | Children:
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
        children: These typically inherit from Tag but can be anything
        is_htmx: Whether or not HTMX sent the request from the page

    Returns:
        HTML document with MVP.css styling or Children for HTMX partial responses.

    Example:

        import air

        app = Air()


        @app.page
        async def index(request: Request) -> Html | Children:
            return layouts.mvpcss(
                Title("Home"),
                Article(
                    H1("Welcome to Air"),
                    P(A("Click to go to Dashboard", href="/dashboard")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        @app.page
        async def dashboard(request: Request) -> Html | Children:
            return layouts.mvpcss(
                Title("Dashboard"),
                Article(
                    H1("Dashboard"),
                    P(A("Go home", href="/")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="127.0.0.1", port=8000)
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


def picocss(*children: Any, is_htmx: bool = False, **kwargs: AttributeType) -> Html | Children:
    """Renders the basic layout with PicoCSS and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. If `is_htmx` is True, then the layout isn't included. This is to support the `hx_boost`
        feature of HTMX

    Note: `PicoCSS` is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `picocss` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged PicoCSS implementation,
        you'll have to create your own layouts.

    Args:
        children: These typically inherit from Tag but can be anything
        is_htmx: Whether or not HTMX sent the request from the page

    Returns:
        HTML document with PicoCSS styling or Children for HTMX partial responses.

    Example:

        import air

        app = Air()


        @app.page
        async def index(request: Request) -> Html | Children:
            return layouts.picocss(
                Title("Home"),
                Article(
                    H1("Welcome to Air"),
                    P(A("Click to go to Dashboard", href="/dashboard")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        @app.page
        async def dashboard(request: Request) -> Html | Children:
            return layouts.picocss(
                Title("Dashboard"),
                Article(
                    H1("Dashboard"),
                    P(A("Go home", href="/")),
                    hx_boost="true",
                ),
                is_htmx=request.htmx.is_hx_request,
            )


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="127.0.0.1", port=8000)
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
