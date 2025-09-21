"""Root module for the Air Tags system."""

from __future__ import annotations

import html
import json
from collections.abc import Mapping
from functools import cached_property
from types import MappingProxyType
from typing import Any, ClassVar, Final, Self, TypedDict

from ..utils import SafeStr, clean_html_attr_key, pretty_format_html, pretty_print_html

type AttributesType = str | int | float | bool


class TagDictType(TypedDict):
    name: str
    attributes: dict[str, AttributesType]
    children: tuple[Any, ...]


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

    def __init__(self, *children: Any, **kwargs: AttributesType) -> None:
        """
        Args:
            children: Tags, strings, or other rendered content.
            kwargs: Keyword arguments transformed into tag attributes.
        """
        self._name = self.__class__.__name__
        self._module = self.__class__.__module__
        self._children, self._attrs = children, kwargs

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Non-instantiable base; all subclasses are instantiable."""
        if cls is BaseTag:
            msg = f"{cls.__name__} cannot be instantiated; use a subclass"
            raise TypeError(msg)
        return super().__new__(cls)

    @property
    def name(self) -> str:
        return self._name.lower()

    @cached_property
    def attrs(self) -> str:
        if not self._attrs:
            return ""
        return " " + " ".join(self._format_attr(key) for key, value in self._attrs.items() if value is not False)

    def _format_attr(self, key: str) -> str:
        value = self._attrs[key]
        clean_key = clean_html_attr_key(key)
        if value is True:
            return clean_key
        return f'{clean_key}="{value}"'

    @cached_property
    def children(self) -> str:
        if not self._children:
            return ""
        return "".join(self._render_child(child) for child in self._children)

    def _render_child(self, child: Any) -> str:
        child_str = str(child)
        if isinstance(child, BaseTag | SafeStr):
            return child_str
        return self._escape_text(child_str)

    @staticmethod
    def _escape_text(text: str) -> str:
        return html.escape(text)

    def render(self) -> str:
        return self._render()

    def pretty_render(
        self,
        *,
        with_body: bool = False,
        with_head: bool = False,
        with_doctype: bool = False,
    ) -> str:
        """Pretty-print without escaping."""
        return pretty_format_html(self._render(), with_body=with_body, with_head=with_head, with_doctype=with_doctype)

    def pretty_print(self) -> None:
        """Pretty-print and render HTML with syntax highlighting."""
        pretty_print_html(self.pretty_render())

    def _render(self) -> str:
        return self._render_paired()

    def _render_void(self) -> str:
        """Render a self-closing (void) tag.

        TODO: HTML5 does not require a trailing slash.
              Consider returning f"<{self.name}{self.attrs}>" instead.
        """
        return f"<{self.name}{self.attrs} />"

    def _render_paired(self) -> str:
        """Render a normal open/close pair."""
        return f"<{self.name}{self.attrs}>{self.children}</{self.name}>"

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        summary = f'("{self._doc_summary}")' if self._doc_summary else ""
        return f"<air.{self._name}{summary}>"

    @property
    def _doc_summary(self) -> str:
        return self.__doc__.splitlines()[0] if self.__doc__ else ""

    def full_repr(self) -> str:
        attributes = f"{TagKeys.ATTRIBUTES}={self._attrs}" if self._attrs else ""
        children = ", ".join(child.full_repr() if isinstance(child, BaseTag) else child for child in self._children)
        children_str = f"{attributes and ', '}{TagKeys.CHILDREN}={children}" if self._children else ""
        return f"{self._name}({attributes}{children_str})"

    def to_pretty_dict(self) -> str:
        try:
            from rich.pretty import pretty_repr

            return pretty_repr(self.to_dict(), max_width=170, max_length=7, max_depth=4, max_string=25)
        except ModuleNotFoundError:
            return str(self.to_dict())

    def to_dict(self) -> TagDictType:
        """
        Convert this Tag into plain Python data that json.dumps can serialize.

        - Children that are Tag instances are converted recursively.
        """
        return {
            TagKeys.NAME: self._name,
            TagKeys.ATTRIBUTES: self._attrs,
            TagKeys.CHILDREN: tuple(self.to_child_dict()),
        }

    def to_child_dict(self) -> list[TagDictType]:
        return [child.to_dict() if isinstance(child, BaseTag) else child for child in self._children]

    def to_json(self, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_pretty_json(self) -> str:
        return self.to_json(indent=4)

    @classmethod
    def from_dict(cls, source_dict: TagDictType) -> Self:
        name, attributes, children_dict = source_dict.values()
        children: tuple[Self, ...] = tuple(cls._from_child_dict(children_dict))
        tag = cls.registry[name](*children, **attributes)
        tag._name = name
        return tag

    @classmethod
    def _from_child_dict(cls, children_dict: TagDictType) -> list[Self]:
        return [
            cls.from_dict(child_dict) if isinstance(child_dict, dict) else child_dict for child_dict in children_dict
        ]

    @classmethod
    def from_json(cls, source_json: str) -> Self:
        return cls.from_dict(json.loads(source_json))

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        BaseTag._registry[cls.__name__] = cls
