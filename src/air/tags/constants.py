from __future__ import annotations

import re
from typing import Final, Literal

from frozendict import frozendict

# noinspection PyUnresolvedReferences
from pygments.lexers.html import HtmlLexer

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer


class TagKeys:
    NAME: Final = "name"
    ATTRIBUTES: Final = "attributes"
    CHILDREN: Final = "children"


LOCALS_CLEANUP_EXCLUDED_KEYS: Final[frozenset[str]] = frozenset({
    "self",
    "children",
    "text_child",
    "args",
    "kwargs",
})
ATTRIBUTES_TO_AIR: Final = frozendict({
    "class": "class_",
    "for": "for_",
    "id": "id_",
    "as": "as_",
    "async": "async_",
})
ATTRIBUTES_TO_HTML: Final = frozendict({
    "class_": "class",
    "for_": "for",
    "id_": "id",
    "as_": "as",
    "async_": "async",
})
FORMAT_HTML_ENCODING: Final = "unicode"
HTML_DOCTYPE: Final = "<!doctype html>"
DEFAULT_THEME: Final = "dracula"
HTML_PANEL_TITLE: Final = "Air → HTML"
PYTHON_PANEL_TITLE: Final = "HTML → Air"
type PanelTitleType = Literal["Air → HTML", "HTML → Air"]
PANEL_TITLE_STYLE: Final = "italic bold"
PANEL_BORDER_STYLE: Final = "bright_magenta"
SYNTAX_LEXER: Final = "python"
DATA_URL_MAX: Final = 32_000
DEFAULT_ENCODING = "utf-8"
BLOB_URL_PRESET = f"data:text/html;charset={DEFAULT_ENCODING};base64,"
DEFAULT_INDENTATION_SIZE: Final = 4
INDENT_UNIT: Final = " " * 4
INLINE_JOIN_SEPARATOR: Final = ", "
MULTILINE_JOIN_SEPARATOR: Final = ",\n"
HTML_ATTRIBUTES_JOIN_SEPARATOR: Final = " "
EMPTY_JOIN_SEPARATOR: Final = ""
AIR_PREFIX: Final = "air."
HTML_LEXER: Final = HtmlLexer()
PYTHON_LEXER: Final = PythonLexer()
_LOOKS_LIKE_FULL_HTML_UNICODE_RE: Final = re.compile(
    r"""
    ^\s*
    (?:<!doctype\s+html\b[^>]*>\s*)?
    <html\b[^>]*>
    (?=.*(?:<head\b[^>]*>.*?</head\s*>|<body\b[^>]*>.*?</body\s*>))
    .*?</html\s*>
    \s*$
    """,
    re.IGNORECASE | re.DOTALL | re.VERBOSE,
)
