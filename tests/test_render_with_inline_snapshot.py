from inline_snapshot import snapshot
from inline_snapshot.extra import transformation

from air import Html, H1
from textwrap import dedent
from inspect import cleandoc

@transformation
def clean_doc_with_transformation(text: str) -> str:
    return dedent(text).lstrip()


from textwrap import dedent


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


def test_doc_with_inline_snapshot_and_transformation() -> None:
    actual_html = """
<!doctype html>
<html>
  <body>
    <h1>Cheese Monger</h1>
  </body>
</html>
        """
    expected_html = snapshot(
        """
        <!doctype html>
        <html>
          <body>
            <h1>Cheese Monger</h1>
          </body>
        </html>
        """
    )
    assert actual_html == clean_doc(expected_html)


def test_doc_with_inline_snapshot() -> None:
    actual_html = """
<!doctype html>
<html>
  <body>
    <h1>Cheese Monger</h1>
  </body>
</html>
        """
    expected_html = snapshot(
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


# The test passed successfully
def test_render_with_inline_snapshot() -> None:
    actual_html = Html(H1("Cheese Monger")).pretty_render()
    expected_html = snapshot(
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


def test_a():
    actual_value = "line1\nline2\n"
    expected_value = snapshot(
        """
        line1
        line2
        """
    )
    assert actual_value == expected_value


def test_b():
    actual_value = "line1\nline2\n"
    expected_value = snapshot(
        clean_doc(
            """
            line1
            line2
            """
        )
    )
    assert actual_value == expected_value

def test_c():
    pass
    # expect("foo").to_match_snapshot()
