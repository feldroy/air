"""Root module for the Air Tags system."""

import html
import json
from functools import cached_property
from typing import Any, TypedDict

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from ..utils import SafeStr, clean_html_attr_key, format_html


class TagDictType(TypedDict):
    name: str
    attributes: dict[str, str | int | float | bool]
    children: tuple[Any]


class Tag:
    """Base tag for all other tags.

    Sets four attributes, name, module, children, and attrs.
    These are important for Starlette view responses, as nested objects
    get auto-serialized to JSON and need to be rebuilt. With
    the values of these attributes, the object reconstruction can occur.
    """

    self_closing = False
    is_pretty = False

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

    @staticmethod
    def _render_child(child: Any) -> str:
        child_str = str(child)
        if isinstance(child, (Tag, SafeStr)):
            return child_str
        # If the type isn't supported, we just convert to `str`
        # and then escape it for safety. This matches to what most
        # template tools do, which prevents hard bugs in production
        # from stopping users cold.
        return html.escape(child_str)

    def render(self) -> str:
        return format_html(self._render()) if self.is_pretty else self._render()

    def __repr__(self) -> str:
        attributes = f"attribute={self._attrs}" if self._attrs else ""
        children = f"{attributes and ', '}children={self._children}" if self._children else ""
        return f"{self._name}({attributes}{children})"

    def raw_repr(self) -> str:
        return object.__repr__(self)

    def __str__(self) -> str:
        return self.render()

    def _render(self) -> str:
        if self.name == "tag":
            return self.children
        # TODO -> HTML5 does not use self-closing slashes(We need to remove self-closing slash and the extra-space)
        if self.self_closing:
            return f"<{self.name}{self.attrs} />"
        return f"<{self.name}{self.attrs}>{self.children}</{self.name}>"

    def to_dict(self) -> TagDictType:
        return {
            "name": self._name,
            "attributes": self._attrs,
            "children": self._children,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, source_dict: TagDictType) -> Self:
        name, attributes, children = source_dict.values()
        tag = cls(*children, **attributes)
        tag._name = name
        return tag

    @classmethod
    def from_json(cls, source_json: str) -> Self:
        return cls.from_dict(json.loads(source_json))
