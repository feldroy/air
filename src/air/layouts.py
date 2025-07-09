from .tags import Base, Body, Head, Html, Link, Main, Meta, Script, Style, Tag, Title

# ruff: noqa F841
HEAD_TAG_TYPES: tuple[Tag] = (Title, Style, Meta, Link, Script, Base)  # type: ignore [assignment]


def filter_body_tags(tags) -> list:
    """Given a list of tags, only list the ones that belong in body."""
    return [t for t in tags if not isinstance(t, HEAD_TAG_TYPES)]  # type: ignore [arg-type]


def filter_head_tags(tags) -> list:
    """Given a list of tags, only list the ones that belong in head."""
    return [t for t in tags if isinstance(t, HEAD_TAG_TYPES)]  # type: ignore [arg-type]


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
    body_tags = filter_body_tags(children)  # type: ignore [arg-type]
    head_tags = filter_head_tags(children)  # type: ignore [arg-type]
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


def mvpcss(*children, htmx: bool = True, **kwargs):
    """Renders the basic layout with MVP.css and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the `<head>` tag
    2. Otherwise everything is put in the `<body>`
    3. HTMX is the default, change with the `htmx` keyword argument

    Note: `MVP.css` is a quick prototyping tool. It isn't designed to be extensible.
        Rather the `mvpcss` layout function makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged PicoCSS implementation,
        you'll have to create your own layouts.
    """
    body_tags = filter_body_tags(children)  # type: ignore [arg-type]
    head_tags = filter_head_tags(children)  # type: ignore [arg-type]
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
        Body(Main(*body_tags)),
    ).render()
