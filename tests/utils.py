from textwrap import dedent


def clean_doc(text: str) -> str:
    return dedent(text).lstrip()
