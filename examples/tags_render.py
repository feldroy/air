"""
A utility script to generate, render, and syntax-highlight HTML for terminal
output using the `rich` library.

The script leverages various imported components to construct an HTML
structure. It then utilizes a rendering function to display the generated
HTML in a nicely formatted panel with syntax highlighting and stylized
borders in the terminal.
Run:
    `uv sync --all-extras --no-extra standard`
    `uv run -q examples/tags_render.py`
"""

from __future__ import annotations

from rich import box, print
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from air import A, Div, Img, Link, P, Script


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
    a = A("Air", data_cloud=True, data_earth="true")
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
        P(a, img),
        class_="class1",
        id="id1",
        style="style1",
        kwarg1="kwarg1",
        kwarg2="kwarg2",
        kwarg3="kwarg3",
    )
    div.is_pretty = True
    # Render the generated Tag nicely in the terminal
    print(div.__repr__())
    # Raw tag representation
    print(div.raw_repr())
    # Dict tag representation
    print(div.to_dict())
    # Render the generated HTML nicely in the terminal
    render_html_pretty(str(div))
