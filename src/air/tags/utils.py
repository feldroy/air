"""Utilities for the Air Tag system."""

from builtins import __dict__ as _bt
from typing import Any, Callable, Final

from .config import HTML_ATTRIBUTES


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


def locals_cleanup(local_data: dict[str, Any], obj) -> dict[str, Any]:
    """Converts arguments to kwargs per the html_attributes structure"""
    data = {}
    attrs = [*HTML_ATTRIBUTES.get(obj.__class__.__name__, []), "class_", "for_", "as_", "id", "style"]
    for attr in attrs:
        # For performance reasons we use key checks rather than local_data.get
        if attr in local_data and local_data[attr] is not None:
            data[attr] = local_data[attr]
    return data
    return data


def svg_locals_cleanup(
    data: dict[str, Any],
    _skip: frozenset[str] = frozenset({"self", "children", "kwargs"}),
) -> dict[str, Any]:
    """Extract non-None attributes from locals() for SVG elements"""
    # Remove special variables
    return {key: value for key, value in data if value is not None and key[0] != "_" and key not in _skip}


def clean_locals(ns: dict[str, object], _skip: frozenset[str] = frozenset({"self", "children", "kwargs"})) -> dict[str, object]:
    return {k: v for k, v in ns.items() if v is not None and k[0] != "_" and k not in _skip}
