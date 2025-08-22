"""Tools for building layouts and several simple layouts for quick prototyping."""

from .tags import (
    Base,
    Body,
    Head,
    Html,
    Link,
    Main,
    Meta,
    Script,
    Style,
    Tag,
    Title,
    Header,
)

# ruff: noqa F841
HEAD_TAG_TYPES: tuple[type[Tag], ...] = (Title, Style, Meta, Link, Script, Base)


def filter_body_tags(tags) -> list:
    """Given a list of tags, only list the ones that belong in body of an HTML document."""
    return [t for t in tags if not isinstance(t, HEAD_TAG_TYPES)]


def filter_head_tags(tags) -> list:
    """Given a list of tags, only list the ones that belong in head of an HTML document."""
    return [t for t in tags if isinstance(t, HEAD_TAG_TYPES)]


def _header(tags) -> Header | str:
    """Extracts the air.Header tag from a set of tags."""
    for tag in tags:
        if isinstance(tag, Header):
            return tag
    return ""


def mvpcss(*children, htmx: bool = True, **kwargs):
    """Renders the basic layout with MVP.css and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. Header and Nav tags are placed in the top of the body above the Main tag
    4. HTMX is the default, change with the `htmx` keyword argument

    The `mvpcss` function is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `mvpcss` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged MVP.css implementation,
        you'll have to create your own layouts.

    Args:
        children: These typically inherit from air.Tag but can be anything
        htmx: Whether or not HTMX is active for the layout

    Example:

        import air

        app = air.Air()

        @app.page
        async def index():
            return air.layouts.mvpcss(
                air.H1('Welcome to Air')
            )
    """
    body_tags = filter_body_tags(children)
    head_tags = filter_head_tags(children)

    if htmx:
        head_tags.insert(
            0,
            Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
        )
    return Html(
        Head(
            Link(rel="stylesheet", href="https://unpkg.com/mvp.css"),
            *head_tags,
        ),
        Body(
            _header(body_tags),
            Main(*[x for x in body_tags if not isinstance(x, Header)]),
        ),
    ).render()


def picocss(*children, htmx: bool = True, **kwargs):
    """Renders the basic layout with PicoCSS and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. HTMX is the default, change with the `htmx` keyword argument

    Note: `PicoCSS` is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `pico` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged PicoCSS implementation,
        you'll have to create your own layouts.
    """
    body_tags = filter_body_tags(children)
    head_tags = filter_head_tags(children)
    if htmx:
        head_tags.insert(
            0,
            Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
        )
    return Html(
        Head(
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
            ),
            *head_tags,
        ),
        Body(Main(*body_tags, class_="container")),
    ).render()
