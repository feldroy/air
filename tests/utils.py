import re
from inspect import cleandoc
from textwrap import dedent


def undent(text: str) -> str:
    return dedent(text).lstrip()


def undent_with_broken_lines(text: str) -> str:
    return undent(_clean_broken_lines(text))


def clean_doc(text: str) -> str:
    return f"{cleandoc(text)}\n"


def clean_doc_with_broken_lines(text: str) -> str:
    return clean_doc(_clean_broken_lines(text))


def _clean_broken_lines(text: str) -> str:
    return re.sub(r"\s*\\\n\s*", " ", text)
