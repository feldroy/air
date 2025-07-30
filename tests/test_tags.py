import air
from air import tags


def _r(tag):
    "Shortcut for easy renders"
    return tag.render()


def test_atag_no_attrs_no_children():
    assert air.A().render() == "<a></a>"


def test_atag_yes_attrs_no_children():
    tag = air.A(href="/", class_="link").render()
    assert tag == '<a href="/" class="link"></a>'


def test_atag_yes_attrs_text_children():
    tag = air.A("Link here", href="/", class_="link").render()
    assert tag == '<a href="/" class="link">Link here</a>'


def test_divtag_yes_attrs_a_child():
    html = air.Div(air.A("Link here", href="/", class_="link")).render()
    assert html == '<div><a href="/" class="link">Link here</a></div>'


def test_divtag_yes_attrs_multiple_a_children():
    html = air.Div(
        air.A("Link here", href="/", class_="link"),
        air.A("Another link", href="/", class_="timid"),
    ).render()
    assert (
        html
        == '<div><a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></div>'
    )


def test_divtag_yes_attrs_nested_children():
    html = air.Div(
        air.P(
            "Links are here",
            air.A("Link here", href="/", class_="link"),
            air.A("Another link", href="/", class_="timid"),
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


def test_raw_html_basic():
    """Test basic Raw rendering without escaping."""
    raw = air.Raw("<strong>Bold</strong> & <em>italic</em>")
    assert raw.render() == "<strong>Bold</strong> & <em>italic</em>"


def test_raw_html_with_script():
    """Test that Raw does not escape script tags (security risk)."""
    raw = air.Raw('<script>alert("XSS")</script>')
    assert raw.render() == '<script>alert("XSS")</script>'
    # This test documents the security risk


def test_raw_html_invalid_args():
    """Test that Raw raises errors with invalid arguments."""
    try:
        air.Raw("first", "second")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "Raw accepts only one string argument" in str(e)

    try:
        air.Raw(123)
        assert False, "Expected TypeError"
    except TypeError as e:
        assert "Raw only accepts string content" in str(e)

    try:
        air.Raw(air.Div("test"))
        assert False, "Expected TypeError"
    except TypeError as e:
        assert "Raw only accepts string content" in str(e)


def test_raw_html_ignores_kwargs():
    """Test that Raw ignores keyword arguments."""
    raw = air.Raw("<div>Test</div>", id="ignored", class_="also-ignored")
    assert raw.render() == "<div>Test</div>"


def test_functions_as_tags():
    """Test that functions can be used as tags."""

    def article_preview(title: str, slug: str, description: str):
        return air.Article(
            air.H2(air.A(title, href=f"/posts/{slug}")), air.P(description)
        )

    articles = [
        article_preview("First Post", "first-post", "This is the first post."),
        article_preview("Second Post", "second-post", "This is the second post."),
        article_preview("Third Post", "third-post", "This is the third post."),
    ]

    content = air.Main(air.H1("Articles"), *articles, air.P("Read more on our blog."))
    assert isinstance(content.render(), str)

    def layout(*children):
        return air.Html(*children)

    html = layout(content)
    assert isinstance(html.render(), str)


def test_pico_card():
    def card(*content, header: str, footer: str):
        return air.Article(air.Header(header), *content, air.Footer(footer))

    html = card(
        air.P("This is a card with some content."),
        header="Card Header",
        footer="Card Footer",
    ).render()

    assert (
        html
        == "<article><header>Card Header</header><p>This is a card with some content.</p><footer>Card Footer</footer></article>"
    )


def test_tags_head_tag_injection():
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
        == '<!doctype html><html><head><title>Test Page</title><meta property="og:title" content="Test Title" /><meta property="og:description" content="Test Description" /></head><body><h1>Check Page Source</h1><p>The meta tags should be in the head section.</p></body></html>'
    )


def test_escape_html():
    html = air.P("I'm <strong>Strong</strong>").render()
    assert html == "<p>I&#x27;m &lt;strong&gt;Strong&lt;/strong&gt;</p>"


def test_script_tag():
    js = "console.log('I am a snippet of javascript');"
    html = air.Script(js, class_="test").render()
    assert html == f"""<script class="test">{js}</script>"""


def test_style_tag():
    css = "p {border-style: solid; border-width: 5px;}"
    html = air.Style(css, class_="test").render()
    assert html == f"""<style class="test">{css}</style>"""


def test_tags_support_global_attributes():
    assert air.A("Hello", data=123).render() == '<a data="123">Hello</a>'
    assert air.A("this", draggable="true").render() == '<a draggable="true">this</a>'


def test_special_characters():
    assert air.P("Hello", id="mine").render() == '<p id="mine">Hello</p>'
    assert air.P("Hello", **{"@data": 1}).render() == '<p @data="1">Hello</p>'


def test_bool_attributes():
    assert (
        _r(air.Option("South America", value="SA", selected=True))
        == '<option selected value="SA">South America</option>'
    )
    assert (
        _r(air.Option("North America", value="NA", selected=False))
        == '<option value="NA">North America</option>'
    )


def test_self_closing_tags():
    html = _r(air.Area(shape="rect", coords="10,20,30,40", alt="Box", href="/box"))
    assert html == '<area alt="Box" coords="10,20,30,40" href="/box" shape="rect" />'


def test_children_tag():
    html = _r(air.Children(air.P("Hello, world!")))
    assert html == "<p>Hello, world!</p>"
    assert (
        _r(air.Children(air.P("Hello, world!"), air.P("Uma")))
        == "<p>Hello, world!</p><p>Uma</p>"
    )


def test_tag_generation():
    """This test exists because not all Tags are covered by other
    tests in this file. It performs a render check on all tag subclasses
    within the tags.py module.
    """
    for name in dir(tags):
        obj = getattr(tags, name)
        if isinstance(obj, type) and issubclass(obj, air.Tag):
            assert obj("test").render()


def test_safestr():
    assert tags.SafeStr("test").__repr__() == "'test'"


def test_other_children_types():
    assert tags.A(1).render() == "<a>1</a>"


def test_tag_for_tag_subclass_wrapper():
    html = _r(air.Tag(air.P("Hello, world!")))
    assert html == "<p>Hello, world!</p>"
