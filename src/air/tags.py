"""Adds s-expression HTML tags to air."""

import html
from functools import cached_property
from typing import Optional
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
        get auto-serialized to JSON and need to be rebuilt. With
        the values of these attributes, the object reconstruction can occur.

        Args:
            children: Tags, strings, or other rendered content.
            kwargs: Keyword arguments transformed into tag attributes.
        """
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
    attrs += ["class_", "id", "style"]
    for attr in attrs:
        if local_data.get(attr) is not None:
            data[attr] = local_data[attr]
    return data


# Stock tags


class A(Tag):
    """Defines a hyperlink

    Args:
        children: Tags, strings, or other rendered content.
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
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        href: Optional[str] = None,
        target: Optional[str] = None,
        download: Optional[str] = None,
        rel: Optional[str] = None,
        hreflang: Optional[str] = None,
        type: Optional[str] = None,
        referrerpolicy: Optional[str] = None,
        media: Optional[str] = None,
        ping: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Abbr(Tag):
    """Defines an abbreviation or an acronym

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Address(Tag):
    """Defines contact information for the author/owner of a document

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
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
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        alt: Optional[str] = None,
        coords: Optional[str] = None,
        download: Optional[str] = None,
        href: Optional[str] = None,
        ping: Optional[str] = None,
        referrerpolicy: Optional[str] = None,
        rel: Optional[str] = None,
        shape: Optional[str] = None,
        target: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Article(Tag):
    """Defines an article

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Aside(Tag):
    """Defines content aside from the page content

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
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
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        autoplay: Optional[str] = None,
        controls: Optional[str] = None,
        loop: Optional[str] = None,
        muted: Optional[str] = None,
        preload: Optional[str] = None,
        src: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class B(Tag):
    """Defines bold text

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Base(Tag):
    """Specifies the base URL/target for all relative URLs in a document

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        href: Optional[str] = None,
        target: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Bdi(Tag):
    """Isolates a part of text that might be formatted in a different direction from other text outside it

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Bdo(Tag):
    """Overrides the current text direction

    Args:
        dir: Specifies the text direction of the text inside the <bdo> element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        dir: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Blockquote(Tag):
    """Defines a section that is quoted from another source

    Args:
        cite: Specifies the source of the quotation.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        cite: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Body(Tag):
    """Defines the document's body

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Br(Tag):
    """Defines a single line break

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
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
        style: Inline style attribute.
    """

    def __init__(
        self,
        *children,
        name: Optional[str] = None,
        type: Optional[str] = None,
        value: Optional[str] = None,
        autofocus: Optional[str] = None,
        disabled: Optional[str] = None,
        form: Optional[str] = None,
        formaction: Optional[str] = None,
        formenctype: Optional[str] = None,
        formmethod: Optional[str] = None,
        formnovalidate: Optional[str] = None,
        formtarget: Optional[str] = None,
        popovertarget: Optional[str] = None,
        popovertargetaction: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Canvas(Tag):
    """Used to draw graphics, on the fly, via scripting (usually JavaScript)

    Args:
        children: Tags, strings, or other rendered content.
        width: Specifies the width of the canvas.
        height: Specifies the height of the canvas.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        width: Optional[str] = None,
        height: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Caption(Tag):
    """Defines a table caption

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Cite(Tag):
    """Defines the title of a work

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Code(Tag):
    """Defines a piece of computer code

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Col(Tag):
    """Specifies column properties for each column within a <colgroup> element

    Args:
        children: Tags, strings, or other rendered content.
        span: Specifies the number of columns a <col> element should span.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        span: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Colgroup(Tag):
    """Specifies a group of one or more columns in a table for formatting

    Args:
        children: Tags, strings, or other rendered content.
        span: Specifies the number of columns a <colgroup> element should span.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        span: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Data(Tag):
    """Adds a machine-readable translation of a given content

    Args:
        children: Tags, strings, or other rendered content.
        value: Specifies the machine-readable translation of the content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children,
        value: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Datalist(Tag):
    """Specifies a list of pre-defined options for input controls"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dd(Tag):
    """Defines a description/value of a term in a description list"""

    def __init__(
        self,
        *children,
        cite: Optional[str] = None,
        datetime: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Del(Tag):
    """Defines text that has been deleted from a document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Details(Tag):
    """Defines additional details that the user can view or hide"""

    def __init__(
        self,
        *children,
        open: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dfn(Tag):
    """Specifies a term that is going to be defined within the content"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dialog(Tag):
    """Defines a dialog box or window"""

    def __init__(
        self,
        *children,
        open: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Div(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dl(Tag):
    """Defines a description list"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dt(Tag):
    """Defines a term/name in a description list"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Em(Tag):
    """Defines emphasized text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Embed(Tag):
    """Defines a container for an external application"""

    def __init__(
        self,
        *children,
        src: Optional[str] = None,
        type: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Fieldset(Tag):
    """Groups related elements in a form"""

    def __init__(
        self,
        *children,
        disabled: Optional[str] = None,
        form: Optional[str] = None,
        name: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figcaption(Tag):
    """Defines a caption for a <figure> element"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figure(Tag):
    """Specifies self-contained content"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Footer(Tag):
    """Defines a footer for a document or section"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Form(Tag):
    """Defines an HTML form for user input"""

    def __init__(
        self,
        *children,
        accept_charset: Optional[str] = None,
        action: Optional[str] = None,
        autocomplete: Optional[str] = None,
        enctype: Optional[str] = None,
        method: Optional[str] = None,
        name: Optional[str] = None,
        novalidate: Optional[str] = None,
        rel: Optional[str] = None,
        target: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H1(Tag):
    """H1 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H2(Tag):
    """H2 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H3(Tag):
    """H3 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H4(Tag):
    """H4 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H5(Tag):
    """H5 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H6(Tag):
    """H6 header"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Head(Tag):
    """Contains metadata/information for the document"""

    def __init__(
        self,
        *children,
        profile: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Header(Tag):
    """Defines a header for a document or section"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hgroup(Tag):
    """Defines a header and related content"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hr(Tag):
    """Defines a thematic change in the content"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class I(Tag):  # noqa: E742
    """Defines a part of text in an alternate voice or mood"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Iframe(Tag):
    """Defines an inline frame"""

    def __init__(
        self,
        *children,
        src: Optional[str] = None,
        srcdoc: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        allow: Optional[str] = None,
        allowfullscreen: Optional[str] = None,
        allowpaymentrequest: Optional[str] = None,
        loading: Optional[str] = None,
        name: Optional[str] = None,
        referrerpolicy: Optional[str] = None,
        sandbox: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Img(Tag):
    """Defines an image"""

    def __init__(
        self,
        *children,
        src: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        srcset: Optional[str] = None,
        alt: Optional[str] = None,
        crossorigin: Optional[str] = None,
        ismap: Optional[str] = None,
        loading: Optional[str] = None,
        longdesc: Optional[str] = None,
        referrerpolicy: Optional[str] = None,
        sizes: Optional[str] = None,
        usemap: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Input(Tag):
    """Defines an input control"""

    def __init__(
        self,
        *children,
        name: Optional[str] = None,
        type: Optional[str] = None,
        value: Optional[str] = None,
        readonly: Optional[str] = None,
        required: Optional[str] = None,
        accept: Optional[str] = None,
        alt: Optional[str] = None,
        autocomplete: Optional[str] = None,
        autofocus: Optional[str] = None,
        checked: Optional[str] = None,
        dirname: Optional[str] = None,
        disabled: Optional[str] = None,
        form: Optional[str] = None,
        formaction: Optional[str] = None,
        formenctype: Optional[str] = None,
        formmethod: Optional[str] = None,
        formnovalidate: Optional[str] = None,
        formtarget: Optional[str] = None,
        height: Optional[str] = None,
        list: Optional[str] = None,
        max: Optional[str] = None,
        maxlength: Optional[str] = None,
        min: Optional[str] = None,
        minlength: Optional[str] = None,
        multiple: Optional[str] = None,
        pattern: Optional[str] = None,
        placeholder: Optional[str] = None,
        popovertarget: Optional[str] = None,
        popovertargetaction: Optional[str] = None,
        size: Optional[str] = None,
        src: Optional[str] = None,
        step: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Ins(Tag):
    """Defines a text that has been inserted into a document"""

    def __init__(
        self,
        *children,
        cite: Optional[str] = None,
        datetime: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Kbd(Tag):
    """Defines keyboard input"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Label(Tag):
    """Defines a label for an <input> element"""

    def __init__(
        self,
        *children,
        for_: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Legend(Tag):
    """Defines a caption for a <fieldset> element"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Li(Tag):
    """Defines a list item"""

    def __init__(
        self,
        *children,
        value: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Link(Tag):
    """Defines the relationship between a document and an external resource (most used to link to style sheets)"""

    def __init__(
        self,
        *children,
        href: Optional[str] = None,
        as_: Optional[str] = None,
        blocking: Optional[str] = None,
        crossorigin: Optional[str] = None,
        disabled: Optional[str] = None,
        fetchpriority: Optional[str] = None,
        hreflang: Optional[str] = None,
        imagesizes: Optional[str] = None,
        imagesrcset: Optional[str] = None,
        integrity: Optional[str] = None,
        media: Optional[str] = None,
        referrerpolicy: Optional[str] = None,
        rel: Optional[str] = None,
        sizes: Optional[str] = None,
        title: Optional[str] = None,
        type: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Main(Tag):
    """Specifies the main content of a document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Map(Tag):
    """Defines an image map"""

    def __init__(
        self,
        *children,
        name: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Mark(Tag):
    """Defines marked/highlighted text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Menu(Tag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children,
        compact: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Meta(Tag):
    """Defines metadata about an HTML document"""

    def __init__(
        self,
        *children,
        charset: Optional[str] = None,
        content: Optional[str] = None,
        http_equiv: Optional[str] = None,
        media: Optional[str] = None,
        name: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Meter(Tag):
    """Defines a scalar measurement within a known range (a gauge)"""

    def __init__(
        self,
        *children,
        value: Optional[str] = None,
        min: Optional[str] = None,
        max: Optional[str] = None,
        low: Optional[str] = None,
        high: Optional[str] = None,
        optimum: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Nav(Tag):
    """Defines navigation links"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Noscript(Tag):
    """Defines an alternate content for users that do not support client-side scripts"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Object(Tag):
    """Defines a container for an external application"""

    def __init__(
        self,
        *children,
        archive: Optional[str] = None,
        border: Optional[str] = None,
        classid: Optional[str] = None,
        codebase: Optional[str] = None,
        codetype: Optional[str] = None,
        data: Optional[str] = None,
        declare: Optional[str] = None,
        form: Optional[str] = None,
        height: Optional[str] = None,
        name: Optional[str] = None,
        standby: Optional[str] = None,
        type: Optional[str] = None,
        usemap: Optional[str] = None,
        width: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ol(Tag):
    """Defines an ordered list"""

    def __init__(
        self,
        *children,
        compact: Optional[str] = None,
        reversed: Optional[str] = None,
        start: Optional[str] = None,
        type: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Optgroup(Tag):
    """Defines a group of related options in a drop-down list"""

    def __init__(
        self,
        *children,
        disabled: Optional[str] = None,
        label: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Option(Tag):
    """Defines an option in a drop-down list"""

    def __init__(
        self,
        *children,
        disabled: Optional[str] = None,
        label: Optional[str] = None,
        selected: bool | None = None,
        value: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Output(Tag):
    """Defines the result of a calculation"""

    def __init__(
        self,
        *children,
        for_: Optional[str] = None,
        form: Optional[str] = None,
        name: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class P(Tag):
    """Defines a paragraph"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Param(Tag):
    """Defines a parameter for an object"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Picture(Tag):
    """Defines a container for multiple image resources"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Pre(Tag):
    """Defines preformatted text"""

    def __init__(
        self,
        *children,
        width: Optional[str] = None,
        wrap: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Progress(Tag):
    """Represents the progress of a task"""

    def __init__(
        self,
        *children,
        max: Optional[str] = None,
        value: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Q(Tag):
    """Defines a short quotation"""

    def __init__(
        self,
        *children,
        cite: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rp(Tag):
    """Defines what to show in browsers that do not support ruby annotations"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rt(Tag):
    """Defines an explanation/pronunciation of characters (for East Asian typography)"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ruby(Tag):
    """Defines a ruby annotation (for East Asian typography)"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class S(Tag):
    """Defines text that is no longer correct"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Samp(Tag):
    """Defines sample output from a computer program"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Search(Tag):
    """Defines a search section"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Section(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Select(Tag):
    """Defines a drop-down list"""

    def __init__(
        self,
        *children,
        autocomplete: Optional[str] = None,
        autofocus: Optional[str] = None,
        disabled: Optional[str] = None,
        form: Optional[str] = None,
        multiple: Optional[str] = None,
        name: Optional[str] = None,
        required: Optional[str] = None,
        size: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Small(Tag):
    """Defines smaller text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Source(Tag):
    """Defines multiple media resources for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children,
        src: Optional[str] = None,
        type: Optional[str] = None,
        sizes: Optional[str] = None,
        media: Optional[str] = None,
        srcset: Optional[str] = None,
        height: Optional[str] = None,
        width: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Span(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Strong(Tag):
    """Defines important text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sub(Tag):
    """Defines subscripted text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Summary(Tag):
    """Defines a visible heading for a <details> element"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sup(Tag):
    """Defines superscripted text"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Table(Tag):
    """Defines a table"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tbody(Tag):
    """Groups the body content in a table"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Td(Tag):
    """Defines a cell in a table"""

    def __init__(
        self,
        *children,
        colspan: Optional[str] = None,
        rowspan: Optional[str] = None,
        headers: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Template(Tag):
    """Defines a container for content that should be hidden when the page loads"""

    def __init__(
        self,
        *children,
        shadowrootmode: Optional[str] = None,
        shadowrootdelegatesfocus: Optional[str] = None,
        shadowrootclonable: Optional[str] = None,
        shadowrootserializable: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Textarea(Tag):
    """Defines a multiline input control (text area)"""

    def __init__(
        self,
        *children,
        autocapitalize: Optional[str] = None,
        autocomplete: Optional[str] = None,
        autocorrect: Optional[str] = None,
        autofocus: Optional[str] = None,
        cols: Optional[str] = None,
        dirname: Optional[str] = None,
        disabled: Optional[str] = None,
        form: Optional[str] = None,
        maxlength: Optional[str] = None,
        minlength: Optional[str] = None,
        name: Optional[str] = None,
        placeholder: Optional[str] = None,
        readonly: Optional[str] = None,
        required: Optional[str] = None,
        rows: Optional[str] = None,
        spellcheck: Optional[str] = None,
        wrap: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tfoot(Tag):
    """Groups the footer content in a table"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Th(Tag):
    """Defines a header cell in a table"""

    def __init__(
        self,
        *children,
        abbr: Optional[str] = None,
        colspan: Optional[str] = None,
        headers: Optional[str] = None,
        rowspan: Optional[str] = None,
        scope: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Thead(Tag):
    """Groups the header content in a table"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Time(Tag):
    """Defines a specific time (or datetime)"""

    def __init__(
        self,
        *children,
        datetime: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Title(Tag):
    """Defines a title for the document"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tr(Tag):
    """Defines a row in a table"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Track(Tag):
    """Defines text tracks for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children,
        default: Optional[str] = None,
        kind: Optional[str] = None,
        label: Optional[str] = None,
        srclang: Optional[str] = None,
        src: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class U(Tag):
    """Defines some text that is unarticulated and styled differently from normal text"""

    def __init__(
        self,
        *children,
        compact: Optional[str] = None,
        type: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ul(Tag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Var(Tag):
    """Defines a variable"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Video(Tag):
    """Defines embedded video content"""

    def __init__(
        self,
        *children,
        src: Optional[str] = None,
        autoplay: Optional[str] = None,
        controls: Optional[str] = None,
        controlslist: Optional[str] = None,
        crossorigin: Optional[str] = None,
        disablepictureinpicture: Optional[str] = None,
        disableremoteplayback: Optional[str] = None,
        height: Optional[str] = None,
        width: Optional[str] = None,
        loop: Optional[str] = None,
        muted: Optional[str] = None,
        playsinline: Optional[str] = None,
        poster: Optional[str] = None,
        preload: Optional[str] = None,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Wbr(Tag):
    """Defines a possible line-break"""

    def __init__(
        self,
        *children,
        class_: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True
