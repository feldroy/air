"""
A utility script to generate, render, and syntax-highlight HTML for terminal
output using the `rich` library.

The script leverages various imported components to construct an HTML
structure. It then utilizes a rendering function to display the generated
HTML in a nicely formatted panel with syntax highlighting and stylized
borders in the terminal.
Run:
    `just run-py-module examples.tags_render`
"""

from __future__ import annotations

from rich import print

from examples.html_sample import SMALL_HTML_SAMPLE, HTML_SAMPLE

if __name__ == "__main__":
    pass
