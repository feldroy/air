"""Default stylesheet for AirForm-rendered HTML.

Usage in templates::

    <style>{{ airform.default_css()|safe }}</style>

Or in Air Tags::

    air.Style(airform.default_css())
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def default_css() -> str:
    """Return the default AirForm CSS as a string."""
    css_path = Path(__file__).parent / "static" / "airform.css"
    return css_path.read_text()
