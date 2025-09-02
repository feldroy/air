"""Root module for the Air Tags system."""

import html
from functools import cached_property
from typing import Any

from ..utils import SafeStr, clean_html_attr_key, format_html


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

    @cached_property
    def attrs(self) -> str:
        if not self._attrs:
            return ""
        return " ".join(self._format_attr(key) for key in self._attrs)

    def _format_attr(self, key: str) -> str:
        value = self._attrs[key]
        clean_key = clean_html_attr_key(key)
        if isinstance(value, bool):
            return clean_key if value else ""
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
        return str(self)

    def __repr__(self) -> str:
        return format_html(self._render())

    __str__ = __repr__

    def _render(self) -> str:
        if self.name == "tag":
            return self.children
        attrs = " " + self.attrs if self.attrs else ""
        # TODO -> HTML5 does not use self-closing slashes(We need to remove self-closing slash and the extra-space)
        if self.self_closing:
            return f"<{self.name}{attrs} />"
        return f"<{self.name}{attrs}>{self.children}</{self.name}>"
