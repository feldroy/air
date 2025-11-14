from inline_snapshot import snapshot

from textwrap import dedent
from inspect import cleandoc

def clean_doc(text: str) -> str:
    return dedent(text).lstrip()


def test_doc_with_inline_snapshot() -> None:
    actual_html = Html(H1("Cheese Monger")).pretty_render()
    actual_html = clean_doc(
        """
        <!doctype html>
        <html>
          <body>
            <h1>Cheese Monger</h1>
          </body>
        </html>
        """
    )
    expected_html = snapshot()
    assert actual_html == expected_html
