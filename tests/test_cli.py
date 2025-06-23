from air.cli import html
from pathlib import Path


def test_html():
    assert html(Path("input"), Path("public")) == 0
