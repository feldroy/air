from inline_snapshot import snapshot
from inline_snapshot.extra import transformation

from air import Html, H1
from textwrap import dedent


@transformation
def clean_doc_with_transformation(text: str) -> str:
    return dedent(text).lstrip()


def clean_doc(text: str) -> str:
    return dedent(text).lstrip()


# The test failed, some snapshots in this test have incorrect values.
def test_render_with_inline_snapshot_and_transformation() -> None:
    actual_html = Html(H1("Cheese Monger")).pretty_render()
    expected_html = clean_doc_with_transformation(
        snapshot(
            """
            <!doctype html>
            <html>
              <body>
                <h1>Cheese Monger</h1>
              </body>
            </html>
            """
        )
    )
    assert actual_html == expected_html


# The test passed successfully
def test_render_with_inline_snapshot() -> None:
    actual_html = Html(H1("Cheese Monger")).pretty_render()
    expected_html = snapshot(
        clean_doc(
            """
            <!doctype html>
            <html>
              <body>
                <h1>Cheese Monger</h1>
              </body>
            </html>
            """
        )
    )
    assert actual_html == expected_html


# The test passed successfully
def test_render_without_inline_snapshot() -> None:
    actual_html = Html(H1("Cheese Monger")).pretty_render()
    expected_html = clean_doc(
        """
        <!doctype html>
        <html>
          <body>
            <h1>Cheese Monger</h1>
          </body>
        </html>
        """
    )
    assert actual_html == expected_html
