"""Utilities for the Air Tag system."""

import html
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


def format_html(source: str) -> str:
    """
    Pretty-print HTML with pretty indentation and then unescape &lt;, &gt;, &amp; &#x27; in the final string.

    NOTE: This will also unescape inside attribute values, which can make the
    HTML invalid and unsafe. Use only if you fully trust the input/output.
    """

    return html.unescape(_format_html_with_escaping(source))


def _format_html_with_escaping(source: str) -> str:
    try:
        from lxml import (
            etree,  # ty: ignore[unresolved-import]
            html as l_html,
        )
    except ImportError:
        return source
    else:
        root = l_html.fromstring(source)
        etree.indent(root)  # pretty indentation
        return l_html.tostring(root, pretty_print=True, encoding="unicode")


def locals_cleanup(
    data: dict[str, Any],
    _skip: frozenset[str] = frozenset({"self", "children", "text_child", "args", "kwargs"}),
) -> dict[str, Any]:
    """Extract non-None attributes from locals() to merge with kwargs"""
    return {key: value for key, value in data.items() if value is not None and key[0] != "_" and key not in _skip}


class SafeStr(str):
    """A string subclass that doesn't trigger html.escape() when called by Tag.render()

    Example:
        sample = SafeStr('Hello, world')
    """
