"""Test to improve coverage of stock.py tag classes.

This test specifically targets the super().__init__() calls in all stock tag classes
to ensure they are properly covered by tests.
"""

import air
from air import SelfClosingTag


def test_stock_tags_comprehensive_coverage() -> None:
    """Test that covers all stock tag classes to improve __init__ coverage."""

    # Test BaseTag subclasses with children and various attributes
    tags_with_children = [
        # Basic tags
        air.A("Link", href="/", target="_blank", class_="link"),
        air.Abbr("HTML", title="HyperText Markup Language"),
        air.Address("Contact info", class_="contact"),
        air.Article("Article content", id="main-article"),
        air.Aside("Sidebar content", class_="sidebar"),
        air.Audio("Audio content", controls=True, src="/audio.mp3"),
        air.B("Bold text", style="font-weight: bold"),
        # Block elements
        air.Blockquote("Quote text", cite="https://example.com", class_="quote"),
        air.Body("Body content", class_="main-body"),
        air.Button("Click me", type="submit", disabled=False, class_="btn"),
        air.Canvas("Canvas content", width=300, height=200, id="canvas"),
        air.Caption("Table caption", class_="table-caption"),
        air.Cite("Citation", class_="citation"),
        air.Code("console.log('hello')", class_="code"),
        air.Colgroup("Colgroup content", span=2),
        # Data and definition elements
        air.Datalist("Datalist content", id="browsers"),
        air.Dd("Definition description", class_="definition"),
        air.Del("Deleted text", datetime="2023-01-01", class_="deleted"),
        air.Details("Details content", open=True, class_="details"),
        air.Dfn("Definition", title="Definition title", class_="definition"),
        air.Dialog("Dialog content", open=False, id="modal"),
        air.Div("Div content", class_="container", id="main"),
        air.Dl("Description list", class_="description-list"),
        air.Dt("Definition term", class_="term"),
        # Emphasis and text formatting
        air.Em("Emphasized text", class_="emphasis"),
        air.Fieldset("Fieldset content", disabled=False, name="group1"),
        air.Figcaption("Figure caption", class_="caption"),
        air.Figure("Figure content", class_="figure"),
        air.Footer("Footer content", class_="page-footer"),
        air.Form("Form content", action="/submit", method="POST", class_="form"),
        # Headers
        air.H1("Header 1", id="title", class_="main-title"),
        air.H2("Header 2", class_="sub-title"),
        air.H3("Header 3", style="color: blue"),
        air.H4("Header 4", id="section"),
        air.H5("Header 5", class_="small-header"),
        air.H6("Header 6", style="font-size: 12px"),
        air.Head("Head content", class_="head"),
        air.Header("Page header", class_="page-header"),
        # Interactive elements
        air.Html("HTML content", lang="en", class_="html-root"),
        air.I("Italic text", class_="italic"),
        air.Iframe("Iframe content", src="/frame", width=400, height=300),
        air.Ins("Inserted text", datetime="2023-01-01", class_="inserted"),
        air.Kbd("Ctrl+C", class_="keyboard"),
        air.Label("Label text", for_="input1", class_="label"),
        air.Legend("Legend text", class_="legend"),
        air.Li("List item", class_="item", id="item1"),
        air.Main("Main content", class_="main-content"),
        air.Map("Map content", name="image-map", class_="map"),
        air.Mark("Highlighted text", class_="highlight"),
        # Media and object elements
        air.Menu("Menu content", type="toolbar", class_="menu"),
        air.Meter("Meter content", value=6, min=0, max=10),
        air.Nav("Navigation", class_="navigation"),
        air.Noscript("No script message", class_="noscript"),
        air.Object("Object content", data="/file.swf", type="application/x-shockwave-flash"),
        air.Ol("List content", type="1", start=1, class_="ordered-list"),
        air.Optgroup("Option group", label="Group 1", disabled=False),
        air.Option("Option text", value="option1", selected=True, class_="option"),
        air.Output("Output text", name="result", for_="input1", class_="output"),
        # Paragraph and text elements
        air.P("Paragraph text", class_="paragraph", id="p1"),
        air.Pre("Preformatted text", class_="preformatted"),
        air.Progress("Progress content", value=50, max=100, class_="progress"),
        air.Q("Quoted text", cite="https://example.com", class_="quote"),
        air.Rp("Rp content", class_="rp"),
        air.Rt("Rt content", class_="rt"),
        air.Ruby("Ruby text", class_="ruby"),
        air.S("Strikethrough text", class_="strikethrough"),
        air.Samp("Sample text", class_="sample"),
        air.Section("Section content", class_="section", id="section1"),
        air.Select("Select content", name="select1", multiple=True, class_="select"),
        air.Small("Small text", class_="small"),
        air.Span("Span text", class_="span", id="span1"),
        air.Strong("Strong text", class_="strong"),
        air.Sub("Subscript", class_="subscript"),
        air.Summary("Summary text", class_="summary"),
        air.Sup("Superscript", class_="superscript"),
        # Table elements
        air.Table("Table content", class_="table", id="table1"),
        air.Tbody("Table body", class_="tbody"),
        air.Td("Table cell", colspan=2, rowspan=1, class_="cell"),
        air.Template("Template content", id="template1", class_="template"),
        air.Textarea("Textarea content", name="textarea1", rows=5, cols=30),
        air.Tfoot("Table footer", class_="tfoot"),
        air.Th("Header cell", scope="col", class_="header-cell"),
        air.Thead("Table head", class_="thead"),
        air.Time("Time content", datetime="2023-01-01T10:00:00", class_="time"),
        air.Title("Page title", class_="title"),
        air.Tr("Table row", class_="row"),
        air.U("Underlined text", class_="underlined"),
        air.Ul("List content", class_="unordered-list"),
        air.Var("Variable", class_="variable"),
        air.Video("Video content", controls=True, width=640, height=480, src="/video.mp4"),
    ]

    # Test SelfClosingTag subclasses with various attributes
    self_closing_tags = [
        air.Area(alt="Area", coords="0,0,50,50", href="/area", shape="rect"),
        air.Base(href="https://example.com", target="_blank"),
        air.Br(class_="line-break", id="br1"),
        air.Col(span=2, class_="column"),
        air.Embed(src="/embed.swf", type="application/x-shockwave-flash", width=400, height=300),
        air.Hr(class_="divider", id="hr1"),
        air.Img(src="/image.jpg", alt="Image", width=300, height=200, class_="image"),
        air.Input(type="text", name="input1", value="default", required=True, class_="input"),
        air.Link(rel="stylesheet", href="/style.css", type="text/css"),
        air.Meta(name="description", content="Page description", charset="utf-8"),
        air.Param(name="param1", value="value1"),
        air.Source(src="/video.mp4", type="video/mp4", media="(min-width: 800px)"),
        air.Track(src="/subtitles.vtt", kind="subtitles", srclang="en", label="English"),
        air.Wbr(class_="word-break"),
    ]

    # Test that all tags can be instantiated and rendered
    all_tags = tags_with_children + self_closing_tags

    for tag in all_tags:
        # Test that the tag can be rendered (this ensures __init__ was called properly)
        rendered = tag.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0

        # Test that attributes were properly set
        assert hasattr(tag, "_attrs")
        assert hasattr(tag, "_name")

    # Test that we covered a significant number of tag classes
    assert len(all_tags) > 90, f"Expected to test more than 90 tags, got {len(all_tags)}"

    # Test some tags with no arguments to ensure basic instantiation works
    basic_tags = [
        air.Div(),
        air.P(),
        air.Span(),
        air.A(),
        air.Button(),
        air.Img(),
        air.Input(),
        air.Br(),
    ]

    for tag in basic_tags:
        rendered = tag.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0


def test_stock_tags_with_kwargs() -> None:
    """Test stock tags with keyword arguments to ensure locals_cleanup works."""

    # Test BaseTag subclasses with children and kwargs
    base_tag_tests = [
        (air.Div, {"data_test": "value", "aria_label": "test", "custom_attr": "custom"}),
        (air.P, {"hx_post": "/api", "hx_target": "#result", "_": "on click toggle .active"}),
        (air.A, {"href": "/", "@click": "handleClick", "x_data": "{ open: false }"}),
        (air.Button, {"type": "submit", "!important": "true", "data_bs_toggle": "modal"}),
        (air.Form, {"method": "POST", "hx_post": "/submit", "hx_target": "#result"}),
        (air.Select, {"name": "country", "v_model": "selectedCountry", "x_ref": "countrySelect"}),
    ]

    for tag_class, kwargs in base_tag_tests:
        # Test with children and kwargs
        tag_with_children = tag_class("Content", **kwargs)
        rendered = tag_with_children.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0

    # Test SelfClosingTag subclasses with just kwargs
    self_closing_tests = [
        (air.Input, {"type": "text", "v_model": "search", "name": "q", "placeholder": "Search..."}),
        (air.Img, {"src": "/img.jpg", "loading": "lazy", "data_src": "/high-res.jpg"}),
        (air.Br, {"class_": "break", "data_test": "value"}),
        (air.Hr, {"class_": "divider", "style": "margin: 10px"}),
    ]

    for tag_class, kwargs in self_closing_tests:
        # Test with just kwargs (SelfClosingTag doesn't accept children)
        tag_no_children = tag_class(**kwargs)
        rendered = tag_no_children.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0


def test_stock_tags_edge_cases() -> None:
    """Test edge cases for stock tags to ensure robust coverage."""

    # Test with mixed content types
    mixed_content_tags = [
        air.Div("Text", air.Span("Nested"), 42, "True", class_="mixed"),
        air.P(air.Strong("Bold"), " and ", air.Em("italic"), " text"),
        air.Ul(air.Li("Item 1"), air.Li("Item 2"), air.Li(air.A("Link", href="/"))),
        air.Table(air.Thead(air.Tr(air.Th("Header"))), air.Tbody(air.Tr(air.Td("Data"))), class_="data-table"),
    ]

    for tag in mixed_content_tags:
        rendered = tag.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0

    # Test with boolean attributes
    boolean_attr_tags = [
        air.Input(type="checkbox", checked=True, required=True, disabled=False),
        air.Button("Submit", disabled=True, autofocus=False),
        air.Select("Options", multiple=True, required=False, disabled=None),
        air.Textarea("Text", readonly=True, required=False, disabled=None),
        air.Option("Option", selected=True, disabled=False),
        air.Audio(controls=True, autoplay=False, loop=None, muted=True),
        air.Video(controls=True, autoplay=False, muted=True, loop=False),
        air.Details("Details", open=True),
        air.Dialog("Dialog", open=False),
    ]

    for tag in boolean_attr_tags:
        rendered = tag.render()
        assert isinstance(rendered, str)
        assert len(rendered) > 0


def test_stock_tags_inheritance() -> None:
    """Test that stock tags properly inherit from their base classes."""

    # Test a sample of BaseTag inheritance
    sample_base_tags = [
        air.Div,
        air.P,
        air.A,
        air.Button,
        air.Form,
        air.H1,
        air.H2,
        air.H3,
        air.Span,
        air.Strong,
        air.Em,
        air.Section,
        air.Article,
        air.Header,
        air.Footer,
    ]

    for tag_class in sample_base_tags:
        assert issubclass(tag_class, air.BaseTag)
        # Test instantiation
        instance = tag_class("test content", class_="test")
        assert isinstance(instance, air.BaseTag)
        assert isinstance(instance.render(), str)

    # Test a sample of SelfClosingTag inheritance (only actual SelfClosingTag subclasses)
    sample_self_closing = [air.Br, air.Hr, air.Img, air.Input, air.Meta, air.Link]

    for tag_class in sample_self_closing:
        assert issubclass(tag_class, SelfClosingTag)
        # Test instantiation
        instance = tag_class(class_="test")
        assert isinstance(instance, SelfClosingTag)
        assert isinstance(instance.render(), str)
