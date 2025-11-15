from __future__ import annotations

from typing import Final

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
LOCALS_CLEANUP_EXCLUDED_KEYS: Final[frozenset[str]] = frozenset(
    {
        "self",
        "children",
        "text_child",
        "args",
        "kwargs",
    }
)
TOP_LEVEL_HTML_TAGS: Final[frozenset[str]] = frozenset(
    {
        HTML_DOCTYPE,
        "<html>",
        "<head>",
        "<body>",
    }
)
