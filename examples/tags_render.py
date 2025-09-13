"""
A utility script to generate, render, and syntax-highlight HTML for terminal
output using the `rich` library.

The script leverages various imported components to construct an HTML
structure. It then utilizes a rendering function to display the generated
HTML in a nicely formatted panel with syntax highlighting and stylized
borders in the terminal.
Run:
    `uv sync --all-extras --no-extra standard`
    `just run examples.tags_render`
"""

from __future__ import annotations

from rich import box, print
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from air import H1, H2, H3, A, B, Div, Img, Link, P, SafeStr, Script
from examples.html_sample import HTML_SAMPLE


def render_html_pretty(html: str, *, theme: str = "dracula") -> None:
    """Pretty-print and render HTML with syntax highlighting."""
    syntax = Syntax(
        html,
        "html",
        line_numbers=True,
        word_wrap=True,
    )
    panel = Panel(
        Padding(syntax, (0, 2)),
        box=box.HEAVY,
        title="Air → HTML",
    )
    console = Console()
    console.print(panel, soft_wrap=False)


if __name__ == "__main__":
    link = Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
    )
    script = Script(
        src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
        integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
        crossorigin="anonymous",
    )
    a = A("A", data_cloud=True, data_earth="true")
    b = B("B", data_cloud=True, data_earth="true")
    h1 = H1("H1", data_cloud=True, data_earth="true")
    h2 = H2("H1", data_cloud=True, data_earth="true")
    h3 = H3("H1", data_cloud=True, data_earth="true")
    s1 = A(SafeStr(":root & > < { --pico-font-size: 100%; }"), id="id1")
    s2 = SafeStr("safe <> string")
    s3 = A(":root & > < { --pico-font-size: 100%; }", id="id1")
    script_safe = Script("safe <> Script", crossorigin="anonymous")
    img = Img(
        src="https://cdn.jsdelivr.net/dist/img.png",
        width=250,
        height=100,
        alt="My Img",
        cheched=False,
        selected=True,
        bar="foo",
    )
    div = Div(
        link,
        script,
        P(a, b, b, img),
        P(a, s1, s2, img, "<>", a, script_safe),
        class_="class1",
        id="id1",
        style="style1",
        kwarg1="kwarg1",
        kwarg2="kwarg2",
        kwarg3="kwarg3",
    )
    # Raw tag representation
    print(repr(div))
    # Full tag representation
    print(div.full_repr())
    # Render the generated HTML nicely in the terminal
    render_html_pretty(div.pretty_render())

    # Extra
    print(repr(HTML_SAMPLE.from_dict(HTML_SAMPLE.to_dict())))
    print(repr(HTML_SAMPLE.from_json(HTML_SAMPLE.to_json())))
