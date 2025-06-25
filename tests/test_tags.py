import air


def test_atag_no_attrs_no_children():
    assert air.A().render() == "<a></a>"


def test_atag_yes_attrs_no_children():
    tag = air.A(href="/", cls="link").render()
    assert tag == '<a href="/" class="link"></a>'


def test_atag_yes_attrs_text_children():
    tag = air.A("Link here", href="/", cls="link").render()
    assert tag == '<a href="/" class="link">Link here</a>'


def test_divtag_yes_attrs_a_child():
    html = air.Div(air.A("Link here", href="/", cls="link")).render()
    assert html == '<div><a href="/" class="link">Link here</a></div>'


def test_divtag_yes_attrs_multiple_a_children():
    html = air.Div(
        air.A("Link here", href="/", cls="link"),
        air.A("Another link", href="/", cls="timid"),
    ).render()
    assert (
        html
        == '<div><a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></div>'
    )


def test_divtag_yes_attrs_nested_children():
    html = air.Div(
        air.P(
            "Links are here",
            air.A("Link here", href="/", cls="link"),
            air.A("Another link", href="/", cls="timid"),
        )
    ).render()
    assert (
        html
        == '<div><p>Links are here<a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></p></div>'
    )


def test_name_types():
    assert issubclass(air.A, air.Tag)
    assert issubclass(air.Div, air.Tag)
    assert issubclass(air.P, air.Tag)


def test_subclassing():
    class AwesomeP(air.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    assert AwesomeP("library").render() == "<p>AWESOME library!</p>"


def test_subclassing_nested():
    class AwesomeP(air.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    html = air.Div(AwesomeP("library")).render()
    assert html == "<div><p>AWESOME library!</p></div>"


def test_text_child_with_sibling_elements():
    html = air.P("This is a", air.Strong("cut off"), "sentence").render()
    assert html == "<p>This is a<strong>cut off</strong>sentence</p>"


def test_special_attributes():
    html = air.P("Has a special attribute", **{"@fun": "times ahead"}).render()
    assert html == '<p @fun="times ahead">Has a special attribute</p>'

    html = air.P("Has a special attribute", **{"!data": "12345"}).render()
    assert html == '<p !data="12345">Has a special attribute</p>'

    html = air.P("HTMX example", hx_post="/get", _id="53").render()
    assert html == '<p hx-post="/get" id="53">HTMX example</p>'


def test_htmx_render():
    html = air.Htmx(air.P("Hello, world")).render()
    assert (
        html
        == '<!doctype html><html><head><script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.5/dist/htmx.min.js"></script></head><body><p>Hello, world</p></body></html>'
    )
