from .tags import Base, Body, Head, Html, Link, Main, Meta, Script, Style, Tag, Title


def pico_page(*children, htmx: bool = True, **kwargs):
    """Renders the basic layout with Pico and HTMX for quick prototyping

    1. At the top level HTML head tags are put in the <head>
    2. Otherwise everything is put in the <body>
    3. HTMX is the default, change with the `htmx` keyword argument

    Note: pico_page is a quick prototyping tool. It isn't designed to be extensible,
        rather it makes it easy to roll out quick demonstrations and proofs-of-concept.
        For more advanced layouts like Eidos or a full-fledged PicoCSS implementation,
        you'll have to create your own layouts.
    """
    HEAD_TAG_TYPES: tuple[Tag] = (Title, Style, Meta, Link, Script, Base)  # type: ignore [assignment]
    body_tags = [c for c in children if not isinstance(c, HEAD_TAG_TYPES)]  # type: ignore [arg-type]
    head_tags = [c for c in children if isinstance(c, HEAD_TAG_TYPES)]  # type: ignore [arg-type]
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
        Body(Main(*body_tags, cls="container")),
    ).render()
