"""Special Air Tags that are not found in any other category."""

from typing import Literal, override

from ..utils import HTML_DOCTYPE, locals_cleanup
from .base import AttributeType, BaseTag, Renderable


class Html(BaseTag):
    """Defines the root of an HTML document"""

    @override
    def _render(self) -> str:
        return f"{HTML_DOCTYPE}{self._render_paired()}"

    @override
    def pretty_render(
        self,
        *,
        with_body: bool = False,
        with_head: bool = False,
        with_doctype: bool = True,
    ) -> str:
        """Pretty-print without escaping."""
        return super().pretty_render(with_body=with_body, with_head=with_head, with_doctype=with_doctype)


class Transparent(BaseTag):
    """Transparent(no own HTML tag) container that renders only its children(just the inner content)."""

    def __init__(
        self,
        *children: Renderable,
    ) -> None:
        super().__init__(*children)

    @override
    def _render(self) -> str:
        return self.children


class Children(Transparent):
    """Alias for the `Transparent` tag; use it if it improves clarity."""


class Tag(Transparent):
    """Alias for the `Transparent` tag; use it if it improves clarity."""


class Tags(Transparent):
    """Alias for the `Transparent` tag; use it if it improves clarity."""


class Fragment(Transparent):
    """Alias for the `Transparent` tag; use it if it improves clarity."""


class SelfClosingTag(BaseTag):
    """Base class for void tags that render as self-closing HTML."""

    def __init__(
        self,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(**kwargs)

    @override
    def _render(self) -> str:
        return self._render_void()


class UnSafeTag(BaseTag):
    """Tag base that bypasses HTML escaping for its content."""

    @override
    def __init__(self, text_child: str = "", /, **kwargs: AttributeType) -> None:
        if not isinstance(text_child, str):
            msg = f"{self!r} only accepts string content"
            raise TypeError(msg)
        super().__init__(text_child, **kwargs)

    @override
    @staticmethod
    def _escape_text(text: str) -> str:
        return text


class Raw(UnSafeTag, Transparent):
    """Renders raw HTML content without escaping.

    Raises:
        TypeError: If non-string content is provided
    Example:
        Raw('<strong>Bold</strong> text')
        # Produces '<strong>Bold</strong> text'
        # Use with other tags
        Div(
            P("Safe content"),
            Raw('<hr class="divider">'),
            P("More safe content")
        )
    """


class Script(UnSafeTag):
    """Defines a client-side script.
    Warning: Script tag does not protect against code injection.

    Args:
        text_child: Inline script code. Use an empty string when providing ``src``.
        src: URI of the external script.
        type: Script type. Examples: ``module``, ``importmap``, ``speculationrules``,
            a JavaScript MIME type (e.g. ``text/javascript``), or empty for classic scripts.
        async_: Fetch in parallel and execute as soon as ready; order is not guaranteed.
        defer: Execute after parsing (classic scripts only; modules defer by default).
        nomodule: Do not execute on browsers that support ES modules.
        crossorigin: CORS mode. One of ``"anonymous"`` or ``"use-credentials"``.
        integrity: Subresource Integrity hash (e.g. ``"sha384-..."``).
        referrerpolicy: Which referrer to send. One of:
            ``"no-referrer"``, ``"no-referrer-when-downgrade"``, ``"origin"``,
            ``"origin-when-cross-origin"``, ``"same-origin"``, ``"strict-origin"``,
            ``"strict-origin-when-cross-origin"``, ``"unsafe-url"``.
        fetchpriority: Network priority hint. One of ``"high"``, ``"low"``, ``"auto"``.
        blocking: Space-separated tokens that block operations; currently ``"render"``.
        attributionsrc: Space-separated URLs for Attribution Reporting (experimental).
        nonce: CSP nonce (meaning: one-time token) to allow this inline script.
        class_: Substituted as the DOM ``class`` attribute.
        id: DOM ``id`` attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    @override
    def __init__(
        self,
        text_child: str = "",
        /,
        *,
        src: str | None = None,
        type: str | None = None,
        async_: bool = False,
        defer: bool = False,
        nomodule: bool = False,
        crossorigin: Literal["anonymous", "use-credentials"] | None = None,
        integrity: str | None = None,
        referrerpolicy: Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ]
        | None = None,
        fetchpriority: Literal["high", "low", "auto"] | None = None,
        blocking: Literal["render"] | None = None,
        attributionsrc: str | None = None,
        nonce: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(text_child, **kwargs | locals_cleanup(locals()))


class Style(UnSafeTag):
    """Defines style information for a document.
    Warning: Style tag does not protect against code injection.

    Args:
        text_child: CSS stylesheet text.
        media: Media query (e.g. ``"(width < 500px)"``). Defaults to ``"all"``.
        title: Title for alternate style sheet sets.
        blocking: Space-separated tokens that block operations; currently ``"render"``.
        nonce: CSP nonce (meaning: one-time token) to allow this inline style.
        type: (Deprecated) Only ``""`` or ``"text/css"`` are permitted; omit in modern HTML.
        class_: Substituted as the DOM ``class`` attribute.
        id: DOM ``id`` attribute.
        style: Inline style attribute.
        kwargs: Keyword arguments transformed into tag attributes.
    """

    @override
    def __init__(
        self,
        text_child: str = "",
        /,
        *,
        media: str | None = None,
        title: str | None = None,
        blocking: Literal["render"] | None = None,
        nonce: str | None = None,
        type: str | None = None,  # deprecated
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(text_child, **kwargs | locals_cleanup(locals()))


class Comment(UnSafeTag):
    """Represents an HTML comment node."""

    @override
    def __init__(
        self,
        text_child: str = "",
        /,
    ) -> None:
        """Initializes the comment with the raw text payload.

        Args:
            text_child: Text inserted inside the comment delimiters.
        """
        if "\n" in text_child:
            msg = f"{self!r}, does not support multi-line comments!"
            raise TypeError(msg)
        super().__init__(text_child)

    @override
    def _render(self) -> str:
        """Wraps the comment text with HTML comment delimiters.

        Returns:
            The serialized comment node.
        """
        return f"<!-- {self.children} -->"
