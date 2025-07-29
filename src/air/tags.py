"""Easy to write and performant HTML content generation using Python classes to render HTML."""

import html
from functools import cached_property
from typing import Any


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
    """Base tag for all other tags.

    Sets four attributes, name, module, children, and attrs.
    These are important for Starlette view responses, as nested objects
    get auto-serialized to JSON and need to be rebuilt. With
    the values of these attributes, the object reconstruction can occur.
    """

    self_closing = False

    def __init__(self, *children: Any, **kwargs: str | int | float | bool):
        """
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
        if self.name == "tag":
            return self.children
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
        args: A single string containing raw text to render

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

    def __init__(self, *args: Any, **kwargs: str | int | float | bool):
        """Initialize Raw with a single string argument.

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("Raw accepts only one string argument")

        raw_string: str = args[0] if args else ""

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


class Tags(Tag):
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
    "Embed": [
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
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Abbr(Tag):
    """Defines an abbreviation or an acronym

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Address(Tag):
    """Defines contact information for the author/owner of a document

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Area(Tag):
    """Defines an area inside an image map

    Args:
        children: Tags, strings, or other rendered content.
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
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Article(Tag):
    """Defines an article

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Aside(Tag):
    """Defines content aside from the page content

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Audio(Tag):
    """Defines embedded sound content

    Args:
        children: Tags, strings, or other rendered content.
        autoplay: Specifies that the audio will start playing as soon as it is ready.
        controls: Specifies that audio controls should be displayed (such as a play/pause button etc).
        loop: Specifies that the audio will start over again, every time it is finished.
        muted: Specifies that the audio output should be muted.
        preload: Specifies if and how the author thinks the audio should be loaded when the page loads.
        src: Specifies the URL of the audio file.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        autoplay: str | None = None,
        controls: str | None = None,
        loop: str | None = None,
        muted: str | None = None,
        preload: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class B(Tag):
    """Defines bold text

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Base(Tag):
    """Specifies the base URL/target for all relative URLs in a document

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        href: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Bdi(Tag):
    """Isolates a part of text that might be formatted in a different direction from other text outside it

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Bdo(Tag):
    """Overrides the current text direction

    Args:
        children: Tags, strings, or other rendered content.
        dir: Specifies the text direction of the text inside the <bdo> element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        dir: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Blockquote(Tag):
    """Defines a section that is quoted from another source

    Args:
        children: Tags, strings, or other rendered content.
        cite: Specifies the source of the quotation.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Body(Tag):
    """Defines the document's body

    Args:
        children: Tags, strings, or other rendered content.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Br(Tag):
    """Defines a single line break

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Button(Tag):
    """Defines a clickable button

    Args:
        children: Tags, strings, or other rendered content.
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
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        width: str | None = None,
        height: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
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
        *children: Any,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Datalist(Tag):
    """Specifies a list of pre-defined options for input controls

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dd(Tag):
    """Defines a description/value of a term in a description list

    Args:
        children: Tags, strings, or other rendered content.
        cite: Specifies the source of the quotation.
        datetime: Specifies the date and time of the quotation.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Del(Tag):
    """Defines text that has been deleted from a document

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Details(Tag):
    """Defines additional details that the user can view or hide

    Args:
        children: Tags, strings, or other rendered content.
        open: Specifies that the details should be visible (open) to the user.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dfn(Tag):
    """Specifies a term that is going to be defined within the content

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dialog(Tag):
    """Defines a dialog box or window

    Args:
        children: Tags, strings, or other rendered content.
        open: Specifies that the dialog box should be visible (open) to the user.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Div(Tag):
    """Defines a section in a document

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dl(Tag):
    """Defines a description list

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Dt(Tag):
    """Defines a term/name in a description list

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Em(Tag):
    """Defines emphasized text

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Embed(Tag):
    """Defines a container for an external application

    Args:
        children: Tags, strings, or other rendered content.
        src: Specifies the address of the external file to embed.
        type: Specifies the media type of the embedded content.
        width: Specifies the width of the embedded content.
        height: Specifies the height of the embedded content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        src: str | None = None,
        type: str | None = None,
        width: str | None = None,
        height: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Fieldset(Tag):
    """Groups related elements in a form

    Args:
        children: Tags, strings, or other rendered content.
        disabled: Specifies that a group of related form elements should be disabled.
        form: Specifies which form the fieldset belongs to.
        name: Specifies a name for the fieldset.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        disabled: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figcaption(Tag):
    """Defines a caption for a <figure> element

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Figure(Tag):
    """Specifies self-contained content

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Footer(Tag):
    """Defines a footer for a document or section

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Form(Tag):
    """Defines an HTML form for user input

    Args:
        children: Tags, strings, or other rendered content.
        action: Specifies where to send the form-data when a form is submitted.
        method: Specifies the HTTP method to use when sending form-data.
        accept_charset: Specifies the character encodings that are to be used for the form submission.
        autocomplete: Specifies whether a form should have autocomplete on or off.
        enctype: Specifies how the form-data should be encoded when submitting it to the server.
        name: Specifies the name of the form.
        novalidate: Specifies that the form should not be validated when submitted.
        rel: Specifies the relationship between a linked resource and the current document.
        target: Specifies where to display the response that is received after submitting the form.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        action: str | None = None,
        method: str | None = None,
        accept_charset: str | None = None,
        autocomplete: str | None = None,
        enctype: str | None = None,
        name: str | None = None,
        novalidate: str | None = None,
        rel: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H1(Tag):
    """H1 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H2(Tag):
    """H2 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H3(Tag):
    """H3 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H4(Tag):
    """H4 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H5(Tag):
    """H5 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class H6(Tag):
    """H6 header

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Head(Tag):
    """Contains metadata/information for the document

    Args:
        children: Tags, strings, or other rendered content.
        profile: Specifies the URL of a document that contains a line-break-separated list of links.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        profile: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Header(Tag):
    """Defines a header for a document or section

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hgroup(Tag):
    """Defines a header and related content

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Hr(Tag):
    """Defines a thematic change in the content

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class I(Tag):  # noqa: E742
    """Defines a part of text in an alternate voice or mood

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Iframe(Tag):
    """Defines an inline frame

    Args:
        children: Tags, strings, or other rendered content.
        src: Specifies the URL of the page to embed.
        srcdoc: Specifies the HTML content of the page to show in the <iframe>.
        width: Specifies the width of an <iframe>.
        height: Specifies the height of an <iframe>.
        allow: Specifies a feature policy for the <iframe>.
        allowfullscreen: Set to true if the <iframe> can activate fullscreen mode.
        allowpaymentrequest: Set to true if a cross-origin <iframe> should be allowed to invoke the Payment Request API.
        loading: Specifies the loading policy of the <iframe>.
        name: Specifies the name of an <iframe>.
        referrerpolicy: Specifies which referrer information to send when fetching the iframe's content.
        sandbox: Enables an extra set of restrictions for the content in an <iframe>.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Img(Tag):
    """Defines an image

    Args:
        children: Tags, strings, or other rendered content.
        src: Specifies the path to the image.
        width: Specifies the width of an image.
        height: Specifies the height of an image.
        srcset: Specifies a list of image files to use in different situations.
        alt: Specifies an alternate text for an image.
        crossorigin: Allows images from third-party sites that allow cross-origin access to be used with canvas.
        ismap: Specifies an image as a server-side image map.
        loading: Specifies whether a browser should load an image immediately or to defer loading of off-screen images.
        longdesc: Specifies a URL to a detailed description of an image.
        referrerpolicy: Specifies which referrer information to use when fetching an image.
        sizes: Specifies image sizes for different page layouts.
        usemap: Specifies an image as a client-side image map.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Input(Tag):
    """Defines an input control

    Args:
        children: Tags, strings, or other rendered content.
        name: Specifies the name of an <input> element.
        type: Specifies the type <input> element to display.
        value: Specifies the value of an <input> element.
        readonly: Specifies that an input field is read-only.
        required: Specifies that an input field must be filled out before submitting the form.
        accept: Specifies a filter for what file types the user can pick from the file input dialog box.
        alt: Specifies an alternate text for images.
        autocomplete: Specifies whether an <input> element should have autocomplete on or off.
        autofocus: Specifies that an <input> element should automatically get focus when the page loads.
        checked: Specifies that an <input> element should be pre-selected when the page loads.
        dirname: Specifies that the text direction of the input field will be submitted.
        disabled: Specifies that an <input> element should be disabled.
        form: Specifies the form the <input> element belongs to.
        formaction: Specifies the URL of the file that will process the input control when the form is submitted.
        formenctype: Specifies how the form-data should be encoded when submitting it to the server.
        formmethod: Defines the HTTP method for sending data to the action URL.
        formnovalidate: Specifies that the form-data should not be validated on submission.
        formtarget: Specifies where to display the response that is received after submitting the form.
        height: Specifies the height of an <input> element.
        list: Refers to a <datalist> element that contains pre-defined options for an <input> element.
        max: Specifies the maximum value for an <input> element.
        maxlength: Specifies the maximum number of characters allowed in an <input> element.
        min: Specifies a minimum value for an <input> element.
        minlength: Specifies the minimum number of characters required in an <input> element.
        multiple: Specifies that a user can enter more than one value in an <input> element.
        pattern: Specifies a regular expression that an <input> element's value is checked against.
        placeholder: Specifies a short hint that describes the expected value of an <input> element.
        popovertarget: Specifies which popover element to invoke.
        popovertargetaction: Specifies what action to perform on the popover element.
        size: Specifies the width, in characters, of an <input> element.
        src: Specifies the URL of the image to use as a submit button.
        step: Specifies the legal number intervals for an input field.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Ins(Tag):
    """Defines a text that has been inserted into a document

    Args:
        children: Tags, strings, or other rendered content.
        cite: Specifies a URL to a document that explains the reason why the text was inserted/changed.
        datetime: Specifies the date and time when the text was inserted/changed.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Kbd(Tag):
    """Defines keyboard input

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Label(Tag):
    """Defines a label for an <input> element

    Args:
        children: Tags, strings, or other rendered content.
        for_: Specifies which form element a label is bound to.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        for_: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Legend(Tag):
    """Defines a caption for a <fieldset> element

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Li(Tag):
    """Defines a list item

    Args:
        children: Tags, strings, or other rendered content.
        value: Only for OL lists, this is the starting number of the list item.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        value: int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Link(Tag):
    """Defines the relationship between a document and an external resource (most used to link to style sheets)

    Args:
        children: Tags, strings, or other rendered content.
        href: Specifies the URL of the linked resource.
        as_: Specifies the relationship between the linked resource and the document.
        blocking: Specifies that the resource should be loaded before the rest of the page.
        crossorigin: Specifies how the element handles cross-origin requests.
        disabled: Specifies that the linked resource is disabled.
        fetchpriority: Specifies the priority for fetching the resource.
        hreflang: Specifies the language of the linked resource.
        imagesizes: Specifies the sizes of the icons for visual media.
        imagesrcset: Specifies the URLs of the icons for visual media.
        integrity: Specifies a cryptographic hash of the resource to ensure its integrity.
        media: Specifies the media type of the linked resource.
        referrerpolicy: Specifies which referrer information to send when fetching the resource.
        rel: Specifies the relationship between the current document and the linked resource.
        sizes: Specifies the size of the linked resource.
        title: Specifies the title of the linked resource.
        type: Specifies the media type of the linked resource.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Main(Tag):
    """Specifies the main content of a document

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Map(Tag):
    """Defines an image map

    Args:
        children: Tags, strings, or other rendered content.
        name: Specifies the name of the image map.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Mark(Tag):
    """Defines marked/highlighted text

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Menu(Tag):
    """Defines a menu list

    Args:
        children: Tags, strings, or other rendered content.
        compact: Specifies that the list should be displayed in a compact style.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        compact: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Meta(Tag):
    """Defines metadata about an HTML document

    Args:
        children: Tags, strings, or other rendered content.
        charset: Specifies the character encoding for the HTML document.
        content: Specifies the value associated with the http-equiv or name attribute.
        http_equiv: Provides an HTTP header for the information/value of the content attribute.
        media: Specifies what media/device the linked document is optimized for.
        name: Specifies a name for the metadata.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        charset: str | None = None,
        content: str | None = None,
        http_equiv: str | None = None,
        media: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Meter(Tag):
    """Defines a scalar measurement within a known range (a gauge)

    Args:
        children: Tags, strings, or other rendered content.
        value: The current numeric value. Must be between the min and max values.
        min: The lower bound of the measured range.
        max: The upper bound of the measured range.
        low: The upper numeric bound of the low end of the measured range.
        high: The lower numeric bound of the high end of the measured range.
        optimum: The optimal numeric value.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        value: str | None = None,
        min: str | None = None,
        max: str | None = None,
        low: str | None = None,
        high: str | None = None,
        optimum: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Nav(Tag):
    """Defines navigation links

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Noscript(Tag):
    """Defines an alternate content for users that do not support client-side scripts

    Args:
     children: Tags, strings, or other rendered content.
     class_: Substituted as the DOM `class` attribute.
     id: DOM ID attribute.
     kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Object(Tag):
    """Defines an embedded object

    Args:
        children: Tags, strings, or other rendered content.
        archive: A space-separated list of URIs for archives of resources for the object.
        border: The width of a border around the object.
        classidcodebase: The codebase URL for the object.
        codetype: The content type of the code.
        data: The address of the object's data.
        declare: Declares the object without instantiating it.
        form: The form the object belongs to.
        height: The height of the object.
        name: The name of the object.
        standby: A message to display while the object is loading.
        type: The content type of the data.
        usemap: The name of a client-side image map to be used with the object.
        width: The width of the object.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ol(Tag):
    """Defines an ordered list

    Args:
        children: Tags, strings, or other rendered content.
        compact: Specifies that the list should be rendered in a compact style.
        reversed: Specifies that the list order should be descending.
        start: Specifies the start value of an ordered list.
        type: Specifies the kind of marker to use in the list.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Any,
        compact: str | None = None,
        reversed: str | None = None,
        start: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Optgroup(Tag):
    """Defines a group of related options in a drop-down list"""

    def __init__(
        self,
        *children: Any,
        disabled: str | None = None,
        label: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Option(Tag):
    """Defines an option in a drop-down list"""

    def __init__(
        self,
        *children: Any,
        disabled: str | None = None,
        label: str | None = None,
        selected: bool | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Output(Tag):
    """Defines the result of a calculation"""

    def __init__(
        self,
        *children: Any,
        for_: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class P(Tag):
    """Defines a paragraph"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Param(Tag):
    """Defines a parameter for an object"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class Picture(Tag):
    """Defines a container for multiple image resources"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Pre(Tag):
    """Defines preformatted text"""

    def __init__(
        self,
        *children: Any,
        width: str | None = None,
        wrap: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Progress(Tag):
    """Represents the progress of a task"""

    def __init__(
        self,
        *children: Any,
        max: str | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Q(Tag):
    """Defines a short quotation"""

    def __init__(
        self,
        *children: Any,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rp(Tag):
    """Defines what to show in browsers that do not support ruby annotations"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Rt(Tag):
    """Defines an explanation/pronunciation of characters (for East Asian typography)"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ruby(Tag):
    """Defines a ruby annotation (for East Asian typography)"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class S(Tag):
    """Defines text that is no longer correct"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Samp(Tag):
    """Defines sample output from a computer program"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Search(Tag):
    """Defines a search section"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Section(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Select(Tag):
    """Defines a drop-down list"""

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Small(Tag):
    """Defines smaller text"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Source(Tag):
    """Defines multiple media resources for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children: Any,
        src: str | None = None,
        type: str | None = None,
        sizes: str | None = None,
        media: str | None = None,
        srcset: str | None = None,
        height: str | None = None,
        width: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Span(Tag):
    """Defines a section in a document"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Strong(Tag):
    """Defines important text"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sub(Tag):
    """Defines subscripted text"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Summary(Tag):
    """Defines a visible heading for a <details> element"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Sup(Tag):
    """Defines superscripted text"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Table(Tag):
    """Defines a table"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tbody(Tag):
    """Groups the body content in a table"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Td(Tag):
    """Defines a cell in a table"""

    def __init__(
        self,
        *children: Any,
        colspan: str | None = None,
        rowspan: str | None = None,
        headers: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Template(Tag):
    """Defines a container for content that should be hidden when the page loads"""

    def __init__(
        self,
        *children: Any,
        shadowrootmode: str | None = None,
        shadowrootdelegatesfocus: str | None = None,
        shadowrootclonable: str | None = None,
        shadowrootserializable: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Textarea(Tag):
    """Defines a multiline input control (text area)"""

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tfoot(Tag):
    """Groups the footer content in a table"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Th(Tag):
    """Defines a header cell in a table"""

    def __init__(
        self,
        *children: Any,
        abbr: str | None = None,
        colspan: str | None = None,
        headers: str | None = None,
        rowspan: str | None = None,
        scope: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Thead(Tag):
    """Groups the header content in a table"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Time(Tag):
    """Defines a specific time (or datetime)"""

    def __init__(
        self,
        *children: Any,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Title(Tag):
    """Defines a title for the document"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Tr(Tag):
    """Defines a row in a table"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Track(Tag):
    """Defines text tracks for media elements (<video> and <audio>)"""

    def __init__(
        self,
        *children: Any,
        default: str | None = None,
        kind: str | None = None,
        label: str | None = None,
        srclang: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True


class U(Tag):
    """Defines some text that is unarticulated and styled differently from normal text"""

    def __init__(
        self,
        *children: Any,
        compact: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Ul(Tag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Var(Tag):
    """Defines a variable"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Video(Tag):
    """Defines embedded video content"""

    def __init__(
        self,
        *children: Any,
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
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))


class Wbr(Tag):
    """Defines a possible line-break"""

    def __init__(
        self,
        *children: Any,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: str | float | int | bool,
    ):
        super().__init__(*children, **kwargs | locals_cleanup(locals(), self))
        self.self_closing = True
