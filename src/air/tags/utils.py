"""Utilities for the Air Tag system."""

from __future__ import annotations

import base64
import html
import tempfile
import webbrowser
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

type StrPath = PathLike | Path | str

if TYPE_CHECKING:
    from rich.console import Console

EXTRA_FEATURE_PRETTY_ERROR_MESSAGE: Final = (
    "Extra feature 'pretty' is not installed. Install with: `uv add air[pretty]`"
)
FORMAT_HTML_ENCODING: Final = "unicode"
HTML_DOCTYPE: Final = "<!doctype html>"
DEFAULT_THEME: Final = "dracula"
PANEL_TITLE: Final = "Air → HTML"
PANEL_TITLE_STYLE: Final = "italic bold"
PANEL_BORDER_STYLE: Final = "bright_magenta"
SYNTAX_LEXER: Final = "html"
DATA_URL_MAX: Final[int] = 23_973


class BrowserOpenError(RuntimeError):
    """Opening the browser failed for a valid file:// URL."""


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
    except ModuleNotFoundError:
        raise ModuleNotFoundError(EXTRA_FEATURE_PRETTY_ERROR_MESSAGE) from None
    else:
        if with_body:
            source = l_html.document_fromstring(source, ensure_head_body=with_head)
        else:
            source = l_html.fromstring(source)
        if pretty:
            etree.indent(source)  # pretty indentation
        doctype = HTML_DOCTYPE if with_doctype else None
        return l_html.tostring(source, encoding=FORMAT_HTML_ENCODING, pretty_print=pretty, doctype=doctype)


def open_local_file_in_the_browser(path: StrPath) -> None:
    """
    Open a local file in the default browser using a proper file:// URL.

    Raises:
        FileNotFoundError: path doesn't exist (or directory lacks index.html).
        BrowserOpenError: browser open command did not launch.
    """
    path = Path(path)
    if path.is_dir():
        path /= "index.html"
    if not path.exists():
        raise FileNotFoundError(path)

    url = path.expanduser().resolve().as_uri()
    _open_new_tab(url)


def _open_new_tab(url: str) -> None:
    open_new_tab_successfully = webbrowser.open_new_tab(url)
    if not open_new_tab_successfully:
        msg = f"Could not open browser for URI: {url}. "
        raise BrowserOpenError(msg)


# TODO -> Remove
def open_html_blob_in_the_browser_old(html_source: str) -> None:
    data = base64.b64encode(html_source.encode()).decode("ascii")
    url = "data:text/html;charset=utf-8;base64," + data
    _open_new_tab(url)


def open_html_blob_in_the_browser_old2(html_source: str, *, data_url_max: int = DATA_URL_MAX) -> None:
    """
    Open an HTML string in the default browser.

    Strategy:
      1) Try a data: URL for small content.
      2) Fallback: write a temporary .html and open file://.

    Raises:
        BrowserOpenError: if the browser could not be launched.
    """
    source_bytes = html_source.encode()

    # 1) data: URL for small pages (fast, no disk I/O)
    if len(source_bytes) <= data_url_max:
        url = "data:text/html;charset=utf-8;base64," + base64.b64encode(source_bytes).decode("ascii")
        _open_new_tab(url)
        return

    # 2) Fallback: temp file + file:// URL (reliable)
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
        f.write(html_source)
        path = Path(f.name)

    _open_new_tab(path.as_uri())


def open_html_in_the_browser(html_source: str) -> None:
    """
    Open an HTML string in the default browser.

    Strategy:
        write a temporary .html and open file://.

    Raises:
        BrowserOpenError: if the browser could not be launched.
    """
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
        f.write(html_source)
        path = Path(f.name)

    _open_new_tab(path.as_uri())


def save_pretty_html(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    file_path: StrPath,
) -> None:
    console = _get_pretty_html_console(source, theme=theme, record=True)
    console.save_html(path=str(file_path))


def display_pretty_html_in_the_browser(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
) -> None:
    open_html_in_the_browser(export_pretty_html(source, theme=theme))


def export_pretty_html(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
) -> str:
    console = _get_pretty_html_console(source, theme=theme, record=True)
    return console.export_html()


def pretty_print_html(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> None:
    """
    Render HTML with syntax highlighting inside a compact, styled panel.

    Args:
        source: The HTML source to render.
        theme: Pygments style name; falls back (meaning: uses a safe default) if unknown.
        record: Boolean to enable recording of terminal output.
    Raises:
        ModuleNotFoundError: If Rich (and its dependencies) are not available.
    """
    _get_pretty_html_console(source, theme=theme, record=record)


def _get_pretty_html_console(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> Console:
    try:
        from rich import box
        from rich.console import Console
        from rich.panel import Panel
        from rich.syntax import Syntax
        from rich.text import Text
    except ModuleNotFoundError:
        raise ModuleNotFoundError(EXTRA_FEATURE_PRETTY_ERROR_MESSAGE) from None
    else:
        syntax = Syntax(source, SYNTAX_LEXER, theme=theme, line_numbers=True, indent_guides=True, word_wrap=True)
        title = Text(PANEL_TITLE, style=PANEL_TITLE_STYLE)
        panel = Panel.fit(
            syntax,
            box=box.HEAVY,
            border_style=PANEL_BORDER_STYLE,
            title=title,
        )
        buffer = StringIO() if record else None
        console = Console(record=record, file=buffer)
        console.print(panel, soft_wrap=False)
        return console


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
