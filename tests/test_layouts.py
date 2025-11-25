import air

from .utils import clean_doc, clean_doc_with_broken_lines


def test_pico_layout() -> None:
    actual_html = air.layouts.picocss(air.H1("Cheese Monger"), air.Title("Cheese Monger")).pretty_render()
    expected_html = clean_doc_with_broken_lines(
        r"""
        <!doctype html>
        <html>
          <head>
            <link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" \
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
            <title>Cheese Monger</title>
          </head>
          <body>
            <main class="container">
              <h1>Cheese Monger</h1>
            </main>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html


def test_pico_layout_htmx() -> None:
    actual_html = air.layouts.picocss(air.H1("Hello, Air"), is_htmx=True).pretty_render()
    expected_html = clean_doc(
        """
        <main class="container">
          <h1>Hello, Air</h1>
        </main>
        """
    )
    assert actual_html == expected_html


def test_mvpcss_layout() -> None:
    actual_html = air.layouts.mvpcss(air.H1("Cheese Monger"), air.Title("Cheese Monger")).pretty_render()
    expected_html = clean_doc_with_broken_lines(
        r"""
        <!doctype html>
        <html>
          <head>
            <link href="https://unpkg.com/mvp.css" rel="stylesheet">
            <style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>
            <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" \
              integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
            <title>Cheese Monger</title>
          </head>
          <body>
            <main>
              <h1>Cheese Monger</h1>
            </main>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html


def test_mvpcss_layout_header() -> None:
    actual_html = air.layouts.mvpcss(
        air.Header(
            air.H1("This is in the header"),
        ),
        air.P("This is in the main"),
    ).pretty_render()
    expected_html = clean_doc_with_broken_lines(
        r"""
        <!doctype html>
        <html>
          <head>
            <link href="https://unpkg.com/mvp.css" rel="stylesheet">
            <style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>
            <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" \
              integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
          </head>
          <body>
            <header>
              <h1>This is in the header</h1>
            </header>
            <main>
              <p>This is in the main</p>
            </main>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html


def test_mvpcss_layout_htmx() -> None:
    actual_html = air.layouts.mvpcss(air.H1("Hello, Air"), is_htmx=True).pretty_render()
    expected_html = clean_doc(
        """
        <main>
          <h1>Hello, Air</h1>
        </main>
        """
    )
    assert actual_html == expected_html
