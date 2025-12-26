import csv

import air
from fastapi import Depends
from typing import Any
from air.tags.models.types import AttributeType



app = air.Air()


def layout(*children: Any, **kwargs: AttributeType) -> air.Html | air.Children:
    body_tags = air.layouts.filter_body_tags(children)
    head_tags = air.layouts.filter_head_tags(children)    

    return air.Html(
        air.Head(
            air.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css", type="text/css"),
            air.Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
            *head_tags,
        ),
        air.Body(
            *[x for x in body_tags]
        ),
    )


@app.page
def index() -> air.BaseTag:
    title = "TODOs"
    return air.layouts.mvpcss(
        air.Title(title),
        air.H1(title),

    )