"""Adds s-expression HTML tags to air."""

import html
from functools import cached_property
from xml.etree import ElementTree as ET


def html_to_airtags(html_text: str, air_prefix: bool = True) -> str:
    def convert_attrs(attrs):
        parts = []
        for key, value in attrs.items():
            if key in {"class", "for", "id_"}:
                key += "_"
            parts.append(f"{key}='{html.escape(value, quote=True)}'")
        return parts

    def convert_node(el, indent=0, air_prefix: bool = True):
        ind = "    " * indent
        if air_prefix:
            tag = f"air.{el.tag.capitalize()}"
        else:
            tag = el.tag.capitalize()

        args = []
        # Add text before children if any
        if el.text and el.text.strip():
            args.append(repr(el.text.strip()))

        # Add children recursively
        for child in el:
            args.append(convert_node(child, indent + 1, air_prefix=air_prefix))
            if child.tail and child.tail.strip():
                args.append(repr(child.tail.strip()))

        # Add attributes
        attr_args = convert_attrs(el.attrib)
        all_args = args + attr_args

        if all_args:
            if len(all_args) == 1:
                return f"{ind}{tag}(\n{all_args[0]})\n"
            else:
                joined = ",\n".join("    " * (indent + 1) + arg for arg in all_args)
                return f"{ind}{tag}(\n{joined}\n{ind})"
        else:
            return f"{ind}{tag}()"

    root = ET.fromstring(html_text)
    return convert_node(root, air_prefix=air_prefix)


def clean_html_attr_key(key: str) -> str:
    """Clean up HTML attribute keys to match the standard W3C HTML spec.

    Args:
        key: An uncleaned HTML attribute key

    Returns:

        Cleaned HTML attribute key
    """
    # If a "_"-suffixed proxy for "class", "for", or "id" is used,
    # convert it to its normal HTML equivalent.
    key = dict(class_="class", for_="for", id_="id").get(key, key)
    # Remove leading underscores and replace underscores with dashes
    return key.lstrip("_").replace("_", "-")


class Tag:
    def __init__(self, *children, **kwargs):
        """Sets four attributes, name, module, children, and attrs.
        These are important for Starlette view responses, as nested objects
        get auto-serialized to JSON and need to be rebuilt. Without
        the values of these attributes, the object reconstruction can't occur"""
        self._name = self.__class__.__name__
        self._module = self.__class__.__module__
        self._children, self._attrs = children, kwargs

    @property
    def name(self) -> str:
        return self._name.lower()

    @property
    def attrs(self) -> str:
        if not self._attrs:
            return ""
        return " " + " ".join(
            f'{clean_html_attr_key(k)}="{v}"' for k, v in self._attrs.items()
        )

    @cached_property
    def children(self):
        elements = []
        for child in self._children:
            if isinstance(child, Tag):
                elements.append(child.render())
            elif isinstance(child, SafeStr):
                elements.append(child)
            elif isinstance(child, str):
                elements.append(html.escape(child))
            elif isinstance(child, int):
                elements.append(str(child))
            else:
                # TODO: Produce a better error message
                msg = f"Unsupported child type: {type(child)}"
                msg += f"\n in tag {self.name}"
                msg += f"\n child {child}"
                msg += f"\n data {self.__dict__}"
                raise TypeError(msg)
        return "".join(elements)

    def render(self) -> str:
        return f"<{self.name}{self.attrs}>{self.children}</{self.name}>"


class CaseTag(Tag):
    """This is for case-sensitive tags like those used in SVG generation."""

    @property
    def name(self) -> str:
        return self._name[0].lower() + self._name[1:]


# Utilities


class SafeStr(str):
    """A string subclass that doesn't trigger html.escape() when called by Tag.render()

    Example:
        sample = SafeStr('Hello, world')
    """

    def __new__(cls, value):
        obj = super().__new__(cls, value)
        return obj

    def __repr__(self):
        return super().__repr__()


# Special tags


class Html(Tag):
    """Defines the root of an HTML document"""

    def render(self) -> str:
        return f"""<!doctype html><html{self.attrs}>{self.children}</html>"""


class RawHTML(Tag):
    """Renders raw HTML content without escaping.

    Args:
        html_string: A single string containing raw HTML to render

    Raises:
        TypeError: If non-string content is provided
        ValueError: If multiple arguments are provided

    Example:
        >>> RawHTML('<strong>Bold</strong> text')
        '<strong>Bold</strong> text'

        >>> # Use with other tags
        >>> Div(
        ...     P("Safe content"),
        ...     RawHTML('<hr class="divider">'),
        ...     P("More safe content")
        ... )
    """

    def __init__(self, *args, **kwargs):
        """Initialize RawHTML with a single string argument.

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("RawHTML accepts only one string argument")

        html_string = args[0] if args else ""

        if not isinstance(html_string, str):
            raise TypeError("RawHTML only accepts string content")

        super().__init__(html_string)

    def render(self) -> str:
        """Render the raw HTML string without escaping."""
        return self._children[0] if self._children else ""


class NoEscapeTag(Tag):
    """Custom tag that does not escape its children.

    This is used for tags like Script and Style where content
    should not be HTML-escaped.
    """

    def render(self) -> str:
        """Render the tag with unescaped content."""
        content = self._children[0] if self._children else ""
        return f"<{self.name}{self.attrs}>{content}</{self.name}>"


class Script(NoEscapeTag):
    """Defines a client-side script

    Warning: Script tag does not protect against code injection.
    """


class Style(NoEscapeTag):
    """Defines style information for a document

    Warning: Style tag does not protect against code injection.
    """


# HTML tag attribute map

html_attributes = {
    "A": [
        "href",
        "target",
        "download",
        "rel",
        "hreflang",
        "typereferrerpolicy",
        "media",
        "ping",
        "class_",
        "id_",
    ],
    'Audio': [
        "autoplay",
        "controls",
        "loop",
        "muted",
        "preload",
        "src",
    ],
    'Button': [
        'name',
        'type',
        'value',
        'autofocus',
        'disabled',
        'form',
        'formaction',
        'formenctype',
        'formmethod',
        'formnovalidate',
        'formtarget',
        'popovertarget',
        'popovertargetaction',
    ],
    'Canvas': [
        'width',
        'height',
    ],
    'Col': ['span'],
    'Colgroup': ['span'],
    'Data': ['value'],
    'Dd': ['cite','datetime'],
    'Details': ['open'],
    'Dialog': ['open'],
    'Embded':[
        'src',
        'type'
        'width'
        'height',
    ],
    'Fieldset': [
        'disabled',
        'form',
        'name',
    ],
    'Form': [
        'accept-charset',
        'action',
        'autocomplete',
        'enctype',
        'method',
        'name',
        'novalidate',
        'rel',
        'target',
    ],
    'Iframe': [
        'src',
        'srcdoc',
        'width',
        'height',
        'allow',
        'allowfullscreen',
        'allowpaymentrequest',
        'loading',
        'name',
        'referrerpolicy',
        'sandbox',
    ],
    'Img': [
        'src',
        'width',
        'height'
        'srcset',
        'alt',
        'crossorigin',
        'ismap',
        'loading',
        'longdesc',
        'referrerpolicy',
        'sizes'
        'usemap',
    ],
    'Input': [
        'type',
        'value',
        'readonly',
        'required',
        'accept',
        'alt',
        'autocomplete',
        'autofocus',
        'checked',
        'dirname',
        'disabled',
        'form',
        'formaction',
        'formenctype',
        'formmethod',
        'formnovalidate',
        'formtarget',
        'height',
        'list',
        'max',
        'maxlength',
        'min',
        'minlength',
        'multiple',
        'name',
        'pattern',
        'placeholder',
        'popovertarget',
        'popovertargetaction',
        'size',
        'src',
        'step',
    ]
}


def locals_cleanup(local_data, obj):
    """Converts arguments to kwargs per the html_attributes structure"""
    data = {}
    for attr in html_attributes.get(obj.__class__.__name__, []):
        if local_data.get(attr) is not None:
            data[attr] = local_data[attr]
    return data


# Stock tags


class A(Tag):
    """Defines a hyperlink"""

    def __init__(
        self,
        *children,
        href: str | None = None,
        target: str | None = None,
        download: str | None = None,
        rel: str | None = None,
        hreflang: str | None = None,
        type: str | None = None,
        referrerpolicy: str | None = None,
        media: str | None = None,
        ping: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Abbr(Tag):
    """Defines an abbreviation or an acronym"""

    pass


class Address(Tag):
    """Defines contact information for the author/owner of a document"""

    pass


class Area(Tag):
    """Defines an area inside an image map"""

    pass


class Article(Tag):
    """Defines an article"""

    pass


class Aside(Tag):
    """Defines content aside from the page content"""

    pass


class Audio(Tag):
    """Defines embedded sound content"""
    def __init__(
        self,
        *children,
        autoplay: str | None = None,
        controls: str | None = None,
        loop: str | None = None,
        muted: str | None = None,
        preload: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class B(Tag):
    """Defines bold text"""

    pass


class Base(Tag):
    """Specifies the base URL/target for all relative URLs in a document"""

    pass


class Bdi(Tag):
    """Isolates a part of text that might be formatted in a different direction from other text outside it"""

    pass


class Bdo(Tag):
    """Overrides the current text direction"""

    pass


class Blockquote(Tag):
    """Defines a section that is quoted from another source"""

    pass


class Body(Tag):
    """Defines the document's body"""

    pass


class Br(Tag):
    """Defines a single line break"""

    pass


class Button(Tag):
    """Defines a clickable button"""
    def __init__(
        self,
        *children,
        name: str | None = None,
        type: str | None = None,
        value: str | None = None,
        autofocus: str | None = None,
        disabled: str | None = None,
        form: str | None = None,
        formaction: str | None = None,
        formenctype: str | None = None,
        formmethod: str | None = None,
        formnovalidate: str | None = None,
        formtarget: str | None = None,
        popovertarget: str | None = None,
        popovertargetaction: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Canvas(Tag):
    """Used to draw graphics, on the fly, via scripting (usually JavaScript)"""
    def __init__(
        self,
        *children,
        width: str | None = None,
        height: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Caption(Tag):
    """Defines a table caption"""

    pass


class Cite(Tag):
    """Defines the title of a work"""

    pass


class Code(Tag):
    """Defines a piece of computer code"""

    pass


class Col(Tag):
    """Specifies column properties for each column within a <colgroup> element"""

    def __init__(
        self,
        *children,
        span: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))

class Colgroup(Tag):
    """Specifies a group of one or more columns in a table for formatting"""

    def __init__(
        self,
        *children,
        span: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Data(Tag):
    """Adds a machine-readable translation of a given content"""

    def __init__(
        self,
        *children,
        value: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))



class Datalist(Tag):
    """Specifies a list of pre-defined options for input controls"""

    pass


class Dd(Tag):
    """Defines a description/value of a term in a description list"""

    def __init__(
        self,
        *children,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Del(Tag):
    """Defines text that has been deleted from a document"""

    


class Details(Tag):
    """Defines additional details that the user can view or hide"""

    def __init__(
        self,
        *children,
        open: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dfn(Tag):
    """Specifies a term that is going to be defined within the content"""

    pass


class Dialog(Tag):
    """Defines a dialog box or window"""

    def __init__(
        self,
        *children,
        open: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Div(Tag):
    """Defines a section in a document"""

    pass


class Dl(Tag):
    """Defines a description list"""

    pass


class Dt(Tag):
    """Defines a term/name in a description list"""

    pass


class Em(Tag):
    """Defines emphasized text"""

    pass


class Embed(Tag):
    """Defines a container for an external application"""

    def __init__(
        self,
        *children,
        src: str | None = None,
        type: str | None = None,
        width: str | None = None,
        height: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Fieldset(Tag):
    """Groups related elements in a form"""

    def __init__(
        self,
        *children,
        disabled: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))

class Figcaption(Tag):
    """Defines a caption for a <figure> element"""

    pass


class Figure(Tag):
    """Specifies self-contained content"""

    pass


class Footer(Tag):
    """Defines a footer for a document or section"""

    pass


class Form(Tag):
    """Defines an HTML form for user input"""

    def __init__(
        self,
        *children,
        accept_charset: str | None = None,
        action: str | None = None,
        autocomplete: str | None = None,
        enctype: str | None = None,
        method: str | None = None,
        name: str | None = None,
        novalidate: str | None = None,
        rel: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))

class H1(Tag):
    """H1 header"""

    pass


class H2(Tag):
    """H2 header"""

    pass


class H3(Tag):
    """H3 header"""

    pass


class H4(Tag):
    """H4 header"""

    pass


class H5(Tag):
    """H5 header"""

    pass


class H6(Tag):
    """H6 header"""

    pass


class Head(Tag):
    """Contains metadata/information for the document"""

    pass


class Header(Tag):
    """Defines a header for a document or section"""

    pass


class Hgroup(Tag):
    """Defines a header and related content"""

    pass


class Hr(Tag):
    """Defines a thematic change in the content"""

    pass


class I(Tag):  # noqa: E742
    """Defines a part of text in an alternate voice or mood"""

    pass


class Iframe(Tag):
    """Defines an inline frame"""

    def __init__(
        self,
        *children,
        src: str | None = None,
        srcdoc: str | None = None,
        width: str | None = None,
        height: str | None = None,
        allow: str | None = None,
        allowfullscreen: str | None = None,
        allowpaymentrequest: str | None = None,
        loading: str | None = None,
        name: str | None = None,
        referrerpolicy: str | None = None,
        sandbox: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Img(Tag):
    """Defines an image"""

    def __init__(
        self,
        *children,
        src: str | None = None,
        width: str | None = None,
        height: str | None = None,
        srcset: str | None = None,
        alt: str | None = None,
        crossorigin: str | None = None,
        ismap: str | None = None,
        loading: str | None = None,
        longdesc: str | None = None,
        referrerpolicy: str | None = None,
        sizes: str | None = None,
        usemap: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Input(Tag):
    """Defines an input control"""

    def __init__(
        self,
        *children,
        type: str | None = None,
        value: str | None = None,
        readonly: str | None = None,
        required: str | None = None,    
        accept: str | None = None,
        alt: str | None = None,
        autocomplete: str | None = None,
        autofocus: str | None = None,
        checked: str | None = None,
        dirname: str | None = None,
        disabled: str | None = None,
        form: str | None = None,
        formaction: str | None = None,
        formenctype: str | None = None,
        formmethod: str | None = None,
        formnovalidate: str | None = None,
        formtarget: str | None = None,
        height: str | None = None,
        list: str | None = None,
        max: str | None = None,
        maxlength: str | None = None,
        min: str | None = None,
        minlength: str | None = None,
        multiple: str | None = None,
        name: str | None = None,
        pattern: str | None = None,
        placeholder: str | None = None,
        popovertarget: str | None = None,
        popovertargetaction: str | None = None,
        size: str | None = None,
        src: str | None = None,
        step: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ins(Tag):
    """Defines a text that has been inserted into a document"""

    pass


class Kbd(Tag):
    """Defines keyboard input"""

    pass


class Label(Tag):
    """Defines a label for an <input> element"""

    pass


class Legend(Tag):
    """Defines a caption for a <fieldset> element"""

    pass


class Li(Tag):
    """Defines a list item"""

    pass


class Link(Tag):
    """Defines the relationship between a document and an external resource (most used to link to style sheets)"""

    pass


class Main(Tag):
    """Specifies the main content of a document"""

    pass


class Map(Tag):
    """Defines an image map"""

    pass


class Mark(Tag):
    """Defines marked/highlighted text"""

    pass


class Menu(Tag):
    """Defines an unordered list"""

    pass


class Meta(Tag):
    """Defines metadata about an HTML document"""

    pass


class Meter(Tag):
    """Defines a scalar measurement within a known range (a gauge)"""

    pass


class Nav(Tag):
    """Defines navigation links"""

    pass


class Noscript(Tag):
    """Defines an alternate content for users that do not support client-side scripts"""

    pass


class Object(Tag):
    """Defines a container for an external application"""

    pass


class Ol(Tag):
    """Defines an ordered list"""

    pass


class Optgroup(Tag):
    """Defines a group of related options in a drop-down list"""

    pass


class Option(Tag):
    """Defines an option in a drop-down list"""

    pass


class Output(Tag):
    """Defines the result of a calculation"""

    pass


class P(Tag):
    """Defines a paragraph"""

    pass


class Param(Tag):
    """Defines a parameter for an object"""

    pass


class Picture(Tag):
    """Defines a container for multiple image resources"""

    pass


class Pre(Tag):
    """Defines preformatted text"""

    pass


class Progress(Tag):
    """Represents the progress of a task"""

    pass


class Q(Tag):
    """Defines a short quotation"""

    pass


class Rp(Tag):
    """Defines what to show in browsers that do not support ruby annotations"""

    pass


class Rt(Tag):
    """Defines an explanation/pronunciation of characters (for East Asian typography)"""

    pass


class Ruby(Tag):
    """Defines a ruby annotation (for East Asian typography)"""

    pass


class S(Tag):
    """Defines text that is no longer correct"""

    pass


class Samp(Tag):
    """Defines sample output from a computer program"""

    pass


class Search(Tag):
    """Defines a search section"""

    pass


class Section(Tag):
    """Defines a section in a document"""

    pass


class Select(Tag):
    """Defines a drop-down list"""

    pass


class Small(Tag):
    """Defines smaller text"""

    pass


class Source(Tag):
    """Defines multiple media resources for media elements (<video> and <audio>)"""

    pass


class Span(Tag):
    """Defines a section in a document"""

    pass


class Strong(Tag):
    """Defines important text"""

    pass


class Sub(Tag):
    """Defines subscripted text"""

    pass


class Summary(Tag):
    """Defines a visible heading for a <details> element"""

    pass


class Sup(Tag):
    """Defines superscripted text"""

    pass


class Table(Tag):
    """Defines a table"""

    pass


class Tbody(Tag):
    """Groups the body content in a table"""

    pass


class Td(Tag):
    """Defines a cell in a table"""

    pass


class Template(Tag):
    """Defines a container for content that should be hidden when the page loads"""

    pass


class Textarea(Tag):
    """Defines a multiline input control (text area)"""

    pass


class Tfoot(Tag):
    """Groups the footer content in a table"""

    pass


class Th(Tag):
    """Defines a header cell in a table"""

    pass


class Thead(Tag):
    """Groups the header content in a table"""

    pass


class Time(Tag):
    """Defines a specific time (or datetime)"""

    pass


class Title(Tag):
    """Defines a title for the document"""

    pass


class Tr(Tag):
    """Defines a row in a table"""

    pass


class Track(Tag):
    """Defines text tracks for media elements (<video> and <audio>)"""

    pass


class U(Tag):
    """Defines some text that is unarticulated and styled differently from normal text"""

    pass


class Ul(Tag):
    """Defines an unordered list"""

    pass


class Var(Tag):
    """Defines a variable"""

    pass


class Video(Tag):
    """Defines embedded video content"""

    pass


class Wbr(Tag):
    """Defines a possible line-break"""

    pass
