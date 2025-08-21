"""Root module for the Air Tags system."""

import html
from functools import cached_property
from typing import Any

from ..utils import SafeStr, clean_html_attr_key


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
                attrs.append(clean_html_attr_key(k))
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
