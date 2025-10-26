import air


def test_pico_layout() -> None:
    html = air.layouts.picocss(air.H1("Cheese Monger"), air.Title("Cheese Monger"))
    assert (
        html.render()
        == '<!doctype html><html><head><link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"'
        ' rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js"'
        ' crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm">'
        '</script><title>Cheese Monger</title></head><body><main class="container">'
        "<h1>Cheese Monger</h1></main></body></html>"
    )


def test_pico_layout_htmx() -> None:
    html = air.layouts.picocss(air.H1("Hello, Air"), is_htmx=True)
    assert html.render() == '<main class="container"><h1>Hello, Air</h1></main>'


def test_mvpcss_layout() -> None:
    html = air.layouts.mvpcss(air.H1("Cheese Monger"), air.Title("Cheese Monger"))
    assert (
        html.render() == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet">'
        "<style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>"
        '<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous"'
        ' integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>'
        "<title>Cheese Monger</title></head><body><main><h1>Cheese Monger</h1></main></body></html>"
    )


def test_mvpcss_layout_header() -> None:
    html = air.layouts.mvpcss(
        air.Header(
            air.H1("This is in the header"),
        ),
        air.P("This is in the main"),
    )
    assert (
        html.render() == '<!doctype html><html><head><link href="https://unpkg.com/mvp.css" rel="stylesheet">'
        "<style>footer, header, main { padding: 1rem; } nav {margin-bottom: 1rem;}</style>"
        '<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous"'
        ' integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm">'
        "</script></head><body><header><h1>This is in the header</h1></header>"
        "<main><p>This is in the main</p></main></body></html>"
    )


def test_mvpcss_layout_htmx() -> None:
    html = air.layouts.mvpcss(air.H1("Hello, Air"), is_htmx=True)
    assert html.render() == "<main><h1>Hello, Air</h1></main>"
