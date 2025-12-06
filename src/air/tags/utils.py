"""Utilities for the Air Tag system."""

from __future__ import annotations

import base64
import html
import re
import tempfile
import webbrowser
from collections import UserString
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.error import URLError

import minify_html
from lxml.etree import indent as indent_element_tree

# noinspection PyProtectedMember
from lxml.html import (
    HtmlElement,
    document_fromstring as parse_html_document_from_string,
    fromstring as parse_html_from_string,
    tostring as serialize_document_to_html_string,
)
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from air.exceptions import BrowserOpenError

from .constants import (
    _LOOKS_LIKE_FULL_HTML_UNICODE_RE,
    ATTRIBUTES_TO_AIR,
    ATTRIBUTES_TO_HTML,
    BLOB_URL_PRESET,
    DATA_URL_MAX,
    DEFAULT_ENCODING,
    DEFAULT_THEME,
    FORMAT_HTML_ENCODING,
    HTML_DOCTYPE,
    HTML_LEXER,
    HTML_PANEL_TITLE,
    LOCALS_CLEANUP_EXCLUDED_KEYS,
    PANEL_BORDER_STYLE,
    PANEL_TITLE_STYLE,
    PYTHON_LEXER,
    PYTHON_PANEL_TITLE,
    PanelTitleType,
)

if TYPE_CHECKING:
    from .types import LexerType, StrPath


def is_full_html_document(text: str) -> bool:
    """Check if a string looks like a full HTML document using a simple heuristic

    The check allows an optional <!doctype html> at the start, requires a root
    <html>...</html> element that spans the whole input, and requires at least
    one complete <head>...</head> or <body>...</body> pair somewhere inside the
    <html> element. Whitespace anywhere in the input is ignored as far as HTML
    normally ignores it.

    Args:
        text: HTML source string to test.

    Returns:
        True if the input looks like a full HTML document,
        otherwise False.
    """
    return bool(_LOOKS_LIKE_FULL_HTML_UNICODE_RE.fullmatch(text))


def migrate_attribute_name_to_html(attr_name: str) -> str:
    """Normalize attribute names to align with HTML conventions.

    Args:
        attr_name: Attribute name supplied by the caller.

    Returns:
        The normalized attribute name compatible with HTML.

    Notes:
        Proxies such as ``class_``, ``for_``, ``id_``, ``as_``, and ``async_`` are converted to their
        standard HTML counterparts. Leading underscores are stripped and remaining underscores become
        dashes to match HTML attribute naming rules.
    """
    attr_name = ATTRIBUTES_TO_HTML.get(attr_name, attr_name)
    return attr_name.lstrip("_").replace("_", "-")


def migrate_attribute_name_to_air_tag(attr_name: str) -> str:
    """Normalize HTML attribute names for Air tag reconstruction.

    Args:
        attr_name: An uncleaned HTML attribute key.

    Returns:
        Normalized attribute key compatible with Air tags.

    Notes:
        HTML-reserved attribute names such as ``class``, ``for``, ``id``, ``as``, and ``async`` are
        mapped to the underscore-suffixed proxies used by Air tags. Leading underscores are stripped
        and remaining underscores become dashes to normalize the key.
    """
    attr_name = ATTRIBUTES_TO_AIR.get(attr_name, attr_name)
    return attr_name.replace("-", "_")


def extract_html_comment(text: str) -> str:
    """Extract the inner content of an HTML comment string.

    Args:
        text: Raw HTML comment, including the ``<!--`` and ``-->`` markers.

    Returns:
        The comment body with surrounding whitespace stripped.

    Raises:
        ValueError: If the input is not a well-formed HTML comment.

    Examples:
        >>> extract_html_comment("<!-- hello -->")
        'hello'
    """
    if match := re.fullmatch(r"\s*<!--\s*(.*?)\s*-->\s*", text, flags=re.DOTALL):
        return match.group(1).strip()
    msg = "Input is not a valid HTML comment"
    raise ValueError(msg)


def compact_format_html(source: str) -> str:
    """Minify HTML markup with safe defaults.

    Args:
        source: Raw HTML markup to compress.

    Returns:
        Space-efficient HTML suitable for inline embedding or network transfer.

    Note:
        Configuration opts into standards-safe options from ``minify_html`` to
        retain required attribute spacing while stripping comments, optional
        closing tags, and excess whitespace, and to minify inline CSS/JS.
    """
    # noinspection PyArgumentEqualDefault
    return minify_html.minify(
        source,  # your HTML string
        allow_noncompliant_unquoted_attribute_values=False,  # keep spec-legal quoting
        allow_optimal_entities=False,  # avoid entity tweaks that fail validation
        allow_removing_spaces_between_attributes=False,  # keep the required inter-attribute space
        keep_closing_tags=False,  # drop optional closing tags
        keep_comments=False,  # remove comments
        keep_html_and_head_opening_tags=False,  # drop optional <html>/<head> openings
        keep_input_type_text_attr=False,  # drop default type="text"
        keep_ssi_comments=False,  # remove SSI comments
        minify_css=True,  # minify <style>/style=""
        minify_doctype=False,  # don't over-minify DOCTYPE (can be non-spec)
        minify_js=True,  # minify inline <script>
        preserve_brace_template_syntax=False,  # assume real HTML, not templates
        preserve_chevron_percent_template_syntax=False,  # assume real HTML, not templates
        remove_bangs=False,  # keep “!” so declarations stay valid
        remove_processing_instructions=True,  # strip stray PIs (<?…?>)
    )


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
    html_element: HtmlElement = (
        parse_html_document_from_string(source, ensure_head_body=with_head)
        if with_body
        else parse_html_from_string(source)
    )
    if pretty:
        indent_element_tree(html_element)  # ty: ignore[invalid-argument-type]
    doctype = HTML_DOCTYPE if with_doctype else None
    # noinspection PyTypeChecker
    return serialize_document_to_html_string(
        doc=html_element, encoding=FORMAT_HTML_ENCODING, pretty_print=pretty, doctype=doctype
    )


def open_local_file_in_the_browser(path: StrPath) -> None:
    """Open a local HTML file in the default browser.

    Args:
        path: Path to a file or directory containing an `index.html`.

    Raises:
        FileNotFoundError: The path does not exist or `index.html` is missing.
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
    """
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding=DEFAULT_ENCODING) as f:
        f.write(html_source)
        path = Path(f.name)

    _open_new_tab(path.as_uri())


def save_text(text: str, file_path: StrPath) -> None:
    """Saves the provided text to a specified file path.

    This function writes the given string data to a file at the provided path
    using a specified encoding.

    Args:
        text: The text content to be saved in the file.
        file_path: The path to the file where the text will be saved.
    """
    Path(file_path).write_text(data=text, encoding=DEFAULT_ENCODING)


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


def pretty_print_python(
    source: str,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> None:
    """Render Python with syntax highlighting inside a styled terminal panel.

    Args:
        source: HTML markup to render.
        theme: Rich syntax highlighting theme name.
        record: Whether to buffer the output for later export.
    """
    _get_pretty_console(source, lexer=PYTHON_LEXER, panel_title=PYTHON_PANEL_TITLE, theme=theme, record=record)


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
    return _get_pretty_console(source, lexer=HTML_LEXER, panel_title=HTML_PANEL_TITLE, theme=theme, record=record)


def _get_pretty_console(
    source: str,
    lexer: LexerType,
    panel_title: PanelTitleType,
    *,
    theme: str = DEFAULT_THEME,
    record: bool = False,
) -> Console:
    """Generates a Rich console with formatted code syntax displayed within a styled panel.

    The console object is configured to display source code syntax highlighting using the
    specified lexer and theme within a panel with a title. Additionally, the console can
    optionally record its output to a buffer.

    Args:
        source: HTML markup to render.
        lexer: The syntax highlighter to use, either for HTML or Python code.
        panel_title: The title to display on the panel's border.
        theme: Rich syntax highlighting theme name.
        record: Whether to buffer the console output.

    Returns:
        A configured Console instance with the styled syntax and panel displayed.
    """
    syntax = Syntax(code=source, lexer=lexer, theme=theme, line_numbers=True, indent_guides=True, word_wrap=True)
    title = Text(panel_title, style=PANEL_TITLE_STYLE)
    panel = Panel(
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
    _skip: frozenset[str] = LOCALS_CLEANUP_EXCLUDED_KEYS,
) -> dict[str, Any]:
    """Filter local variables for keyword argument construction.

    Args:
        data: Dictionary of local variables to filter.
        _skip: Keys that should remain excluded from the result.

    Returns:
        A dictionary containing only keyword-safe values.
    """
    return {key: value for key, value in data.items() if value is not None and key[0] != "_" and key not in _skip}


class SafeStr(UserString):
    """String subclass that bypasses HTML escaping when rendered."""
