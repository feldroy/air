from typing import Any

import pytest

import air


def _r(tag: air.BaseTag):
    """Shortcut for easy renders"""
    return tag.render()


def test_atag_no_attrs_no_children() -> None:
    assert air.A().render() == "<a></a>"


def test_atag_yes_attrs_no_children() -> None:
    tag = air.A(href="/", class_="link").render()
    assert tag == '<a href="/" class="link"></a>'


def test_atag_yes_attrs_text_children() -> None:
    tag = air.A("Link here", href="/", class_="link").render()
    assert tag == '<a href="/" class="link">Link here</a>'


def test_divtag_yes_attrs_a_child() -> None:
    html = air.Div(air.A("Link here", href="/", class_="link")).render()
    assert html == '<div><a href="/" class="link">Link here</a></div>'


def test_divtag_yes_attrs_multiple_a_children() -> None:
    html = air.Div(
        air.A("Link here", href="/", class_="link"),
        air.A("Another link", href="/", class_="timid"),
    ).render()
    assert html == '<div><a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></div>'


def test_divtag_yes_attrs_nested_children() -> None:
    html = air.Div(
        air.P(
            "Links are here",
            air.A("Link here", href="/", class_="link"),
            air.A("Another link", href="/", class_="timid"),
        ),
    ).render()
    assert (
        html
        == '<div><p>Links are here<a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></p></div>'
    )


def test_name_types() -> None:
    assert issubclass(air.A, air.BaseTag)
    assert issubclass(air.Div, air.BaseTag)
    assert issubclass(air.P, air.BaseTag)


def test_subclassing() -> None:
    class AwesomeP(air.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    assert AwesomeP("library").render() == "<p>AWESOME library!</p>"


def test_subclassing_nested() -> None:
    class AwesomeP(air.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    html = air.Div(AwesomeP("library")).render()
    assert html == "<div><p>AWESOME library!</p></div>"


def test_text_child_with_sibling_elements() -> None:
    html = air.P("This is a", air.Strong("cut off"), "sentence").render()
    assert html == "<p>This is a<strong>cut off</strong>sentence</p>"


def test_special_attributes() -> None:
    html = air.P("Has a special attribute", **{"@fun": "times ahead"}).render()
    assert html == '<p @fun="times ahead">Has a special attribute</p>'

    html = air.P("Has a special attribute", **{"!data": "12345"}).render()
    assert html == '<p !data="12345">Has a special attribute</p>'

    html = air.P("HTMX example", hx_post="/get", _id="53").render()
    assert html == '<p hx-post="/get" id="53">HTMX example</p>'


def test_raw_html_basic() -> None:
    """Test basic Raw rendering without escaping."""
    raw = air.Raw("<strong>Bold</strong> & <em>italic</em>")
    assert raw.render() == "<strong>Bold</strong> & <em>italic</em>"


def test_raw_html_with_script() -> None:
    """Test that Raw does not escape script tags (security risk)."""
    raw = air.Raw('<script>alert("XSS")</script>')
    assert raw.render() == '<script>alert("XSS")</script>'
    # This test documents the security risk


def test_raw_html_invalid_args() -> None:
    """Test that Raw raises errors with invalid arguments."""
    with pytest.raises(TypeError):
        air.Raw("first", "second")

    with pytest.raises(TypeError):
        air.Raw(123)

    with pytest.raises(TypeError):
        air.Raw(air.Div("test"))


def test_raw_html_reject_kwargs() -> None:
    """Test that Raw reject keyword arguments."""
    with pytest.raises(TypeError):
        air.Raw("<div>Test</div>", id="ignored", class_="also-ignored")


def test_functions_as_tags() -> None:
    """Test that functions can be used as tags."""

    def article_preview(title: str, slug: str, description: str) -> air.Article:
        return air.Article(air.H2(air.A(title, href=f"/posts/{slug}")), air.P(description))

    articles = [
        article_preview("First Post", "first-post", "This is the first post."),
        article_preview("Second Post", "second-post", "This is the second post."),
        article_preview("Third Post", "third-post", "This is the third post."),
    ]

    content = air.Main(air.H1("Articles"), *articles, air.P("Read more on our blog."))
    assert isinstance(content.render(), str)

    def layout(*children: Any) -> air.Html:
        return air.Html(*children)

    html = layout(content)
    assert isinstance(html.render(), str)


def test_pico_card() -> None:
    def card(*children: Any, header: str, footer: str) -> air.Article:
        return air.Article(air.Header(header), *children, air.Footer(footer))

    html = card(
        air.P("This is a card with some content."),
        header="Card Header",
        footer="Card Footer",
    ).render()

    assert (
        html
        == "<article><header>Card Header</header><p>This is a card with some content.</p><footer>Card Footer</footer></article>"
    )


def test_tags_head_tag_injection() -> None:
    meta_tags = [
        air.Meta(property="og:title", content="Test Title"),
        air.Meta(property="og:description", content="Test Description"),
    ]

    html = air.Html(
        air.Head(
            air.Title("Test Page"),
            *meta_tags,  # These should appear in <head>
        ),
        air.Body(
            air.H1("Check Page Source"),
            air.P("The meta tags should be in the head section."),
        ),
    ).render()

    assert (
        html
        == '<!doctype html><html><head><title>Test Page</title><meta property="og:title" content="Test Title"><meta property="og:description" content="Test Description"></head><body><h1>Check Page Source</h1><p>The meta tags should be in the head section.</p></body></html>'
    )


def test_escape_html() -> None:
    html = air.P("I'm <strong>Strong</strong>").render()
    assert html == "<p>I&#x27;m &lt;strong&gt;Strong&lt;/strong&gt;</p>"


def test_script_tag() -> None:
    js = "console.log('I am a snippet of javascript');"
    html = air.Script(js, class_="test").render()
    assert html == f"""<script class="test">{js}</script>"""


def test_style_tag() -> None:
    css = "p {border-style: solid; border-width: 5px;}"
    html = air.Style(css, class_="test").render()
    assert html == f"""<style class="test">{css}</style>"""


def test_tags_support_global_attributes() -> None:
    assert air.A("Hello", data=123).render() == '<a data="123">Hello</a>'
    assert air.A("this", draggable="true").render() == '<a draggable="true">this</a>'


def test_special_characters() -> None:
    assert air.P("Hello", id="mine").render() == '<p id="mine">Hello</p>'
    assert air.P("Hello", **{"@data": 1}).render() == '<p @data="1">Hello</p>'


def test_bool_attributes() -> None:
    assert (
        _r(air.Option("South America", value="SA", selected=True))
        == '<option selected value="SA">South America</option>'
    )
    assert _r(air.Option("North America", value="NA", selected=False)) == '<option value="NA">North America</option>'


def test_self_closing_tags() -> None:
    html = _r(air.Area(shape="rect", coords="10,20,30,40", alt="Box", href="/box"))
    assert html == '<area alt="Box" coords="10,20,30,40" href="/box" shape="rect">'


def test_children_tag() -> None:
    html = _r(air.Children(air.P("Hello, world!")))
    assert html == "<p>Hello, world!</p>"
    assert _r(air.Children(air.P("Hello, world!"), air.P("Uma"))) == "<p>Hello, world!</p><p>Uma</p>"


def test_tag_generation() -> None:
    """This test exists because not all Tags are covered by other
    tests in this file. It performs a render check on all tag subclasses
    within the tags.py module.
    """
    for tag in air.BaseTag.registry.values():
        rendered = None
        if issubclass(tag, air.UnSafeTag):
            rendered = tag("test").render()
        elif issubclass(tag, air.SelfClosingTag):
            rendered = tag(foo="bar").render()
        elif issubclass(tag, air.Transparent):
            rendered = tag(air.H1("test")).render()
        else:
            rendered = tag(air.H1("test"), foo="bar").render()
        assert rendered


def test_safestr() -> None:
    assert repr(air.SafeStr("test")) == "'test'"


def test_other_children_types() -> None:
    assert air.A(1).render() == "<a>1</a>"


def test_tag_for_tag_subclass_wrapper() -> None:
    html = _r(air.Tag(air.P("Hello, world!")))
    assert html == "<p>Hello, world!</p>"


def test_tag_label_for() -> None:
    html = _r(air.Label("Email Address:", for_="email"))
    assert html == '<label for="email">Email Address:</label>'


def test_tag_label_as() -> None:
    html = _r(air.Link(as_="fred"))
    assert html == '<link as="fred">'


def test_tag_bool_tag() -> None:
    html = _r(air.A("Air", data_fresh_air=True))
    assert html == "<a data-fresh-air>Air</a>"
    html = _r(air.P(air.A("Air", data_cloud=True, data_earth="true")))
    assert html == '<p><a data-cloud data-earth="true">Air</a></p>'


def test_input_boolean_attributes() -> None:
    """Test that Input tag boolean attributes render correctly."""

    # Test autofocus=True renders as boolean attribute
    html = _r(air.Input(name="q", autofocus=True))
    assert html == '<input name="q" autofocus>'

    # Test autofocus=False doesn't render the attribute
    html = _r(air.Input(name="q", autofocus=False))
    assert html == '<input name="q">'

    # Test autofocus=None doesn't render the attribute
    html = _r(air.Input(name="q", autofocus=None))
    assert html == '<input name="q">'

    # Test checked=True renders as boolean attribute
    html = _r(air.Input(type="checkbox", name="agree", checked=True))
    assert html == '<input name="agree" type="checkbox" checked>'

    # Test checked=False doesn't render the attribute
    html = _r(air.Input(type="checkbox", name="agree", checked=False))
    assert html == '<input name="agree" type="checkbox">'

    # Test disabled=True renders as boolean attribute
    html = _r(air.Input(name="q", disabled=True))
    assert html == '<input name="q" disabled>'

    # Test disabled=False doesn't render the attribute
    html = _r(air.Input(name="q", disabled=False))
    assert html == '<input name="q">'

    # Test required=True renders as boolean attribute
    html = _r(air.Input(name="email", required=True))
    assert html == '<input name="email" required>'

    # Test required=False doesn't render the attribute
    html = _r(air.Input(name="email", required=False))
    assert html == '<input name="email">'


def test_input_boolean_attributes_combinations() -> None:
    """Test combinations of boolean attributes on Input tag."""

    # Test multiple boolean attributes together
    html = _r(air.Input(name="email", type="email", required=True, autofocus=True, disabled=False))
    assert html == '<input name="email" type="email" required autofocus>'

    # Test with some True and some False
    html = _r(air.Input(name="q", autofocus=True, disabled=False, required=True))
    assert html == '<input name="q" required autofocus>'

    # Test with checkbox and checked
    html = _r(air.Input(type="checkbox", name="terms", checked=True, required=True))
    assert html == '<input name="terms" type="checkbox" required checked>'


def test_input_boolean_attributes_with_other_attrs() -> None:
    """Test boolean attributes work correctly with other attributes."""

    # Test autofocus with other attributes
    html = _r(air.Input(name="search", type="text", placeholder="Search...", autofocus=True, class_="search-input"))
    assert html == '<input name="search" type="text" autofocus placeholder="Search..." class="search-input">'

    # Test disabled with other attributes
    html = _r(air.Input(name="readonly", type="text", value="Can't change me", disabled=True, readonly=True))
    assert html == '<input name="readonly" type="text" value="Can\'t change me" readonly disabled>'
