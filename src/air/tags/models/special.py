"""Special Air Tags that aren't find in any other category."""

from typing import Any

from .base import Tag


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
