from textwrap import dedent

from inline_snapshot.extra import transformation


@transformation
def clean_doc(text: str) -> str:
    return dedent(text).lstrip()
