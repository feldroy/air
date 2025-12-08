from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from pygments.lexers.html import HtmlLexer

    # noinspection PyUnresolvedReferences
    from pygments.lexers.python import PythonLexer

type LexerType = HtmlLexer | PythonLexer
type StrPath = PathLike | Path | str
