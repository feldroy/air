import re
from inspect import cleandoc


def clean_doc(text: str) -> str:
    return f"{cleandoc(text)}\n"


def clean_doc_with_broken_lines(text: str) -> str:
    return clean_doc(_clean_broken_lines(text))


def _clean_broken_lines(text: str) -> str:
    return re.sub(r"\s*\\\n\s*", " ", text)
