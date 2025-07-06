import air


def test_pico_page():
    html = air.pico_page(air.H1("Cheese Monger"), air.Title("Cheese Monger"))
    assert "htmx.min.js" in html
    assert "pico.min.css" in html
    assert "<title>Cheese Monger</title>" in html
    assert "<h1>Cheese Monger</h1>" in html
