"""Utilities for the Air Tag system."""

import html
from typing import Any, Final

EXTRA_FEATURE_PRETTY_ERROR_MESSAGE: Final = (
    "Extra feature 'pretty' is not installed. Install with: `uv add air[pretty]`"
)
HTML_DOCTYPE: Final = "<!doctype html>"


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


def pretty_format_html(
    source: str,
    *,
    with_body: bool = False,
    with_head: bool = False,
    with_doctype: bool = False,
) -> str:
    """
    Pretty-print HTML with pretty indentation and then unescape &lt;, &gt;, &amp; &#x27; in the final string.

    NOTE: This will also unescape inside attribute values, which can make the
    HTML invalid and unsafe. Use only if you fully trust the input/output.
    """

    return html.unescape(
        format_html(source, with_body=with_body, with_head=with_head, with_doctype=with_doctype, pretty=True)
    )


def format_html(
    source: str,
    *,
    with_body: bool = False,
    with_head: bool = False,
    with_doctype: bool = False,
    pretty: bool = False,
) -> str:
    try:
        from lxml import (
            etree,  # ty: ignore[unresolved-import]
            html as l_html,
        )
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(EXTRA_FEATURE_PRETTY_ERROR_MESSAGE) from exc
    else:
        if with_body:
            source = l_html.document_fromstring(source, ensure_head_body=with_head)
        else:
            source = l_html.fromstring(source)
        if pretty:
            etree.indent(source)  # pretty indentation
        doctype = HTML_DOCTYPE if with_doctype else None
        return l_html.tostring(source, encoding="unicode", pretty_print=pretty, doctype=doctype)


def pretty_print_html(source: str, *, theme: str = "dracula") -> None:
    """Pretty-print and render HTML with syntax highlighting."""
    try:
        from rich import box
        from rich.console import Console
        from rich.padding import Padding
        from rich.panel import Panel
        from rich.syntax import Syntax
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(EXTRA_FEATURE_PRETTY_ERROR_MESSAGE) from exc
    else:
        syntax = Syntax(
            source,
            "html",
            line_numbers=True,
            word_wrap=True,
        )
        panel = Panel(
            Padding(syntax, (0, 2)),
            box=box.HEAVY,
            title="Air → HTML",
        )
        console = Console()
        console.print(panel, soft_wrap=False)


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
