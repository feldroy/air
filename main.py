import importlib
from pathlib import Path
from os import getenv
from functools import cache
import importlib
import inspect
import pkgutil
from typing import Any, List, ParamSpec,TypeVar
import html

import air
from air_markdown.tags import AirMarkdown
from fastapi import HTTPException
import sentry_sdk


from pages import charts, home, why

renderer = air.JinjaRenderer("templates")

SENTRY_DSN = getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )

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


@app.page
def error_check():
    three = 1 / 0
    return air.H1("This will never be seen")


@app.get("/llms.txt")
async def llms_txt():
    return air.responses.FileResponse("llms.txt")


@cache
def get_air_objects() -> List[Any]:
    """
    Gets all the objects in the `air` package that are defined within air
    (nothing imported into air from core python or other libraries).

    Returns:
        A list of these objects.
    """
    air_objects = set()
    prefix = air.__name__ + "."
    for _, module_name, _ in pkgutil.walk_packages(air.__path__, prefix):
        try:
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module):
                if hasattr(obj, "__module__") and obj.__module__.startswith(
                    air.__name__
                ):
                    air_objects.add(obj)
        except Exception:
            continue
    return list(air_objects)


reference_warning = air.Section(
                air.Aside(
                    air.Strong("WARNING:", style="color: red"),
                    " This API reference is very new and there are unsolved formatting challenges.",
                )
            )


@app.page
async def reference(request: air.Request):
    modules = [
        air.Li(air.A(x, href=f"/reference/{x}"))
        for x in sorted(list(set([x.__module__ for x in get_air_objects()])))
    ]
    return layout(
        request, air.Article(air.H1("API Reference"), reference_warning, air.Ul(*modules), class_="prose")
    )


def doc_obj(obj):
    if obj.__module__ in ("air.tags.models.stock",):
        doc = (
            AirMarkdown(html.escape(obj.__doc__))
            if (hasattr(obj, "__doc__") and isinstance(obj.__doc__, str))
            else ""
        )
    else:
        doc = (
            AirMarkdown(obj.__doc__)
            if (hasattr(obj, "__doc__") and isinstance(obj.__doc__, str))
            else ""
        )
    return air.Section(
        air.H2(obj.__name__, air.Small(f"  ({obj.__module__}.{obj.__name__})")), doc
    )


@app.get("/reference/{module:path}")
def reference_module(request: air.Request, module: str):
    objects = [
        x
        for x in get_air_objects()
        if x.__module__ == module and not isinstance(x, (ParamSpec, TypeVar))
    ]
    objects = [doc_obj(x) for x in sorted(objects, key=lambda x: x.__name__)]
    return layout(
        request,
        air.Article(
            air.H1(air.A("API Reference:", href="/reference"), " ", module),
            reference_warning,
            air.Ul(*objects),
            class_="prose",
        ),
    )


@app.get("/{slug:path}")
def airpage(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(request, AirMarkdown(text))
    path = Path(f"pages/{slug}.py")
    if path.exists():
        module_name = f"pages.{slug.replace('/', '.')}"
        mod = importlib.import_module(module_name)
        return layout(request, mod.render(request))
    raise HTTPException(status_code=404)
