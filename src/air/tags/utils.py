"""Utilities for the Air Tag system."""

from typing import Any


def clean_html_attr_key(key: str) -> str:
    """Clean up HTML attribute keys to match the standard W3C HTML spec.

    Args:
        key: An uncleaned HTML attribute key

    Returns:

        Cleaned HTML attribute key
    """
    # If a "_"-suffixed proxy for "class", "for", or "id" is used,
    # convert it to its normal HTML equivalent.
    key = {"class_": "class", "for_": "for", "id_": "id", "as_": "as"}.get(key, key)
    # Remove leading underscores and replace underscores with dashes
    return key.lstrip("_").replace("_", "-")


class SafeStr(str):
    """A string subclass that doesn't trigger html.escape() when called by Tag.render()

    Example:
        sample = SafeStr('Hello, world')
    """


def format_html(source: str) -> str:
    # Parse to a tree, then serialize with pretty indentation.
    try:
        from lxml import etree, html  # ty: ignore[unresolved-import]

        root = html.fromstring(source)
        etree.indent(root)
        return html.tostring(root, pretty_print=True, encoding="unicode")
    except ImportError:
        return source


def locals_cleanup(
    data: dict[str, Any],
    _skip: frozenset[str] = frozenset({"self", "children", "kwargs"}),
) -> dict[str, Any]:
    """Extract non-None attributes from locals() to merge with kwargs"""
    return {key: value for key, value in data.items() if value is not None and key[0] != "_" and key not in _skip}
