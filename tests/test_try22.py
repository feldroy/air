from inline_snapshot import snapshot

import air

from .utils import clean_doc


def test_mvpcss_layout_try_1() -> None:
    actual_html = air.layouts.mvpcss(
        air.H1("Cheese Monger"), air.Title("Cheese Monger")
    ).pretty_render()
    expected_html = clean_doc(
        snapshot(
            """
            <!doctype html>
            <html>
              <head>
                <link href="https://unpkg.com/mvp.css" rel="stylesheet">
                <style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>
                <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
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
    )
    assert actual_html == expected_html


def test_mvpcss_layout_try_3() -> None:
    actual_html = air.layouts.mvpcss(
        air.H1("Cheese Monger"), air.Title("Cheese Monger")
    ).pretty_render()
    expected_html = snapshot(
        """
        <!doctype html>
        <html>
          <head>
            <link href="https://unpkg.com/mvp.css" rel="stylesheet">
            <style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>
            <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
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


def test_mvpcss_layout_try_2() -> None:
    actual_html = air.layouts.mvpcss(
        air.H1("Cheese Monger"), air.Title("Cheese Monger")
    ).pretty_render()
    expected_html = clean_doc(
        """
        <!doctype html>
        <html>
          <head>
            <link href="https://unpkg.com/mvp.css" rel="stylesheet">
            <style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>
            <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
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
