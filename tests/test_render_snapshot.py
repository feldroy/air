from inline_snapshot import snapshot
from textwrap import dedent




def test_render_html() -> None:
    actual_value = dedent(
        """
        <div class="container">
            <h1>Welcome</h1>
                <p>This is a paragraph.</p>
        </div>
        """
    )
    expected_value = snapshot()
    assert actual_value == expected_value
