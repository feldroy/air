from pathlib import Path

import air

def make_link_from_pyfile(path: Path):
    # Remove .py extension and use as link name and href
    name = path.name[:-3]
    return air.A(name.replace('_', ' ').title(), href=f"learn/{name}")

def render(request: air.Request):
    files = Path("pages/learn").glob("*.py")
    links = [air.Li(make_link_from_pyfile(x)) for x in files]
    return air.Children(
        air.Title("Learn: Air Python Web Framework"),
        air.Article(
            air.H1("Learn"),
            air.P("Welcome to the Air Learn section! Choose a topic below:"),
            air.Ul(*links),
            class_="prose",
        ),
    )