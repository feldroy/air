from __future__ import annotations

from typing import Final

FORMAT_HTML_ENCODING: Final = "unicode"
HTML_DOCTYPE: Final = "<!doctype html>"
DEFAULT_THEME: Final = "dracula"
PANEL_TITLE: Final = "Air → HTML"
PANEL_TITLE_STYLE: Final = "italic bold"
PANEL_BORDER_STYLE: Final = "bright_magenta"
SYNTAX_LEXER: Final = "html"
DATA_URL_MAX: Final = 32_000
DEFAULT_ENCODING = "utf-8"
BLOB_URL_PRESET = f"data:text/html;charset={DEFAULT_ENCODING};base64,"
LOCALS_CLEANUP_EXCLUDED_KEYS: Final[frozenset[str]] = frozenset({
    "self",
    "children",
    "text_child",
    "args",
    "kwargs",
})
TOP_LEVEL_HTML_TAGS: Final[frozenset[str]] = frozenset({
    HTML_DOCTYPE,
    "<html",
    "<head",
    "<body",
})
DEFAULT_INDENTATION_SIZE = 4
INDENT_UNIT: Final = " " * 4
INLINE_JOIN_SEPARATOR = ", "
MULTILINE_JOIN_SEPARATOR = ",\n"
HTML_ATTRIBUTES_JOIN_SEPARATOR = " "
EMPTY_JOIN_SEPARATOR = ""
