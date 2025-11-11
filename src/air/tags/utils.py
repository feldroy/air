"""Utilities for the Air Tag system."""

from __future__ import annotations

import base64
import html
import tempfile
import webbrowser
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Any, Final
from urllib.error import URLError

from lxml import (
    etree,  # ty: ignore[unresolved-import]
    html as l_html,
)
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from air.exceptions import BrowserOpenError

type StrPath = PathLike | Path | str

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
DATA_URL_MAX: Final[int] = 32_000
BLOB_URL_PRESET = "data:text/html;charset=utf-8;base64,"


def clean_html_attr_key(key: str) -> str:
    """Normalize attribute names to align with HTML conventions.

    Args:
        key: Attribute name supplied by the caller.

    Returns:
        The normalized attribute name compatible with HTML.
    """
    # If a "_"-suffixed proxy for "class", "for", or "id" is used,
    # convert it to its normal HTML equivalent.
    key = {"class_": "class", "for_": "for", "id_": "id", "as_": "as", "async_": "async"}.get(key, key)
    # Remove leading underscores and replace underscores with dashes
    return key.lstrip("_").replace("_", "-")


def pretty_format_html(
    source: str,
    *,
    with_body: bool = False,
    with_head: bool = False,
    with_doctype: bool = False,
) -> str:
    """Pretty-print HTML and unescape common entities in the result.

    Args:
        source: Raw HTML markup to format.
        with_body: Whether to wrap the markup in a `<body>` element.
        with_head: Whether to include a `<head>` element when `with_body` is set.
        with_doctype: Whether to prefix the result with a doctype declaration.

    Returns:
        The formatted HTML string with entities such as `&lt;` unescaped.

    Note:
        Entity unescaping applies to attribute values as well; use this helper only with trusted HTML.
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
    """Format HTML markup using `lxml`.

    Args:
        source: Raw HTML markup to format.
        with_body: Whether to ensure a `<body>` element is present.
        with_head: Whether to add a `<head>` element when `with_body` is enabled.
        with_doctype: Whether to include a doctype declaration in the result.
        pretty: Whether to indent the output for readability.

    Returns:
        The serialized HTML produced by `lxml.html.tostring`.
    """
    source = l_html.document_fromstring(source, ensure_head_body=with_head) if with_body else l_html.fromstring(source)
    if pretty:
        etree.indent(source)  # pretty indentation
    doctype = HTML_DOCTYPE if with_doctype else None
    return l_html.tostring(source, encoding=FORMAT_HTML_ENCODING, pretty_print=pretty, doctype=doctype)


def open_local_file_in_the_browser(path: StrPath) -> None:
    """Open a local HTML file in the default browser.

    Args:
        path: Path to a file or directory containing an `index.html`.

    Raises:
        FileNotFoundError: The path does not exist or `index.html` is missing.
        BrowserOpenError: The browser command failed to launch.
    """
    path = Path(path)
    if path.is_dir():
        path /= "index.html"
    if not path.exists():
        raise FileNotFoundError(path)

    url = path.expanduser().resolve().as_uri()
    _open_new_tab(url)


def _open_new_tab(url: str) -> None:
    """Launch a new browser tab for the provided URL.

    Args:
        url: The URL to open.

    Raises:
        BrowserOpenError: The browser invocation returned a failure signal.
    """
    open_new_tab_successfully = webbrowser.open_new_tab(url)
    if not open_new_tab_successfully:
        msg = f"Could not open browser for URI: {url}. "
        raise BrowserOpenError(msg)


def open_html_blob_in_the_browser(html_source: str, *, data_url_max: int = DATA_URL_MAX) -> None:
    """Open HTML content encoded as a data URL in the browser.

    Args:
        html_source: HTML markup to embed in a data URL.
        data_url_max: Maximum permitted URL length before falling back to a file.

    Raises:
        URLError: The data URL exceeds the configured maximum length.
    """
    source_bytes = html_source.encode()
    url = BLOB_URL_PRESET + base64.b64encode(source_bytes).decode("ascii")
    if len(url) >= data_url_max:
        msg = "html_source is to long!"
        raise URLError(msg)
    _open_new_tab(url)


def open_html_in_the_browser(html_source: str) -> None:
    """Open an HTML string in the browser via a temporary file.

    Args:
        html_source: HTML markup to render in the browser.

    Raises:
        BrowserOpenError: The browser command failed.
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
    """Persist syntax-highlighted HTML to a file.

    Args:
        source: HTML markup to render with syntax highlighting.
        theme: Rich syntax highlighting theme name.
        file_path: Destination file path for the exported HTML.
    """
    console = _get_pretty_html_console(source, theme=theme, record=True)
    console.save_html(path=str(file_path))


def display_pretty_html_in_the_browser(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
) -> None:
    """Open syntax-highlighted HTML in the browser.

    Args:
        source: HTML markup to render with syntax highlighting.
        theme: Rich syntax highlighting theme name.
    """
    open_html_in_the_browser(export_pretty_html(source, theme=theme))


def export_pretty_html(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
) -> str:
    """Return syntax-highlighted HTML for display elsewhere.

    Args:
        source: HTML markup to render with syntax highlighting.
        theme: Rich syntax highlighting theme name.

    Returns:
        The rendered HTML containing the highlighted markup.
    """
    console = _get_pretty_html_console(source, theme=theme, record=True)
    return console.export_html()


def pretty_print_html(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> None:
    """Render HTML with syntax highlighting inside a styled terminal panel.

    Args:
        source: HTML markup to render.
        theme: Rich syntax highlighting theme name.
        record: Whether to buffer the output for later export.

    Raises:
        ModuleNotFoundError: The optional Rich dependency is unavailable.
    """
    _get_pretty_html_console(source, theme=theme, record=record)


def _get_pretty_html_console(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> Console:
    """Return a Rich console configured for HTML syntax highlighting.

    Args:
        source: HTML markup to render.
        theme: Rich syntax highlighting theme name.
        record: Whether to buffer the console output.

    Returns:
        A configured Rich console instance.
    """
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
    """Filter local variables for keyword argument construction.

    Args:
        data: Dictionary of local variables to filter.
        _skip: Keys that should remain excluded from the result.

    Returns:
        A dictionary containing only keyword-safe values.
    """
    return {key: value for key, value in data.items() if value is not None and key[0] != "_" and key not in _skip}


class SafeStr(str):
    """String subclass that bypasses HTML escaping when rendered."""
