from pathlib import Path

import air

from airdocs.utils import make_link_from_mdpath


def render(request: air.Request):
    files = Path("pages/concepts").glob("*.md")
    links = [air.Li(make_link_from_mdpath(x)) for x in files]
    return air.Children(
        air.Title("Concepts"),
        air.Article(
            air.H1("Concepts"),
            air.P("Why and how Air works."),
            air.Ul(*links),
            class_="prose",
        ),
    )
