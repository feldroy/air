"""Root module for the Air Tags system."""

from __future__ import annotations

import html
import json
from collections.abc import Mapping
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, Any, ClassVar, Final, Self, TypedDict

import nh3
from selectolax.lexbor import LexborHTMLParser, LexborNode
from typing_extensions import Doc
from rich.pretty import pretty_repr
from textwrap import indent as tw_indent

from ..constants import TOP_LEVEL_HTML_TAGS
from ..utils import (
    SafeStr,
    StrPath,
    _fmt_value, clean_html_attr_key,
    compact_format_html,
    display_pretty_html_in_the_browser,
    extract_html_comment, has_all_top_level_tags, migrate_html_key_to_air_tag, open_html_in_the_browser,
    pretty_format_html,
    pretty_print_html,
)

type Renderable = Annotated[
    str | BaseTag | SafeStr | int | float,
    Doc(
        """
        The type for any renderable content(a child of a tag)
        Excludes types like None (renders as "None"), bool ("True"/"False"),
        complex ("(1+2j)"), bytes ("b'...'"), and others that produce
        undesirable or unintended HTML output.
        """
    ),
]
type AttributeType = Annotated[
    str | int | float | bool,
    Doc(
        """
        The type for any HTML attribute value.
        """
    ),
]
type TagAttributesType = Annotated[
    dict[str, AttributeType],
    Doc(
        """
        The type for a dictionary of HTML attributes.
        """
    ),
]


class TagDictType(TypedDict):
    name: str
    attributes: TagAttributesType
    children: tuple[Renderable, ...]


class TagKeys:
    NAME: Final = "name"
    ATTRIBUTES: Final = "attributes"
    CHILDREN: Final = "children"


class BaseTag:
    """Base tag for all other tags.

    Sets four attributes, name, module, children, and attrs.
    These are important for Starlette view responses, as nested objects
    get auto-serialized to JSON and need to be rebuilt. With
    the values of these attributes, the object reconstruction can occur.
    """

    _registry: ClassVar[dict[str, type[BaseTag]]] = {}
    registry: ClassVar[Mapping[str, type[BaseTag]]] = MappingProxyType(_registry)  # read-only view

    def __init__(self, *children: Renderable, **attributes: AttributeType) -> None:
        """Initialize a tag with renderable children and HTML attributes.

        Args:
            children: Renderable objects that become the tag's inner content.
            attributes: Attribute names and values applied to the tag element.
        """
        self._name = self.__class__.__name__
        self._module = self.__class__.__module__
        self._children: tuple[Renderable, ...] = children
        self._attrs: TagAttributesType = attributes

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Create a tag instance while preventing direct BaseTag instantiation.

        Raises:
            TypeError: If code attempts to instantiate BaseTag directly.
        """
        if cls is BaseTag:
            msg = f"{cls.__name__} cannot be instantiated; use a subclass"
            raise TypeError(msg)
        return super().__new__(cls)

    @property
    def name(self) -> str:
        """Return the normalized tag name.

        Returns:
            The lowercase tag name for use in HTML.
        """
        return self._name.lower()

    @cached_property
    def attrs(self) -> str:
        """Return the formatted HTML attributes string.

        Returns:
            A string containing formatted attributes prefixed with a space,
            or an empty string when no attributes are present.
        """
        if not self._attrs:
            return ""
        return " " + " ".join(self._format_attr(key) for key, value in self._attrs.items() if value is not False)

    def _format_attr(self, key: str) -> str:
        """Convert a stored attribute into an HTML-safe representation.

        Args:
            key: The original attribute key stored on the tag.

        Returns:
            The attribute rendered as `key="value"` or a bare key for boolean attributes.
        """
        value = self._attrs[key]
        clean_key = clean_html_attr_key(key)
        if value is True:
            return clean_key
        return f'{clean_key}="{value}"'

    @cached_property
    def children(self) -> str:
        """Render all child nodes into a single HTML string.

        Returns:
            Concatenated child HTML, or an empty string when no children exist.
        """
        if not self._children:
            return ""
        return "".join(self._render_child(child) for child in self._children)

    def _render_child(self, child: Any) -> str:
        """Render a single child element.

        Args:
            child: The child object to render.

        Returns:
            The rendered child string, escaped when the child is not tag-aware.
        """
        child_str = str(child)
        if isinstance(child, BaseTag | SafeStr):
            return child_str
        return self._escape_text(child_str)

    @staticmethod
    def _escape_text(text: str) -> str:
        """Escape text for safe HTML display.

        Args:
            text: The raw text that may contain HTML.

        Returns:
            The escaped text with HTML entities substituted.
        """
        return html.escape(text)

    @cached_property
    def html(self) -> str:
        """Render the HTML representation of the tag.

        Returns:
            The rendered HTML string.
        """
        return self._render()

    def render(self) -> str:
        """Render the HTML representation of the tag.

        Returns:
            The rendered HTML string.
        """
        return self.html

    def render_in_the_browser(self) -> None:
        """Render the tag and open the result in a browser tab."""
        open_html_in_the_browser(self.render())

    def pretty_render_in_the_browser(self) -> None:
        """Render pretty-formatted HTML and open the result in a browser tab."""
        open_html_in_the_browser(self.pretty_render(with_body=True, with_doctype=True))

    def pretty_render(
        self,
        *,
        with_body: bool = False,
        with_head: bool = False,
        with_doctype: bool = False,
    ) -> str:
        """Render the prettified-formatted HTML representation of the tag.

        Args:
            with_body: Whether to wrap the HTML inside a `<body>` element.
            with_head: Whether to generate a `<head>` element.
            with_doctype: Whether to prefix the output with a doctype declaration.

        Returns:
            The pretty-formatted HTML string.
        """
        return pretty_format_html(self._render(), with_body=with_body, with_head=with_head, with_doctype=with_doctype)

    def compact_render(self) -> str:
        """Render the compact-formatted HTML representation of the tag.

        Returns:
            A minimized HTML string produced by `minify_html.minify`.
        """

        return compact_format_html(self._render())

    def pretty_print(self) -> None:
        """Display pretty-formatted HTML in the console with syntax highlighting."""
        pretty_print_html(self.pretty_render())

    def save(self, file_path: StrPath) -> None:
        """Persist the rendered HTML to disk.

        Args:
            file_path: Destination path for the HTML file.
        """
        Path(file_path).write_text(self.render())

    def pretty_save(self, file_path: StrPath) -> None:
        """Persist pretty-formatted HTML to disk.

        Args:
            file_path: Destination path for the pretty HTML file.
        """
        Path(file_path).write_text(self.pretty_render())

    def pretty_display_in_the_browser(self) -> None:
        """Display pretty-formatted HTML in the browser."""
        display_pretty_html_in_the_browser(self.pretty_render(with_body=True, with_doctype=True))

    def _render(self) -> str:
        """Render the tag using the default rendering strategy.

        Returns:
            The rendered HTML string.
        """
        return self._render_paired()

    def _render_void(self) -> str:
        """Render a self-closing (void) tag.

        Returns:
            The rendered HTML string for a void element.

        Note:
            HTML5 does not require a trailing slash for void elements.
        """
        return f"<{self.name}{self.attrs}>"

    def _render_paired(self) -> str:
        """Render a standard paired tag with children.

        Returns:
            The rendered HTML string containing children.
        """
        return f"<{self.name}{self.attrs}>{self.children}</{self.name}>"

    def __str__(self) -> str:
        """Render the HTML representation of the tag.

        Returns:
            The rendered HTML string.
        """
        return self.render()

    def __repr__(self) -> str:
        """Return a concise representation showing the tag name and summary."""
        summary = f'("{self._doc_summary}")' if self._doc_summary else ""
        return f"<air.{self.__class__.__name__}{summary}>"

    @property
    def _doc_summary(self) -> str:
        """Return the first line of the class docstring if present.

        Returns:
            The summary line extracted from the class docstring.
        """
        return self.__doc__.splitlines()[0] if self.__doc__ else ""

    def full_repr(self) -> str:
        """Return an expanded representation including attributes and children.

        Returns:
            The expanded string representation of the tag hierarchy.
        """
        attributes = f"{TagKeys.ATTRIBUTES}={self._attrs}" if self._attrs else ""
        children = ", ".join(child.full_repr() if isinstance(child, BaseTag) else child for child in self._children)
        children_str = f"{attributes and ', '}{TagKeys.CHILDREN}={children}" if self._children else ""
        return f"{self._name}({attributes}{children_str})"

    def to_source2(self) -> str:
        attributes = [f'{key}="{value}"' for key, value in self._attrs.items()] if self._attrs else []
        children = [
            child.to_source2() if isinstance(child, BaseTag) else child for child in self._children
        ] if self._children else []
        return f"air.{self._name}({", ".join(children + attributes)})"

    def to_source44(self, level: int = 0) -> str:
        indent_unit = " " * 4
        prefix = indent_unit * level

        # children first, then attributes
        args: list[str] = []

        for child in self._children:
            if isinstance(child, BaseTag):
                # child starts at column 0, parent will indent the block
                args.append(child.to_source44(level=0))
            else:
                args.append(_fmt_value(child))

        for key, value in self._attrs.items():
            args.append(f"{key}={_fmt_value(value)}")

        if not args:
            return f"{prefix}{self._name}()".expandtabs(4)

        # one line if simple
        if len(args) == 1 and "\n" not in args[0]:
            inner = args[0]
            return f"{prefix}{self._name}({inner})".expandtabs(4)

        # pretty multi line
        inner = ",\n".join(args)
        inner = tw_indent(inner, indent_unit * (level + 1))

        result = (
            f"{prefix}{self._name}(\n"
            f"{inner},\n"
            f"{prefix})"
        )
        return result.expandtabs(4)

    def to_source(self) -> str:
        # attributes like: lang="en"
        attributes = [
            f"{key}={value}"
            for key, value in self._attrs.items()
        ] if self._attrs else []

        # children are either BaseTag instances or strings
        children = [
            (
                child.to_source()
                if isinstance(child, BaseTag)
                else str(child)
            ).expandtabs()
            for child in self._children
        ] if self._children else []

        # combine children and attributes in order
        parts = children + attributes
        inner = ", ".join(parts)

        # expand tabs in the final string too
        return f"{self._name}({inner})".expandtabs()


    def to_pretty_dict(self) -> str:
        """Produce a human-friendly mapping view of the tag.

        Returns:
            A formatted string produced by the rich pretty printer when available,
            otherwise the standard string form of the mapping.
        """
        return pretty_repr(self.to_dict(), max_width=170, max_length=7, max_depth=4, max_string=25)


    def to_dict(self) -> TagDictType:
        """Convert the tag into a JSON-serializable dictionary.

        Returns:
            A mapping with the tag name, attributes, and serialized children.
        """
        return {
            TagKeys.NAME: self._name,
            TagKeys.ATTRIBUTES: self._attrs,
            TagKeys.CHILDREN: tuple(self._to_child_dict()),
        }

    def _to_child_dict(self) -> list[TagDictType | Renderable]:
        """Convert child nodes into serializable objects.

        Returns:
            A list containing serialized child tags or raw values.
        """
        return [child.to_dict() if isinstance(child, BaseTag) else child for child in self._children]

    def to_json(self, indent: int | None = None) -> str:
        """Serialize the tag to JSON.

        Args:
            indent: Indentation width to use for pretty-printing.

        Returns:
            The JSON string representation of the tag.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_pretty_json(self) -> str:
        """Serialize the tag to formatted JSON.

        Returns:
            The indented JSON string representation of the tag.
        """
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, source_dict: TagDictType) -> BaseTag:
        """Instantiate a tag hierarchy from serialized data.

        Args:
            source_dict: The dictionary produced by `to_dict`.

        Returns:
            The restored tag instance.
        """
        name, attributes, children_dict = source_dict.values()
        children: tuple[BaseTag, ...] = tuple(cls._from_child_dict(children_dict))
        air_tag = cls._create_tag(name, *children, **attributes)
        return air_tag

    @classmethod
    def _from_child_dict(cls, children_dict: TagDictType) -> list[BaseTag | Renderable]:
        """Restore serialized children into tag instances or raw values.

        Args:
            children_dict: The serialized children sequence.

        Returns:
            The restored children collection.
        """
        return [
            cls.from_dict(child_dict) if isinstance(child_dict, dict) else child_dict for child_dict in children_dict
        ]

    @classmethod
    def from_json(cls, source_json: str) -> BaseTag:
        """Instantiate a tag hierarchy from JSON.

        Args:
            source_json: The JSON string produced by `to_json`.

        Returns:
            The restored tag instance.
        """
        return cls.from_dict(json.loads(source_json))

    @classmethod
    def from_html(cls, html_source: str) -> BaseTag:
        if not isinstance(html_source, str):
            raise TypeError(f"{cls.__name__}.from_html(html_source) expects a string argument.")
        if not nh3.is_html(html_source):
            raise ValueError(f"{cls.__name__}.from_html(html_source) expects a valid HTML string.")
        # if not has_all_top_level_tags(html_source):
        #     raise ValueError(f"{cls.__name__}.from_html(html_source) expects an HTML string with all top level tags.")
        parser = LexborHTMLParser(html_source)
        # TODO -> Use unwrap_tags for tags without any top_level_tags
        # parser.unwrap_tags(["body", "head"])
        parser.strip_tags(cls.tags_to_strip(html_source))
        return cls._from_html(parser.root)

    @staticmethod
    def tags_to_strip(html_source: str) -> list[str]:
        tags_to_strip = []
        if "<head" not in html_source:
            tags_to_strip.append("head")
        if "<body" not in html_source:
            tags_to_strip.append("body")
        return tags_to_strip

    @classmethod
    def _from_html(cls, node: LexborNode) -> BaseTag:
        children: tuple[BaseTag, ...] = tuple(
            [
                cls._from_child_html(child)
                for child in node.iter(include_text=False)
            ]
        )
        attributes: TagAttributesType = {
            migrate_html_key_to_air_tag(key): value
            for key, value in node.attributes.items()
        }
        air_tag = cls._create_tag(node.tag, *children, **attributes)
        return air_tag

    @classmethod
    def _from_child_html(cls, node: LexborNode) -> BaseTag | str | None:
        if node.first_child and node.first_child == node.last_child and node.first_child.text_content:
            # TODO -> Can be: node.first_child.text_content
            return cls._create_tag(node.tag, node.inner_html)
        if node.tag.endswith("-comment"):
            return cls._create_tag("Comment", extract_html_comment(node.html))
        return cls._from_html(node)

    @classmethod
    def _from_child_html_old(cls, node: LexborNode) -> BaseTag | str | None:
        if node.tag.endswith("-text"):
            return node.text_content
        if node.tag.endswith("-document"):
            raise NotImplementedError
        if node.tag.endswith("-comment"):
            return cls._create_tag("Comment", extract_html_comment(node.html))
        return cls._from_html(node)

    @classmethod
    def _create_tag(cls, name: str, /, *children: Renderable, **attributes: AttributeType) -> BaseTag:
        return cls.registry[name.title()](*children, **attributes)  # ty: ignore[invalid-argument-type]

    @classmethod
    def from_html_to_source(cls, html_source: str) -> str:
        return cls.from_html(html_source).to_source()

    def __init_subclass__(cls) -> None:
        """Register subclasses so they can be restored from serialized data."""
        super().__init_subclass__()
        BaseTag._registry[cls.__name__] = cls

    def __eq__(self, other: Self, /) -> bool:
        if isinstance(other, BaseTag):
            return self.render() == other.render()
        raise TypeError(f"<{self.name}> is comparable only to other air-tags.")
