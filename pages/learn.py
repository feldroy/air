import air
from air_markdown import TailwindTypographyMarkdown as Markdown


def render(request: air.Request):
    return air.Children(
        air.Title("Learn: Air Python Web Framework"),
        Markdown("""
# Learn

Welcome to the Air Learn section! Choose a topic below:

- [Quickstart](learn_quickstart)
- [Tutorial 1: Combining FastAPI and Air](learn_tutorial_1)

More tutorials coming soon!
"""),
    )