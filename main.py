import importlib
from pathlib import Path
from random import sample

import air
from air_markdown import TailwindTypographyMarkdown as Markdown
from fastapi import HTTPException

from pages import charts, home, why

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
    return air.I(
        why.reasons_not_to_use_air(),
        hx_trigger="every 3s",
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
