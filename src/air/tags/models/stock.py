"""Default tags, mostly found within the official HTML specification.

Script and Style tags can be found in the [air.tags.models.special](/reference/air.tags.models.special) page."""

from ..utils import locals_cleanup
from .base import AttributeType, BaseTag, Renderable
from .special import SelfClosingTag


class A(BaseTag):
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
        *children: Renderable,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Abbr(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Address(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Area(SelfClosingTag):
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
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Article(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Aside(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Audio(BaseTag):
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
        *children: Renderable,
        autoplay: str | None = None,
        controls: str | None = None,
        loop: str | None = None,
        muted: str | None = None,
        preload: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class B(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Base(SelfClosingTag):
    """Specifies the base URL/target for all relative URLs in a document

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        href: str | None = None,
        target: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Bdi(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Bdo(BaseTag):
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
        *children: Renderable,
        dir: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Blockquote(BaseTag):
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
        *children: Renderable,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Body(BaseTag):
    """Defines the document's body

    Args:
        children: Tags, strings, or other rendered content.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Br(SelfClosingTag):
    """Defines a single line break

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Button(BaseTag):
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
        *children: Renderable,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Canvas(BaseTag):
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
        *children: Renderable,
        width: str | int | None = None,
        height: str | int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Caption(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Cite(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Code(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Col(SelfClosingTag):
    """Specifies column properties for each column within a <colgroup> element

    Args:
        span: Specifies the number of columns a <col> element should span.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Colgroup(BaseTag):
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
        *children: Renderable,
        span: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Data(BaseTag):
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
        *children: Renderable,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Datalist(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Dd(BaseTag):
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
        *children: Renderable,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Del(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Details(BaseTag):
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
        *children: Renderable,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Dfn(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Dialog(BaseTag):
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
        *children: Renderable,
        open: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Div(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Dl(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Dt(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Em(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Embed(SelfClosingTag):
    """Defines a container for an external application

    Args:
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
        *,
        src: str | None = None,
        type: str | None = None,
        width: str | int | None = None,
        height: str | int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Fieldset(BaseTag):
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
        *children: Renderable,
        disabled: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Figcaption(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Figure(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Footer(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Form(BaseTag):
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
        *children: Renderable,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H1(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H2(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H3(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H4(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H5(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class H6(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Head(BaseTag):
    """Contains metadata/information for the document

    Args:
        children: Tags, strings, or other rendered content.
        profile: Specifies the URL of a document that contains a line-break-separated list of links.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        profile: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Header(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Hgroup(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Hr(SelfClosingTag):
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
        *,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class I(BaseTag):  # noqa: E742
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Iframe(BaseTag):
    """Defines an inline frame

    Args:
        children: Tags, strings, or other rendered content.
        src: Specifies the URL of the page to embed.
        srcdoc: Specifies the HTML content of the page to show in the `<iframe>`.
        width: Specifies the width of an `<iframe>`.
        height: Specifies the height of an `<iframe>`.
        allow: Specifies a feature policy for the `<iframe>`.
        allowfullscreen: Set to true if the `<iframe>` can activate fullscreen mode.
        allowpaymentrequest: Set to true if a cross-origin `<iframe>` should be allowed to invoke the Payment Request API.
        loading: Specifies the loading policy of the `<iframe>`.
        name: Specifies the name of an `<iframe>`.
        referrerpolicy: Specifies which referrer information to send when fetching the iframe's content.
        sandbox: Enables an extra set of restrictions for the content in an `<iframe>`.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        src: str | None = None,
        srcdoc: str | None = None,
        width: str | int | None = None,
        height: str | int | None = None,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Img(SelfClosingTag):
    """Defines an image

    Args:
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
        *,
        src: str | None = None,
        width: str | int | None = None,
        height: str | int | None = None,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Input(SelfClosingTag):
    """Defines an input control

    Args:
        name: Specifies the name of an `<input>` element.
        type: Specifies the type `<input>` element to display.
        value: Specifies the value of an `<input>` element.
        readonly: Specifies that an input field is read-only.
        required: Specifies that an input field must be filled out before submitting the form.
        accept: Specifies a filter for what file types the user can pick from the file input dialog box.
        alt: Specifies an alternate text for images.
        autocomplete: Specifies whether an `<input>` element should have autocomplete on or off.
        autofocus: Specifies that an `<input>` element should automatically get focus when the page loads.
        checked: Specifies that an `<input>` element should be pre-selected when the page loads.
        dirname: Specifies that the text direction of the input field will be submitted.
        disabled: Specifies that an `<input>` element should be disabled.
        form: Specifies the form the `<input>` element belongs to.
        formaction: Specifies the URL of the file that will process the input control when the form is submitted.
        formenctype: Specifies how the form-data should be encoded when submitting it to the server.
        formmethod: Defines the HTTP method for sending data to the action URL.
        formnovalidate: Specifies that the form-data should not be validated on submission.
        formtarget: Specifies where to display the response that is received after submitting the form.
        height: Specifies the height of an `<input>` element.
        list: Refers to a <datalist> element that contains pre-defined options for an `<input>` element.
        max: Specifies the maximum value for an `<input>` element.
        maxlength: Specifies the maximum number of characters allowed in an `<input>` element.
        min: Specifies a minimum value for an `<input>` element.
        minlength: Specifies the minimum number of characters required in an `<input>` element.
        multiple: Specifies that a user can enter more than one value in an `<input>` element.
        pattern: Specifies a regular expression that an `<input>` element's value is checked against.
        placeholder: Specifies a short hint that describes the expected value of an `<input>` element.
        popovertarget: Specifies which popover element to invoke.
        popovertargetaction: Specifies what action to perform on the popover element.
        size: Specifies the width, in characters, of an `<input>` element.
        src: Specifies the URL of the image to use as a submit button.
        step: Specifies the legal number intervals for an input field.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        type: str | None = None,
        value: str | None = None,
        readonly: bool | None = None,
        required: bool | None = None,
        accept: str | None = None,
        alt: str | None = None,
        autocomplete: str | None = None,
        autofocus: bool | None = None,
        checked: bool | None = None,
        dirname: str | None = None,
        disabled: bool | None = None,
        form: str | None = None,
        formaction: str | None = None,
        formenctype: str | None = None,
        formmethod: str | None = None,
        formnovalidate: bool | None = None,
        formtarget: str | None = None,
        height: str | int | None = None,
        list: str | None = None,
        max: str | None = None,
        maxlength: str | None = None,
        min: str | None = None,
        minlength: str | None = None,
        multiple: bool | None = None,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Ins(BaseTag):
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
        *children: Renderable,
        cite: str | None = None,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Kbd(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Label(BaseTag):
    """Defines a label for an `<input>` element

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
        *children: Renderable,
        for_: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Legend(BaseTag):
    """Defines a caption for a `<fieldset>` element

    Args:
         children: Tags, strings, or other rendered content.
         class_: Substituted as the DOM `class` attribute.
         id: DOM ID attribute.
         style: Inline style attribute.
         kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Li(BaseTag):
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
        *children: Renderable,
        value: int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Link(SelfClosingTag):
    """Defines the relationship between a document and an external resource (most used to link to style sheets)

    Args:
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
        *,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Main(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Map(BaseTag):
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
        *children: Renderable,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Mark(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Menu(BaseTag):
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
        *children: Renderable,
        compact: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Meta(SelfClosingTag):
    """Defines metadata about an HTML document

    Args:
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
        *,
        charset: str | None = None,
        content: str | None = None,
        http_equiv: str | None = None,
        media: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Meter(BaseTag):
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
        *children: Renderable,
        value: str | None = None,
        min: str | None = None,
        max: str | None = None,
        low: str | None = None,
        high: str | None = None,
        optimum: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Nav(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Noscript(BaseTag):
    """Defines an alternate content for users that do not support client-side scripts

    Args:
     children: Tags, strings, or other rendered content.
     class_: Substituted as the DOM `class` attribute.
     id: DOM ID attribute.
     kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Object(BaseTag):
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
        *children: Renderable,
        archive: str | None = None,
        border: str | None = None,
        classid: str | None = None,
        codebase: str | None = None,
        codetype: str | None = None,
        data: str | None = None,
        declare: str | None = None,
        form: str | None = None,
        height: str | int | None = None,
        name: str | None = None,
        standby: str | None = None,
        type: str | None = None,
        usemap: str | None = None,
        width: str | int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Ol(BaseTag):
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
        *children: Renderable,
        compact: str | None = None,
        reversed: str | None = None,
        start: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Optgroup(BaseTag):
    """Defines a group of related options in a drop-down list

    Args:
        children: Tags, strings, or other rendered content.
        disabled: Indicates if items in the option group are not selectable.
        label: Specifies a label for the group of options.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        disabled: str | None = None,
        label: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Option(BaseTag):
    """Defines an option in a drop-down list

    Args:
        children: Tags, strings, or other rendered content.
        disabled: Indicates if the option is not selectable.
        label: Specifies a label for the option indicating the meaning of the option.
        selected: Specifies that the option should be pre-selected.
        value: Specifies the value to be sent with the form.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        disabled: str | None = None,
        label: str | None = None,
        selected: bool | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Output(BaseTag):
    """Defines the result of a calculation

    Args:
        children: Tags, strings, or other rendered content.
        for_: Lists the IDs of the elements that contributed to the calculation.
        form: Associates the output with a form element.
        name: Defines a name for the output element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        for_: str | None = None,
        form: str | None = None,
        name: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class P(BaseTag):
    """Defines a paragraph

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Param(SelfClosingTag):
    """Defines a parameter for an object

    Args:
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class Picture(BaseTag):
    """Defines a container for multiple image resources

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Pre(BaseTag):
    """Defines preformatted text

    Args:
        children: Tags, strings, or other rendered content.
        width: preferred counf of characters that a line should have
        wrap: hint indicating how overflow must happen
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        width: str | int | None = None,
        wrap: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Progress(BaseTag):
    """Represents the progress of a task

    Args:
        children: Tags, strings, or other rendered content.
        max: The maximum value of the progress bar.
        value: The current value of the progress bar.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        max: str | None = None,
        value: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Q(BaseTag):
    """Defines a short quotation

    Args:
        children: Tags, strings, or other rendered content.
        cite: Specifies a URL to the source of the quotation.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        cite: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Rp(BaseTag):
    """Defines what to show in browsers that do not support ruby annotations

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Rt(BaseTag):
    """Defines an explanation/pronunciation of characters (for East Asian typography)

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Ruby(BaseTag):
    """Defines a ruby annotation (for East Asian typography)

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class S(BaseTag):
    """Defines text that is no longer correct

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Samp(BaseTag):
    """Defines sample output from a computer program

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Search(BaseTag):
    """Defines a search section

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Section(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Select(BaseTag):
    """Defines a drop-down list

    Args:
        children: Tags, strings, or other rendered content.
        autocomplete: Hint for a user agent's autocomplete feature.
        autofocus: Indicate that a form control should have input focus when the page loads.
        disabled: Indicates that the user cannot interact with the control.
        form: Associates the drop-down list with a form element.
        multiple: Indicates that multiple options can be selected at once.
        name: Specifies the name of the drop-down list.
        required: Indicates that an option must be selected before the form can be submitted.
        size: If drop-down list is a scrolling list box, specifies the number of visible options.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Small(BaseTag):
    """Defines smaller text

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Source(BaseTag):
    """Defines multiple media resources for media elements (<video> and <audio>)

    Args:
        children: Tags, strings, or other rendered content.
        src: Specifies the URL of the media resource.
        type: Specifies the MIME type of the media resource.
        sizes: List of source sizes that describe the final rendered width of the image.
        media: Specifies the media query for the media resource.
        srcset: Specifies a list of one or more image URLs and their descriptors.
        height: Specifies the height of the media resource.
        width: Specifies the width of the media resource.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        src: str | None = None,
        type: str | None = None,
        sizes: str | None = None,
        media: str | None = None,
        srcset: str | None = None,
        height: str | int | None = None,
        width: str | int | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Span(BaseTag):
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
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Strong(BaseTag):
    """Defines important text

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Sub(BaseTag):
    """Defines subscripted text

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Summary(BaseTag):
    """Defines a visible heading for a <details> element

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Sup(BaseTag):
    """Defines superscripted text

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Table(BaseTag):
    """Defines a table

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Tbody(BaseTag):
    """Groups the body content in a table

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Td(BaseTag):
    """Defines a cell in a table

    Args:
        children: Tags, strings, or other rendered content.
        colspan: Defines the number of columns a cell should span.
        rowspan: Defines the number of rows a cell should span.
        headers: list of string ids of the `<th>` elements that apply to the cell
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        colspan: str | None = None,
        rowspan: str | None = None,
        headers: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Template(BaseTag):
    """Defines a container for content that should be hidden when the page loads

    Args:
        children: Tags, strings, or other rendered content.
        shadowrootmode: Creates a shadow root for the parent element.
        shadowrootdelegatesfocus: Sets whether the shadow root created delegates focus.
        shadowrootclonable: Sets the value of the 'cloneable' property on the shadow root.
        shadowrootserializable: Sets the value of the 'serializable' property on the shadow root.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        shadowrootmode: str | None = None,
        shadowrootdelegatesfocus: str | None = None,
        shadowrootclonable: str | None = None,
        shadowrootserializable: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Textarea(BaseTag):
    """Defines a multiline input control (text area)

    Args:
        children: Tags, strings, or other rendered content.
        autocapitalize: Determines whether inputted text is automatically capitalized.
        autocomplete: Controls whether inputted text can be automatically completed by the browser.
        autocorrect: Controls whether autocorrect is enabled on the input text.
        autofocus: Indicates that the text area should have input focus when the page loads.
        cols: Defines the visible width of the text area in average character widths.
        dirname: Indicates text directionality of the element contents.
        disabled: Determines if the user can interact with the text area.
        form: Associates the text area with a form element.
        maxlength: Defines the maximum number of characters allowed in the text area.
        minlength: Defines the minimum number of characters required in the text area.
        name: The name of the element.
        placeholder: Provides a hint to the user of what can be entered in the text area.
        readonly: Indicates that the user may not edit the value of the text area.
        required: Specifies that the text area must be filled out before submitting the form.
        rows: Defines the visible number of lines for the control.
        spellcheck: Specifies if the element is subject to browser or OS spell-check.
        wrap: Indicates how the text area handles line wrapping.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        autocapitalize: str | None = None,
        autocomplete: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        cols: str | None = None,
        dirname: str | None = None,
        disabled: bool | None = None,
        form: str | None = None,
        maxlength: str | None = None,
        minlength: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        readonly: bool | None = None,
        required: bool | None = None,
        rows: str | None = None,
        spellcheck: str | None = None,
        wrap: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Tfoot(BaseTag):
    """Groups the footer content in a table

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Th(BaseTag):
    """Defines a header cell in a table

    Args:
        children: Tags, strings, or other rendered content.
        abbr: An abbreviated description of the header cell content.
        colspan: Defines the number of columns a header cell should span.
        headers: list of string ids of the `<th>` elements that provide the headers for the cell.
        rowspan: Defines the number of rows a header cell should span.
        scope: Specifies whether the header cell is a header for a column, row, or group of columns or rows.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        abbr: str | None = None,
        colspan: str | None = None,
        headers: str | None = None,
        rowspan: str | None = None,
        scope: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Thead(BaseTag):
    """Groups the header content in a table

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Time(BaseTag):
    """Defines a specific time (or datetime)

    Args:
        children: Tags, strings, or other rendered content.
        datetime: Specifies the date and/or time format.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        datetime: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Title(BaseTag):
    """Defines a title for the document

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Tr(BaseTag):
    """Defines a row in a table

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Track(SelfClosingTag):
    """Defines text tracks for media elements (<video> and <audio>)

    Args:
        default: Indicates that the track is to be enabled if the user's preferences do not indicate any.
        kind: Specifies how the text track is meant to be used.
        label: Provides a user-readable title for the text track.
        srclang: Specifies the language of the text track data.
        src: Specifies the URL of the track file.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    def __init__(
        self,
        *,
        default: str | None = None,
        kind: str | None = None,
        label: str | None = None,
        srclang: str | None = None,
        src: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))


class U(BaseTag):
    """Defines some text that is unarticulated and styled differently from normal text"""

    def __init__(
        self,
        *children: Renderable,
        compact: str | None = None,
        type: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Ul(BaseTag):
    """Defines an unordered list"""

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Var(BaseTag):
    """Defines a variable"""

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Video(BaseTag):
    """Defines embedded video content"""

    def __init__(
        self,
        *children: Renderable,
        src: str | None = None,
        autoplay: str | None = None,
        controls: str | None = None,
        controlslist: str | None = None,
        crossorigin: str | None = None,
        disablepictureinpicture: str | None = None,
        disableremoteplayback: str | None = None,
        height: str | int | None = None,
        width: str | int | None = None,
        loop: str | None = None,
        muted: str | None = None,
        playsinline: str | None = None,
        poster: str | None = None,
        preload: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Wbr(SelfClosingTag):
    """Defines a possible line-break"""

    def __init__(
        self,
        *,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs | locals_cleanup(locals()))
