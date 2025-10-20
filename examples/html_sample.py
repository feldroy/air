from typing import Final

from air import *

SMALL_HTML_SAMPLE: Final = Html(
    Div(
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
            integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
            crossorigin="anonymous",
        ),
        H1("H1", data_cloud=True, data_earth="true"),
        H2("H1", data_cloud=True, data_earth="true"),
        P(
            A("A", data_cloud=True, data_earth="true"),
            A(SafeStr(":root & > < { --pico-font-size: 100%; }"), id="id1"),
            SafeStr("safe <> string"),
            A(":root & > < { --pico-font-size: 100%; }", id="id1"),
            Img(
                src="https://cdn.jsdelivr.net/dist/img.png",
                width=250,
                height=100,
                alt="My Img",
                checked=False,
                selected=True,
                bar="foo",
            ),
            "<>",
            Script("safe <> Script", crossorigin="anonymous"),
        ),
        class_="class1",
        id="id1",
        style="style1",
        kwarg1="kwarg1",
        kwarg2="kwarg2",
        kwarg3="kwarg3",
    )
)

HTML_SAMPLE: Final = Html(
    Head(
        Meta(
            property="og:image",
            content="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg",
        ),
        Meta(property="og:site_name", content="https://daniel.feldroy.com"),
        Meta(property="og:image:type", content="image/png"),
        Meta(property="og:type", content="website"),
        Meta(property="og:url", content="http://daniel.feldroy.com/"),
        Meta(property="og:title", content="Daniel Roy Greenfeld"),
        Meta(
            property="og:description",
            content="Daniel Roy Greenfeld's personal blog",
        ),
        Meta(
            content="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg",
            name="twitter:image",
        ),
        Meta(content="summary", name="twitter:card"),
        Meta(content="Daniel Roy Greenfeld", name="twitter:title"),
        Meta(
            content="Daniel Roy Greenfeld's personal blog",
            name="twitter:description",
        ),
        Link(href="http://daniel.feldroy.com/", rel="canonical"),
        Link(
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
            rel="stylesheet",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
            integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
            crossorigin="anonymous",
        ),
        Style(":root { --pico-font-size: 100%; }"),
        Link(
            href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css",
            media="(prefers-color-scheme: dark)",
            rel="stylesheet",
        ),
        Link(
            href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css",
            media="(prefers-color-scheme: light)",
            rel="stylesheet",
        ),
        Script(src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"),
        Script(
            src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js",
        ),
        Script(
            src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js",
        ),
        Script(
            src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/javascript.min.js",
        ),
        Script(
            src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/html.min.js",
        ),
        Script(
            src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/css.min.js",
        ),
        Link(href="/public/style.css", rel="stylesheet", type="text/css"),
        Title("Daniel Roy Greenfeld"),
    ),
    Body(
        Header(
            A(
                Img(
                    src="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg",
                    width="108",
                    alt="Daniel Roy Greenfeld",
                    class_="borderCircle",
                ),
                href="/",
            ),
            A(H2("Daniel Roy Greenfeld"), href="/"),
            P(
                A("About", href="/about"),
                "|",
                A("Articles (715)", href="/posts"),
                "|",
                A("Books", href="/books"),
                "|",
                A("Jobs", href="/jobs"),
                "|",
                A("Tags", href="/tags"),
                "|",
                A("Search", href="/search"),
            ),
            style="text-align: center;",
        ),
        Main(
            Div(
                Section(
                    H1("Recent Writings"),
                    Span(
                        H2(
                            A(
                                "Unpack for keyword arguments",
                                href="/posts/2025-07-unpack-for-keyword-arguments",
                            ),
                        ),
                        P(
                            "Keyword arguments can now be more narrowly typed by using typing.Unpack and typing.TypeDict.",
                            Br(),
                            Small(Time("July 27, 2025 at 4:55pm")),
                        ),
                    ),
                    Span(
                        H2(
                            A(
                                "uv run for running tests on versions of Python",
                                href="/posts/2025-07-uv-run-for-testing-python-versions",
                            ),
                        ),
                        P(
                            "Using uv run with make to replace tox or nox for testing multiple versions of Python locally.",
                            Br(),
                            Small(Time("July 20, 2025 at 10:08am")),
                        ),
                    ),
                    Span(
                        H2(
                            A(
                                "Farewell to Michael Ryabushkin",
                                href="/posts/2025-05-farewell-to-michael-ryabushkin",
                            ),
                        ),
                        P(
                            "In early May of 2025 Michael Ryabushkin (aka Goodwill) passed away. He was a great friend and an even better person. I will miss him dearly.",
                            Br(),
                            Small(Time("May 16, 2025 at 11:22am")),
                        ),
                    ),
                    Span(
                        H2(
                            A(
                                "Exploring flexicache",
                                href="/posts/2025-05-flexicache",
                            ),
                        ),
                        P(
                            "An exploration of using flexicache for caching in Python.",
                            Br(),
                            Small(Time("May 09, 2025 at 8:00am")),
                        ),
                    ),
                    P(
                        A(
                            "Read all articles",
                            href="<function posts at 0x7fa78cb1b740>",
                        ),
                    ),
                ),
                Section(
                    H1("TIL", Small("(Today I learned)")),
                    Span(
                        H3(
                            A(
                                "Setting environment variables for pytest",
                                href="/posts/til-2025-09-setting-environment-variables-for-pytest",
                            ),
                        ),
                        P(Small(Time("September 02, 2025 at 2:29am"))),
                    ),
                    Span(
                        H3(
                            A(
                                "Using SQLModel Asynchronously with FastAPI (and Air) with PostgreSQL",
                                href="/posts/til-2025-08-using-sqlmodel-asynchronously-with-fastapi-and-air-with-postgresql",
                            ),
                        ),
                        P(Small(Time("August 29, 2025 at 5:54am"))),
                    ),
                    Span(
                        H3(
                            A(
                                "Single source version package builds with uv (redux)",
                                href="/posts/til-2025-08-single-source-version-package-builds-with-uv-redux",
                            ),
                        ),
                        P(Small(Time("August 22, 2025 at 2:20am"))),
                    ),
                    Span(
                        H3(
                            A(
                                "How to type args and kwargs",
                                href="/posts/til-2025-07-how-to-type-args-and-kwargs",
                            ),
                        ),
                        P(Small(Time("July 26, 2025 at 9:15am"))),
                    ),
                    Span(
                        H3(
                            A(
                                "Single source version package builds with uv",
                                href="/posts/til-2025-07-single-source-version-package-builds-with-uv",
                            ),
                        ),
                        P(Small(Time("July 23, 2025 at 1:59am"))),
                    ),
                    Span(
                        H3(
                            A(
                                "Removing exif geodata from media",
                                href="/posts/til-2025-06-removing-exif-geodata-from-media",
                            ),
                        ),
                        P(Small(Time("June 23, 2025 at 8:56pm"))),
                    ),
                    Span(
                        H3(
                            A(
                                "HTML 404 errors for FastAPI",
                                href="/posts/til-2025-06-html-404-errors-for-fastapi",
                            ),
                        ),
                        P(Small(Time("June 13, 2025 at 4:23am"))),
                    ),
                    P(A("Read more TIL articles", href="/tags/TIL")),
                ),
                Section(
                    H1("Featured Writings"),
                    Span(
                        H2(
                            A(
                                "The Thirty Minute Rule",
                                href="/posts/thirty-minute-rule",
                            ),
                        ),
                        P(
                            "What to do when you get stuck on a coding issue for more than 30 minutes.",
                            Br(),
                            Small(Time("August 18, 2021 at 12:00am")),
                        ),
                    ),
                    Span(
                        H2(
                            A(
                                "What's the Best Thing about Working for Octopus Energy?",
                                href="/posts/whats-the-best-thing-about-working-for-octopus-energy-part-1",
                            ),
                        ),
                        P(
                            "An in-depth discussion about my employment at Octopus Energy.",
                            Br(),
                            Small(Time("June 08, 2021 at 11:59pm")),
                        ),
                    ),
                    Span(
                        H2(
                            A("Code, Code, Code", href="/posts/code-code-code"),
                        ),
                        P(
                            "I'm often asked by new programmers how they can forge a path into using their skills professionally. Or how they can get better at writing software. In this article I share the secret master-level method to improvement.",
                            Br(),
                            Small(Time("May 28, 2016 at 12:00am")),
                        ),
                    ),
                    Span(
                        H2(
                            A(
                                "I Married Audrey Roy",
                                href="/posts/i-married-audrey-roy",
                            ),
                        ),
                        P(
                            "The story of one of the best days of my life.",
                            Br(),
                            Small(Time("January 04, 2014 at 12:00am")),
                        ),
                    ),
                ),
                class_="grid",
            ),
            class_="container",
        ),
        Footer(
            Hr(),
            P(
                A(
                    "LinkedIn",
                    href="https://www.linkedin.com/in/danielfeldroy/",
                    target="_blank",
                ),
                "|",
                A(
                    "Bluesky",
                    href="https://bsky.app/profile/daniel.feldroy.com",
                    target="_blank",
                ),
                "|",
                A(
                    "Twitter",
                    href="https://twitter.com/pydanny",
                    target="_blank",
                ),
                "|",
                A("Github", href="https://github.com/pydanny", target="_blank"),
                "| Feeds:",
                A("All", href="/feeds/atom.xml", target="_blank"),
                ",",
                A("Python", href="/feeds/python.atom.xml", target="_blank"),
                ",",
                A("TIL", href="/feeds/til.atom.xml", target="_blank"),
            ),
            P("All rights reserved 2025, Daniel Roy Greenfeld"),
            class_="container",
        ),
        Dialog(
            Header(
                H2("Search"),
                Input(
                    hx_trigger="keyup",
                    hx_get="/search-results",
                    hx_target=".search-results-modal",
                    type="text",
                    name="q",
                    placeholder="Enter your search query...",
                    id="search-input",
                ),
                Div(class_="search-results-modal"),
                class_="modal-content",
            ),
            id="search-modal",
            style="display:none;",
            class_="modal overflow-auto",
        ),
        Div(hx_trigger="keyup[key=='/'] from:body"),
        Script(
            "document.body.addEventListener('keydown', e => {\n            if (e.key === '/') {\n                e.preventDefault();\n                document.getElementById('search-modal').style.display = 'block';\n                document.getElementById('search-input').focus();\n            }\n            if (e.key === 'Escape') {\n                document.getElementById('search-modal').style.display = 'none';\n            }\n            });\n\n            document.getElementById('search-input').addEventListener('input', e => {\n            htmx.trigger('.search-results', 'htmx:trigger', {value: e.target.value});\n            });",
        ),
        hx_boost="true",
    ),
)
