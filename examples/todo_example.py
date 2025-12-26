import csv

import air
from fastapi import Depends
from typing import Any
from air.tags.models.types import AttributeType



app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")


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


def _check_user(request: air.Request) -> Any | None:
    return request.session.get("user") if hasattr(request, "session") else None

def _require_login(request: air.Request):
    # Replace this with your actual login check
    user = _check_user(request=request)  

    if not user:
        # Redirect if not logged in
        raise air.HTTPException(
            status_code=307,
            headers={"Location": "/login"},
        )
    return user
require_login = Depends(_require_login)


@app.page
def index(user=require_login) -> air.BaseTag:
    title = "TODOs"
    return layout(
        air.Title(title),
        air.H1(title),
    )

@app.page
async def login():
    return layout(
        air.H1('TODOs Login'),
        # login the user
        air.Form(
            air.P(
            air.Label("Username:", for_="username"),
            air.Input(type="text", name="username", id="username", required=True, autofocus=True),
            ),
            air.P(
            air.Label("Password:", for_="password"),
            air.Input(type="password", name="password", id="password", required=True, autofocus=True),            
            ),
            air.P(air.Button("Login", type="submit")),
            action="/login",
            method="post",
        )    
    )