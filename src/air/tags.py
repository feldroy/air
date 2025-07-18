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
    key = dict(class_="class", for_="for", id_="id", as_="as").get(key, key)
    # Remove leading underscores and replace underscores with dashes
    return key.lstrip("_").replace("_", "-")


class Tag:
    self_closing = False

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
        attrs = []
        for k, v in self._attrs.items():
            if isinstance(v, bool) and v is True:
                # Add single word attribute like "selected"
                attrs.append(k)
            elif isinstance(v, bool) and v is False:
                # Skip single word attribute like "selected"
                continue
            else:
                attrs.append(f'{clean_html_attr_key(k)}="{v}"')
        return " " + " ".join(attrs)

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
            else:
                # If the type isn't supported, we just convert to `str`
                # and then escape it for safety. This matches to what most
                # template tools do, which prevents hard bugs in production
                # from stopping users cold.
                elements.append(html.escape(str(child)))
        return "".join(elements)

    def render(self) -> str:
        if self.self_closing:
            return f"<{self.name}{self.attrs} />"
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


class Raw(Tag):
    """Renders raw HTML content without escaping.

    Args:
        raw_string: A single string containing raw text to render

    Raises:
        TypeError: If non-string content is provided
        ValueError: If multiple arguments are provided

    Example:

        # Produces '<strong>Bold</strong> text'
        Raw('<strong>Bold</strong> text')

        # Use with other tags
        Div(
            P("Safe content"),
            Raw('<hr class="divider">'),
            P("More safe content")
        )
    """

    def __init__(self, *args, **kwargs):
        """Initialize Raw with a single string argument.

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("Raw accepts only one string argument")

        raw_string = args[0] if args else ""

        if not isinstance(raw_string, str):
            raise TypeError("Raw only accepts string content")

        super().__init__(raw_string)

    def render(self) -> str:
        """Render the string without escaping."""
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

    pass


class Style(NoEscapeTag):
    """Defines style information for a document

    Warning: Style tag does not protect against code injection.
    """

    pass


class Children(Tag):
    def render(self) -> str:
        return self.children


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
        "id",
    ],
    "Area": [
        "alt",
        "coords",
        "download",
        "href",
        "ping",
        "referrerpolicy",
        "rel",
        "shape",
        "target",
    ],
    "Audio": [
        "autoplay",
        "controls",
        "loop",
        "muted",
        "preload",
        "src",
    ],
    "Base": [
        "href",
        "target",
    ],
    "Bdi": [
        "dir",
    ],
    "Blockquote": [
        "cite",
    ],
    "Button": [
        "name",
        "type",
        "value",
        "autofocus",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "popovertarget",
        "popovertargetaction",
    ],
    "Canvas": [
        "width",
        "height",
    ],
    "Col": ["span"],
    "Colgroup": ["span"],
    "Data": ["value"],
    "Dd": ["cite", "datetime"],
    "Details": ["open"],
    "Dialog": ["open"],
    "Embded": [
        "src",
        "typewidthheight",
    ],
    "Fieldset": [
        "disabled",
        "form",
        "name",
    ],
    "Form": [
        "accept-charset",
        "action",
        "autocomplete",
        "enctype",
        "method",
        "name",
        "novalidate",
        "rel",
        "target",
    ],
    "Head": [
        "profile",
    ],
    "Iframe": [
        "src",
        "srcdoc",
        "width",
        "height",
        "allow",
        "allowfullscreen",
        "allowpaymentrequest",
        "loading",
        "name",
        "referrerpolicy",
        "sandbox",
    ],
    "Img": [
        "src",
        "width",
        "heightsrcset",
        "alt",
        "crossorigin",
        "ismap",
        "loading",
        "longdesc",
        "referrerpolicy",
        "sizesusemap",
    ],
    "Input": [
        "type",
        "value",
        "readonly",
        "required",
        "accept",
        "alt",
        "autocomplete",
        "autofocus",
        "checked",
        "dirname",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "height",
        "list",
        "max",
        "maxlength",
        "min",
        "minlength",
        "multiple",
        "name",
        "pattern",
        "placeholder",
        "popovertarget",
        "popovertargetaction",
        "size",
        "src",
        "step",
    ],
    "Ins": [
        "cite",
        "datetime",
    ],
    "Label": ["for"],
    "Li": [
        "value",
    ],
    "Link": [
        "href",
        "as_",
        "blocking",
        "crossorigin",
        "disabled",
        "fetchpriority",
        "hreflang",
        "imagesizes",
        "imagesrcset",
        "integrity",
        "media",
        "referrerpolicy",
        "rel",
        "sizes",
        "title",
        "type",
    ],
    "Map": [
        "name",
    ],
    "Marquee": [
        "behavior",
        "direction",
        "height",
        "width",
        "loop",
        "scrollamount",
        "scrolldelay",
        "truespeed",
        "vspace",
    ],
    "Menu": [
        "compact",
    ],
    "Meta": [
        "charset",
        "content",
        "http_equiv",
        "media",
        "name",
    ],
    "Meter": [
        "value",
        "min",
        "max",
        "low",
        "high",
        "optimum",
    ],
    "Object": [
        "archive",
        "border",
        "classidcodebase",
        "codetype",
        "data",
        "declare",
        "form",
        "height",
        "name",
        "standby",
        "type",
        "usemap",
        "width",
    ],
    "Ol": [
        "compact",
        "reversed",
        "start",
        "type",
    ],
    "Optgroup": [
        "disabled",
        "label",
    ],
    "Option": [
        "disabled",
        "label",
        "selected",
        "value",
    ],
    "Output": [
        "for_",
        "form",
        "name",
    ],
    "Pre": [
        "width",
        "wrap",
    ],
    "Progress": [
        "max",
        "value",
    ],
    "Q": [
        "cite",
    ],
    "Script": [
        "async",
        "attributionsrc",
        "blocking",
        "crossorigin",
        "defer",
        "fetchpriority",
        "integrity",
        "nomodule",
        "noncereferrerpolicy",
        "src",
        "type",
    ],
    "Select": [
        "autocomplete",
        "autofocus",
        "disabled",
        "form",
        "multiple",
        "name",
        "required",
        "size",
    ],
    "Slot": [
        "name",
    ],
    "Source": [
        "src",
        "type",
        "sizes",
        "media",
        "srcset",
        "height",
        "width",
    ],
    "Style": [
        "media",
        "nonce",
        "title",
        "blocking",
    ],
    "Td": [
        "colspan",
        "rowspan",
        "headers",
    ],
    "Template": [
        "shadowrootmode",
        "shadowrootdelegatesfocus",
        "shadowrootclonable",
        "shadowrootserializable",
    ],
    "Textarea": [
        "autocapitalize",
        "autocomplete",
        "autocorrect",
        "autofocus",
        "cols",
        "dirname",
        "disabled",
        "form",
        "maxlength",
        "minlength",
        "name",
        "placeholder",
        "readonly",
        "required",
        "rows",
        "spellcheck",
        "wrap",
    ],
    "Th": [
        "abbr",
        "colspan",
        "headers",
        "rowspan",
        "scope",
    ],
    "Time": [
        "datetime",
    ],
    "Track": [
        "default",
        "kind",
        "label",
        "srclang",
        "src",
    ],
    "Ul": [
        "compact",
        "type",
    ],
    "Video": [
        "src",
        "autoplay",
        "controls",
        "controlslist",
        "crossorigin",
        "disablepictureinpicture",
        "disableremoteplayback",
        "height",
        "width",
        "loop",
        "muted",
        "playsinline",
        "poster",
        "preload",
    ],
}


def locals_cleanup(local_data, obj):
    """Converts arguments to kwargs per the html_attributes structure"""
    data = {}
    attrs = html_attributes.get(obj.__class__.__name__, [])
    attrs += ["class_", "id"]
    for attr in attrs:
        if local_data.get(attr) is not None:
            data[attr] = local_data[attr]
    return data


# Stock tags


class A(Tag):
    """Defines a hyperlink

    Args:
        href: Specifies the URL of the page the link goes to.
        target: Specifies where to open the linked document.
        download: Specifies that the target will be downloaded when a user clicks on the hyperlink.
        rel: Specifies the relationship between the current document and the linked document.
        hreflang: Specifies the language of the linked document.
        type: Specifies the media type of the linked document.
        referrerpolicy: Specifies which referrer information to send with the link.
        media: Specifies what media/device the linked document is optimized for.
        ping: Specifies a space-separated list of URLs to which, when the link is followed, post requests with the body ping will be sent by the browser (in the background). Typically used for tracking.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Abbr(Tag):
    """Defines an abbreviation or an acronym

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Address(Tag):
    """Defines contact information for the author/owner of a document

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Area(Tag):
    """Defines an area inside an image map

    Args:
        alt: Specifies an alternate text for an area. Required if the href attribute is present.
        coords: Specifies the coordinates of an area.
        download: Specifies that the target will be downloaded when a user clicks on the hyperlink.
        href: Specifies the URL of the page the link goes to.
        ping: Specifies a space-separated list of URLs to which, when the link is followed, post requests with the body ping will be sent by the browser (in the background). Typically used for tracking.
        referrerpolicy: Specifies which referrer information to send with the link.
        rel: Specifies the relationship between the current document and the linked document.
        shape: Specifies the shape of an area.
        target: Specifies where to open the linked document.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        alt: str | None = None,
        coords: str | None = None,
        download: str | None = None,
        href: str | None = None,
        ping: str | None = None,
        referrerpolicy: str | None = None,
        rel: str | None = None,
        shape: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Article(Tag):
    """Defines an article

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Aside(Tag):
    """Defines content aside from the page content

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Audio(Tag):
    """Defines embedded sound content

    Args:
        autoplay: Specifies that the audio will start playing as soon as it is ready.
        controls: Specifies that audio controls should be displayed (such as a play/pause button etc).
        loop: Specifies that the audio will start over again, every time it is finished.
        muted: Specifies that the audio output should be muted.
        preload: Specifies if and how the author thinks the audio should be loaded when the page loads.
        src: Specifies the URL of the audio file.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class B(Tag):
    """Defines bold text

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Base(Tag):
    """Specifies the base URL/target for all relative URLs in a document

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        href: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Bdi(Tag):
    """Isolates a part of text that might be formatted in a different direction from other text outside it

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Bdo(Tag):
    """Overrides the current text direction

    Args:
        dir: Specifies the text direction of the text inside the <bdo> element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        dir: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Blockquote(Tag):
    """Defines a section that is quoted from another source

    Args:
        cite: Specifies the source of the quotation.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Body(Tag):
    """Defines the document's body

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Br(Tag):
    """Defines a single line break

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Button(Tag):
    """Defines a clickable button

    Args:
        name: Specifies a name for the button.
        type: Specifies the type of button.
        value: Specifies an initial value for the button.
        autofocus: Specifies that a button should automatically get focus when the page loads.
        disabled: Specifies that a button should be disabled.
        form: Specifies which form the button belongs to.
        formaction: Specifies where to send the form-data when a form is submitted. Only for type="submit".
        formenctype: Specifies how the form-data should be encoded before sending it to a server. Only for type="submit".
        formmethod: Specifies how to send the form-data (which HTTP method to use). Only for type="submit".
        formnovalidate: Specifies that the form-data should not be validated on submission. Only for type="submit".
        formtarget: Specifies where to display the response that is received after submitting the form. Only for type="submit".
        popovertarget: Specifies which popover element to invoke.
        popovertargetaction: Specifies what action to perform on the popover element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
    """

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
        id: str | None = None,
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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Caption(Tag):
    """Defines a table caption"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Cite(Tag):
    """Defines the title of a work"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Code(Tag):
    """Defines a piece of computer code"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Col(Tag):
    """Specifies column properties for each column within a <colgroup> element"""

    def __init__(
        self,
        *children,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Colgroup(Tag):
    """Specifies a group of one or more columns in a table for formatting"""

    def __init__(
        self,
        *children,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Datalist(Tag):
    """Specifies a list of pre-defined options for input controls"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dd(Tag):
    """Defines a description/value of a term in a description list"""

    def __init__(
        self,
        *children,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Del(Tag):
    """Defines text that has been deleted from a document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Details(Tag):
    """Defines additional details that the user can view or hide"""

    def __init__(
        self,
        *children,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dfn(Tag):
    """Specifies a term that is going to be defined within the content"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dialog(Tag):
    """Defines a dialog box or window"""

    def __init__(
        self,
        *children,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Div(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dl(Tag):
    """Defines a description list"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dt(Tag):
    """Defines a term/name in a description list"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Em(Tag):
    """Defines emphasized text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Fieldset(Tag):
    """Groups related elements in a form"""

    def __init__(
        self,
        *children,
        disabled: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figcaption(Tag):
    """Defines a caption for a <figure> element"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figure(Tag):
    """Specifies self-contained content"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Footer(Tag):
    """Defines a footer for a document or section"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H1(Tag):
    """H1 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H2(Tag):
    """H2 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H3(Tag):
    """H3 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H4(Tag):
    """H4 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H5(Tag):
    """H5 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H6(Tag):
    """H6 header"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Head(Tag):
    """Contains metadata/information for the document"""

    def __init__(
        self,
        *children,
        profile: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Header(Tag):
    """Defines a header for a document or section"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hgroup(Tag):
    """Defines a header and related content"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hr(Tag):
    """Defines a thematic change in the content"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class I(Tag):  # noqa: E742
    """Defines a part of text in an alternate voice or mood"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


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
        id: str | None = None,
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
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Input(Tag):
    """Defines an input control"""

    def __init__(
        self,
        *children,
        name: str | None = None,
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
        pattern: str | None = None,
        placeholder: str | None = None,
        popovertarget: str | None = None,
        popovertargetaction: str | None = None,
        size: str | None = None,
        src: str | None = None,
        step: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Ins(Tag):
    """Defines a text that has been inserted into a document"""

    def __init__(
        self,
        *children,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Kbd(Tag):
    """Defines keyboard input"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Label(Tag):
    """Defines a label for an <input> element"""

    def __init__(
        self,
        *children,
        for_: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Legend(Tag):
    """Defines a caption for a <fieldset> element"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Li(Tag):
    """Defines a list item"""

    def __init__(
        self,
        *children,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Link(Tag):
    """Defines the relationship between a document and an external resource (most used to link to style sheets)"""

    def __init__(
        self,
        *children,
        href: str | None = None,
        as_: str | None = None,
        blocking: str | None = None,
        crossorigin: str | None = None,
        disabled: str | None = None,
        fetchpriority: str | None = None,
        hreflang: str | None = None,
        imagesizes: str | None = None,
        imagesrcset: str | None = None,
        integrity: str | None = None,
        media: str | None = None,
        referrerpolicy: str | None = None,
        rel: str | None = None,
        sizes: str | None = None,
        title: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Main(Tag):
    """Specifies the main content of a document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Map(Tag):
    """Defines an image map"""

    def __init__(
        self,
        *children,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Mark(Tag):
    """Defines marked/highlighted text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Menu(Tag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children,
        compact: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Meta(Tag):
    """Defines metadata about an HTML document"""

    def __init__(
        self,
        *children,
        charset: str | None = None,
        content: str | None = None,
        http_equiv: str | None = None,
        media: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Meter(Tag):
    """Defines a scalar measurement within a known range (a gauge)"""

    def __init__(
        self,
        *children,
        value: str | None = None,
        min: str | None = None,
        max: str | None = None,
        low: str | None = None,
        high: str | None = None,
        optimum: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Nav(Tag):
    """Defines navigation links"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Noscript(Tag):
    """Defines an alternate content for users that do not support client-side scripts"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Object(Tag):
    """Defines a container for an external application"""

    def __init__(
        self,
        *children,
        archive: str | None = None,
        border: str | None = None,
        classid: str | None = None,
        codebase: str | None = None,
        codetype: str | None = None,
        data: str | None = None,
        declare: str | None = None,
        form: str | None = None,
        height: str | None = None,
        name: str | None = None,
        standby: str | None = None,
        type: str | None = None,
        usemap: str | None = None,
        width: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ol(Tag):
    """Defines an ordered list"""

    def __init__(
        self,
        *children,
        compact: str | None = None,
        reversed: str | None = None,
        start: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Optgroup(Tag):
    """Defines a group of related options in a drop-down list"""

    def __init__(
        self,
        *children,
        disabled: str | None = None,
        label: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Option(Tag):
    """Defines an option in a drop-down list"""

    def __init__(
        self,
        *children,
        disabled: str | None = None,
        label: str | None = None,
        selected: bool | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Output(Tag):
    """Defines the result of a calculation"""

    def __init__(
        self,
        *children,
        for_: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class P(Tag):
    """Defines a paragraph"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Param(Tag):
    """Defines a parameter for an object"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Picture(Tag):
    """Defines a container for multiple image resources"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Pre(Tag):
    """Defines preformatted text"""

    def __init__(
        self,
        *children,
        width: str | None = None,
        wrap: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Progress(Tag):
    """Represents the progress of a task"""

    def __init__(
        self,
        *children,
        max: str | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Q(Tag):
    """Defines a short quotation"""

    def __init__(
        self,
        *children,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rp(Tag):
    """Defines what to show in browsers that do not support ruby annotations"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rt(Tag):
    """Defines an explanation/pronunciation of characters (for East Asian typography)"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ruby(Tag):
    """Defines a ruby annotation (for East Asian typography)"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class S(Tag):
    """Defines text that is no longer correct"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Samp(Tag):
    """Defines sample output from a computer program"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Search(Tag):
    """Defines a search section"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Section(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Select(Tag):
    """Defines a drop-down list"""

    def __init__(
        self,
        *children,
        autocomplete: str | None = None,
        autofocus: str | None = None,
        disabled: str | None = None,
        form: str | None = None,
        multiple: str | None = None,
        name: str | None = None,
        required: str | None = None,
        size: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Small(Tag):
    """Defines smaller text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Source(Tag):
    """Defines multiple media resources for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children,
        src: str | None = None,
        type: str | None = None,
        sizes: str | None = None,
        media: str | None = None,
        srcset: str | None = None,
        height: str | None = None,
        width: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Span(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Strong(Tag):
    """Defines important text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sub(Tag):
    """Defines subscripted text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Summary(Tag):
    """Defines a visible heading for a <details> element"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sup(Tag):
    """Defines superscripted text"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Table(Tag):
    """Defines a table"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tbody(Tag):
    """Groups the body content in a table"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Td(Tag):
    """Defines a cell in a table"""

    def __init__(
        self,
        *children,
        colspan: str | None = None,
        rowspan: str | None = None,
        headers: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Template(Tag):
    """Defines a container for content that should be hidden when the page loads"""

    def __init__(
        self,
        *children,
        shadowrootmode: str | None = None,
        shadowrootdelegatesfocus: str | None = None,
        shadowrootclonable: str | None = None,
        shadowrootserializable: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Textarea(Tag):
    """Defines a multiline input control (text area)"""

    def __init__(
        self,
        *children,
        autocapitalize: str | None = None,
        autocomplete: str | None = None,
        autocorrect: str | None = None,
        autofocus: str | None = None,
        cols: str | None = None,
        dirname: str | None = None,
        disabled: str | None = None,
        form: str | None = None,
        maxlength: str | None = None,
        minlength: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        readonly: str | None = None,
        required: str | None = None,
        rows: str | None = None,
        spellcheck: str | None = None,
        wrap: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tfoot(Tag):
    """Groups the footer content in a table"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Th(Tag):
    """Defines a header cell in a table"""

    def __init__(
        self,
        *children,
        abbr: str | None = None,
        colspan: str | None = None,
        headers: str | None = None,
        rowspan: str | None = None,
        scope: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Thead(Tag):
    """Groups the header content in a table"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Time(Tag):
    """Defines a specific time (or datetime)"""

    def __init__(
        self,
        *children,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Title(Tag):
    """Defines a title for the document"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tr(Tag):
    """Defines a row in a table"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Track(Tag):
    """Defines text tracks for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children,
        default: str | None = None,
        kind: str | None = None,
        label: str | None = None,
        srclang: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class U(Tag):
    """Defines some text that is unarticulated and styled differently from normal text"""

    def __init__(
        self,
        *children,
        compact: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ul(Tag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Var(Tag):
    """Defines a variable"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Video(Tag):
    """Defines embedded video content"""

    def __init__(
        self,
        *children,
        src: str | None = None,
        autoplay: str | None = None,
        controls: str | None = None,
        controlslist: str | None = None,
        crossorigin: str | None = None,
        disablepictureinpicture: str | None = None,
        disableremoteplayback: str | None = None,
        height: str | None = None,
        width: str | None = None,
        loop: str | None = None,
        muted: str | None = None,
        playsinline: str | None = None,
        poster: str | None = None,
        preload: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Wbr(Tag):
    """Defines a possible line-break"""

    def __init__(
        self,
        *children,
        class_: str | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True
