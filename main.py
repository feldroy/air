import importlib
from pathlib import Path
from random import sample

import air
from air_markdown import TailwindTypographyMarkdown as Markdown
from fastapi import HTTPException

from pages import charts, home

renderer = air.JinjaRenderer("templates")

app = air.Air()


def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception("First arg of layout needs to be an air.Request")
    head_tags = air.layouts.filter_head_tags(content)
    body_tags = air.layouts.filter_body_tags(content)
    return renderer(
        request,
        "page.html",
        head_tags=air.Children(*head_tags),
        body_tags=air.Children(*body_tags),
    )


@app.page
def index(request: air.Request):
    return layout(request, home.render(request))


@app.page
def dontuseair():
    reasons = [
        "unless you like living on the edge",
        "unless you believe in unicorns",
        "you like early stage projects",
        "you want to try an early stage project",
        "if you are building something where lives depend on stability",
        "because there's no paid support",
        "as it is just another Python web framework",
        "when you could be using COBOL",
        "if you have a problem with dairy-themed documentation (although we do like spicy vegan cheese dips)",
        "it's better to stay under waterwe're running out",
    ]
    return air.I(
        f"... {sample(reasons, 1)[0]}",
        hx_trigger="every 4s",
        hx_get="/dontuseair",
        hx_swap="outerHTML",
    )


@app.page
def data():
    data = charts.generate_data()
    # This replaces the script in the web page with new data, and triggers
    # an animation of the transition
    return air.Script(
        f"var data = {data}; Plotly.animate('randomChart', data);",
        id="dataSource",
        hx_trigger="every 2s",
        hx_get="/data",
        hx_swap="outerHTML",
    )


@app.get("/{slug:path}")
def airpage(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(request, Markdown(text))
    path = Path(f"pages/{slug}.py")
    if path.exists():
        module_name = f"pages.{slug.replace('/', '.')}"
        mod = importlib.import_module(module_name)
        return layout(request, mod.render(request))
    raise HTTPException(status_code=404)
