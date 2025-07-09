import air


def test_pico_layout():
    html = air.layouts.picocss(air.H1("Cheese Monger"), air.Title("Cheese Monger"))
    assert "htmx.min.js" in html
    assert "pico.min.css" in html
    assert "<title>Cheese Monger</title>" in html
    assert "<h1>Cheese Monger</h1>" in html
    assert (
        """<!doctype html><html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"></link><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm" crossorigin="anonymous"></script><title>Cheese Monger</title></head><body><main class="container"><h1>Cheese Monger</h1></main></body></html>"""
        == html
    )


def test_mvpcss_layout():
    html = air.layouts.mvpcss(air.H1("Cheese Monger"), air.Title("Cheese Monger"))
    assert "htmx.min.js" in html
    assert "mvp.css" in html
    assert "<title>Cheese Monger</title>" in html
    assert "<h1>Cheese Monger</h1>" in html
    assert (
        """<!doctype html><html><head><link rel="stylesheet" href="https://unpkg.com/mvp.css"></link><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm" crossorigin="anonymous"></script><title>Cheese Monger</title></head><body><main><h1>Cheese Monger</h1></main></body></html>"""
        == html
    )
