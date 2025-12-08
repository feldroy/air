"""Root module for the Base air-tag for all other tags."""

from __future__ import annotations

import html
import json
from functools import cached_property
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Self

import nh3
from rich.pretty import pretty_repr
from selectolax.lexbor import LexborHTMLParser, LexborNode

from air.tags.constants import (
    DEFAULT_INDENTATION_SIZE,
    EMPTY_JOIN_SEPARATOR,
    HTML_ATTRIBUTES_JOIN_SEPARATOR,
    INLINE_JOIN_SEPARATOR,
    MULTILINE_JOIN_SEPARATOR,
    TagKeys,
)
from air.tags.utils import (
    SafeStr,
    compact_format_html,
    display_pretty_html_in_the_browser,
    is_full_html_document,
    migrate_attribute_name_to_html,
    open_html_in_the_browser,
    pretty_format_html,
    pretty_print_html,
    pretty_print_python,
    save_text,
)

from .utils import (
    _format_attribute_instantiation,
    _format_child_instantiation,
    _format_instantiation_call,
    _get_paddings,
    _migrate_html_attributes_to_air_tag,
    _wrap_multiline_instantiation_args,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from air.tags.types import StrPath

    from .types import (
        AttributeType,
        Renderable,
        TagAttributesType,
        TagChildrenType,
        TagChildrenTypeForDict,
        TagDictType,
    )


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
        self._children: TagChildrenType = children
        self._attrs: TagAttributesType = attributes

    def __new__(cls, *children: Renderable, **attributes: AttributeType) -> Self:
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
        return " " + HTML_ATTRIBUTES_JOIN_SEPARATOR.join(
            self._format_attr(name) for name, value in self._attrs.items() if value is not False
        )

    def _format_attr(self, name: str) -> str:
        """Convert a stored attribute into an HTML-safe representation.

        Args:
            name: The original attribute name stored on the tag.

        Returns:
            The attribute rendered as `name="value"` or a bare name for boolean attributes.
        """
        attr_value = self._attrs[name]
        attr_name = migrate_attribute_name_to_html(name)
        if attr_value is True:
            return attr_name
        return f'{attr_name}="{attr_value}"'

    @cached_property
    def children(self) -> str:
        """Render all child nodes into a single HTML string.

        Returns:
            Concatenated child HTML, or an empty string when no children exist.
        """
        if not self._children:
            return ""
        return EMPTY_JOIN_SEPARATOR.join(self._render_child(child) for child in self._children)

    def _render_child(self, child: Renderable) -> str:
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

    @cached_property
    def pretty_html(self) -> str:
        """Render prettified-formatted HTML representation of the tag.

        Returns:
            The prettified-formatted HTML string,
        """
        return self.pretty_render()

    @cached_property
    def compact_html(self) -> str:
        """Render the compact-formatted HTML representation of the tag.

        Returns:
            A minimized HTML string produced by `minify_html.minify`.
        """
        return self.compact_render()

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

    def save(self, *, file_path: StrPath) -> None:
        """Persist the rendered HTML to disk.

        Args:
            file_path: Destination path for the HTML file.
        """
        save_text(text=self.render(), file_path=file_path)

    def pretty_save(self, *, file_path: StrPath) -> None:
        """Persist pretty-formatted HTML to disk.

        Args:
            file_path: Destination path for the pretty HTML file.
        """
        save_text(text=self.pretty_render(), file_path=file_path)

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
        return self.html

    def __repr__(self) -> str:
        """Return a concise representation showing the tag name and summary.

        Returns:
            A readable string representation for debugging.
        """
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
        children = INLINE_JOIN_SEPARATOR.join(
            child.full_repr() if isinstance(child, BaseTag) else child for child in self._children
        )  # ty: ignore[no-matching-overload]
        children_str = f"{attributes and ', '}{TagKeys.CHILDREN}={children}" if self._children else ""
        return f"{self._name}({attributes}{children_str})"

    def to_source(self) -> str:
        """Return a Python expression that reconstructs this tag.

        Convert this air-tag into the instantiable-formatted representation of the tag.

        Returns:
            The formatted instantiation call for this tag and its children.
        """
        return self._to_source()

    def _to_source(self, level: int = 0) -> str:
        """Return a Python expression that reconstructs this tag.

        Convert this air-tag into the instantiable-formatted representation of the tag.

        Args:
            level: The current indentation depth when nesting tags.

        Returns:
            The formatted instantiation call for this tag and its children.
        """
        outer_padding, inner_padding = _get_paddings(level)
        instantiation_args = self._format_instantiation_arguments(
            level=level, outer_padding=outer_padding, inner_padding=inner_padding
        )
        return _format_instantiation_call(
            tag_name=self._name, instantiation_args=instantiation_args, outer_padding=outer_padding
        )

    def _format_instantiation_arguments(self, level: int, outer_padding: str, inner_padding: str) -> str:
        """Compose the argument list for the tag instantiation call.

        Args:
            level: Current indentation depth for nested tags.
            outer_padding: Padding applied to the opening line of the call.
            inner_padding: Padding applied to nested children and attributes.

        Returns:
            The formatted argument string, either inline or multiline.
        """
        if self.is_attribute_free_void_element:
            return ""
        if self._should_format_multiline_arguments():
            return self._format_multiline_instantiation_arguments(
                level=level, outer_padding=outer_padding, inner_padding=inner_padding
            )
        return self._format_inline_instantiation_arguments(level=level)

    def _should_format_multiline_arguments(self) -> bool:
        """Decide whether to expand constructor arguments across multiple lines.

        Returns:
            True when multiple children or attributes exist, or the first child is a tag.
        """
        return len(self._children) > 1 or len(self._attrs) > 1 or isinstance(self.first_child, BaseTag)

    def _format_multiline_instantiation_arguments(self, level: int, outer_padding: str, inner_padding: str) -> str:
        """Format constructor arguments on separate lines with indentation.

        Args:
            level: Current indentation depth for nested tags.
            outer_padding: Padding for the opening and closing lines.
            inner_padding: Padding for each argument line.

        Returns:
            A multiline argument string wrapped with surrounding padding.
        """
        instantiation_args = self._get_instantiation_arguments(level, inner_padding)
        multiline_instantiation_args = MULTILINE_JOIN_SEPARATOR.join(instantiation_args)
        return _wrap_multiline_instantiation_args(multiline_instantiation_args, outer_padding)

    def _format_inline_instantiation_arguments(self, level: int) -> str:
        """Format constructor arguments on a single line.

        Args:
            level: Current indentation depth for nested tags.

        Returns:
            The inline argument string.
        """
        instantiation_args = self._get_instantiation_arguments(level=level)
        return INLINE_JOIN_SEPARATOR.join(instantiation_args)

    def _get_instantiation_arguments(self, level: int, inner_padding: str = "") -> list[str]:
        """Collect formatted children and attribute arguments.

        Args:
            level: Current indentation depth for nested tags.
            inner_padding: Padding applied to nested argument lines.

        Returns:
            A list of formatted argument strings.
        """
        children_instantiation_args = self._get_children_instantiation_arguments(level=level, padding=inner_padding)
        attribute_instantiation_args = self._get_attributes_instantiation_arguments(padding=inner_padding)
        return children_instantiation_args + attribute_instantiation_args

    def _get_children_instantiation_arguments(self, level: int, padding: str) -> list[str]:
        """Format each child as an instantiation argument.

        Args:
            level: Current indentation depth for nested tags.
            padding: Padding applied to each child line.

        Returns:
            Formatted child argument strings.
        """
        return [
            child._to_source(level + 1) if isinstance(child, BaseTag) else _format_child_instantiation(child, padding)
            for child in self._children
        ]

    def _get_attributes_instantiation_arguments(self, padding: str) -> list[str]:
        """Format each attribute as a keyword argument.

        Args:
            padding: Padding applied to each attribute line.

        Returns:
            Formatted attribute argument strings.
        """
        return [
            _format_attribute_instantiation(attr_name=name, attr_value=value, padding=padding)
            for name, value in self._attrs.items()
        ]

    @property
    def is_attribute_free_void_element(self) -> bool:
        """Check whether the tag has neither attributes nor children.

        Returns:
            True when the tag has no attributes and no children.
        """
        return not self.has_children and not self.has_attributes

    @property
    def has_children(self) -> bool:
        """Return True when the tag contains one or more children.

        Returns:
            True when children are present; otherwise False.
        """
        return bool(self._children)

    @property
    def has_attributes(self) -> bool:
        """Return True when the tag defines one or more attributes.

        Returns:
            True when attributes are present; otherwise False.
        """
        return bool(self._attrs)

    @property
    def first_child(self) -> Renderable | None:
        """Return the first child or None when no children are present.

        Returns:
            The first child value, or None if there are no children.
        """
        if self._children:
            return self._children[0]
        return None

    @property
    def last_child(self) -> Renderable | None:
        """Return the last child or None when no children are present.

        Returns:
            The last child value, or None if there are no children.
        """
        if self._children:
            return self._children[self.num_of_direct_children - 1]
        return None

    @property
    def first_attribute(self) -> tuple[str, AttributeType] | None:
        """Return the first attribute key-value pair or None when none exist.

        Returns:
            The first attribute pair, or None if no attributes are set.
        """
        if self._attrs:
            return next(iter(self._attrs.items()))
        return None

    @property
    def last_attribute(self) -> tuple[str, AttributeType] | None:
        """Return the last attribute key-value pair or None when none exist.

        Returns:
            The last attribute pair, or None if no attributes are set.
        """
        if self._attrs:
            return list(self._attrs.items()).pop()
        return None

    @property
    def num_of_direct_children(self) -> int:
        """Return the number of the direct children for an element.

        Returns:
            The count of children.
        """
        return len(self._children)

    @property
    def num_of_attributes(self) -> int:
        """Return the number of defined attributes.

        Returns:
            The count of attributes.
        """
        return len(self._attrs)

    @property
    def tag_id(self) -> AttributeType | None:
        """Return the tag's `id_` attribute when present.

        Returns:
            The `id_` value or None if absent.
        """
        return self._attrs.get("id_")

    def to_pretty_dict(
        self,
        *,
        max_width: int = 170,
        max_length: int = 7,
        max_depth: int = 4,
        max_string: int = 25,
        expand_all: bool = False,
    ) -> str:
        """Produce a human-friendly mapping view of the tag.

        Returns:
            A formatted string produced by the rich pretty printer when available,
            otherwise the standard string form of the mapping.
        """
        return pretty_repr(
            self.to_dict(),
            max_width=max_width,
            max_length=max_length,
            max_depth=max_depth,
            max_string=max_string,
            expand_all=expand_all,
        )

    def to_dict(self) -> TagDictType:
        """Convert the tag into a JSON-serializable dictionary.

        Returns:
            A mapping with the tag name, attributes, and serialized children.
        """
        return {
            TagKeys.NAME: self._name,
            TagKeys.ATTRIBUTES: self._attrs,
            TagKeys.CHILDREN: self._to_child_dict(),
        }

    def _to_child_dict(self) -> TagChildrenTypeForDict:
        """Convert child nodes into serializable objects.

        Returns:
            A list containing serialized child tags or raw values.
        """
        return tuple(child.to_dict() if isinstance(child, BaseTag) else child for child in self._children)

    def to_json(self, *, indent_size: int | None = None) -> str:
        """Serialize the tag to JSON.

        Args:
            indent_size: Indentation width to use for pretty-printing.

        Returns:
            The JSON string representation of the tag.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent_size)

    def to_pretty_json(self) -> str:
        """Serialize the tag to formatted JSON.

        Returns:
            The indented JSON string representation of the tag.
        """
        return self.to_json(indent_size=DEFAULT_INDENTATION_SIZE)

    @classmethod
    def from_dict(cls, source_dict: TagDictType) -> BaseTag:
        """Instantiate a tag hierarchy from serialized data.

        Args:
            source_dict: The dictionary produced by `to_dict`.

        Returns:
            The restored tag instance.
        """
        name: str = source_dict[TagKeys.NAME]
        attributes: TagAttributesType = source_dict[TagKeys.ATTRIBUTES]
        children_dict: TagChildrenTypeForDict = source_dict[TagKeys.CHILDREN]
        children: TagChildrenType = cls._from_child_dict(children_dict)
        return cls._create_tag(name, *children, **attributes)

    @classmethod
    def _from_child_dict(cls, children_dict: TagChildrenTypeForDict) -> TagChildrenTypeForDict:
        """Restore serialized children into tag instances or raw values.

        Args:
            children_dict: The serialized children sequence.

        Returns:
            The restored children's collection.
        """
        # noinspection PyTypeChecker
        return tuple(
            cls.from_dict(child_dict) if isinstance(child_dict, dict) else child_dict for child_dict in children_dict
        )

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
    def print_source(cls, html_source: str) -> None:
        """Display the instantiable-formatted representation of the tag in the console with syntax highlighting.

        1. Reconstruct the corresponding air-tag tree from the given HTML content.
        2. Convert air-tag tree into the instantiable-formatted representation of the tag.
        3. Display it with syntax highlighting inside a styled terminal panel.

        Args:
            html_source: HTML content to parse.
        """
        pretty_print_python(cls.from_html(html_source).to_source())

    @classmethod
    def save_source(cls, *, file_path: StrPath, html_source: str) -> None:
        """Save the instantiable-formatted representation of the tag to disk.

        1. Reconstruct the corresponding air-tag tree from the given HTML content.
        2. Convert air-tag tree into the instantiable-formatted representation of the tag.
        3. Save the Python expression that reconstructs this tag to disk.

        Args:
            html_source: HTML content to parse.
            file_path: Destination path for the .py file.
        """
        save_text(text=cls.from_html(html_source).to_source(), file_path=file_path)

    @classmethod
    def from_html_to_source(cls, html_source: str) -> str:
        """Reconstruct the instantiable-formatted representation of the tag from the given HTML content.

        For converting the corresponding air-tag tree from the given HTML content,
        into the instantiable-formatted representation of the tag.

        Args:
            html_source: HTML content to parse.

        Returns:
            The formatted instantiation call for this tag and its children.
        """
        return cls.from_html(html_source).to_source()

    @classmethod
    def from_html(cls, html_source: str) -> BaseTag:
        """Reconstruct the corresponding air-tag tree from the given HTML content.

        Args:
            html_source: HTML content to parse.

        Returns:
            The root air-tag built from the provided HTML content.

        Raises:
            TypeError: If ``html_source`` is not a string.
            ValueError: If the markup is not valid HTML.
        """
        if not isinstance(html_source, str):
            msg = f"{cls.__name__}.from_html(html_source) expects a string argument."
            raise TypeError(msg)
        if not nh3.is_html(html_source):
            msg = f"{cls.__name__}.from_html(html_source) expects a valid HTML string."
            raise ValueError(msg)
        is_fragment = not is_full_html_document(html_source)
        parser = LexborHTMLParser(html_source, is_fragment=is_fragment)
        return cls._from_html(parser.root)

    @classmethod
    def _from_html(cls, node: LexborNode) -> BaseTag:
        """Recursively build a tag tree from a parsed HTML node.

        Args:
            node: Parsed HTML element node.

        Returns:
            The reconstructed Air tag for the provided node.
        """
        children: TagChildrenType = tuple(
            cls._from_child_html(child) for child in node.iter(include_text=True, skip_empty=True)
        )
        attributes: TagAttributesType = _migrate_html_attributes_to_air_tag(node)
        return cls._create_tag(node.tag, *children, **attributes)

    @classmethod
    def _from_child_html(cls, node: LexborNode) -> BaseTag | str | None:
        """Convert a parsed HTML child node into an Air tag, text, or comment.

        Args:
            node: Parsed HTML child node.

        Returns:
            An Air tag for element nodes, stripped text for text nodes, or a comment tag for comment
            nodes.

        Raises:
            ValueError: If the node type cannot be handled.
        """
        if node.is_element_node:
            return cls._from_html(node)
        if node.is_text_node and node.text_content:
            return node.text_content
        if node.is_comment_node and node.comment_content:
            return cls._create_tag("comment", node.comment_content)
        msg = f"Unable to parse <{node.tag}>."
        raise ValueError(msg)

    @classmethod
    def _create_tag(cls, name: str, /, *children: Renderable, **attributes: AttributeType) -> BaseTag:
        """Instantiate a registered tag by name.

        Args:
            name: Tag name looked up in the registry.
            children: Child content passed to the tag constructor.
            attributes: Attributes passed to the tag constructor.

        Returns:
            The instantiated Air tag.

        Raises:
            TypeError: If the tag name is not registered.
        """
        try:
            return cls.registry[name.lower()](*children, **attributes)
        except KeyError as e:
            msg = f"Unable to create a new air-tag, <{name}> is not a registered tag name."
            raise TypeError(msg) from e

    def __init_subclass__(cls) -> None:
        """Register subclasses so they can be restored from serialized data."""
        super().__init_subclass__()
        BaseTag._registry[cls.__name__.lower()] = cls

    def __eq__(self, other: object, /) -> bool:
        """Compare tags by their rendered HTML.

        Args:
            other: Object to compare against.

        Returns:
            True when the rendered HTML matches.

        Raises:
            TypeError: If compared to a non-BaseTag object.
        """
        if not isinstance(other, BaseTag):
            msg = f"<{self.name}> is comparable only to other air-tags."
            raise TypeError(msg)
        return self.html == other.html

    def __hash__(self) -> int:
        """Return the hash of the rendered HTML representation.

        Returns:
            Hash derived from the rendered HTML string.
        """
        return hash(self.html)
