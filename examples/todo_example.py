from typing import Any

from fastapi import Depends

import air
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
        air.Body(*[x for x in body_tags]),
    )


def _check_user(request: air.Request) -> Any | None:
    return request.session.get("username") if hasattr(request, "session") else None


def _require_login(request: air.Request):
    # Replace this with your actual login check
    username = _check_user(request=request)

    if not username and request.htmx.is_hx_request:
        return air.Div(**{"hx_on::load": f"window.location.replace({index.url()})"})
    if not username:
        # Redirect if not logged in
        raise air.HTTPException(
            status_code=307,
            headers={"Location": index.url()},
        )
    return username


require_login = Depends(_require_login)


@app.page
async def index(request: air.Request) -> air.BaseTag:
    print(request.session.get("user"))
    if request.session.get("user") if hasattr(request, "session") else False:
        print(request.session.get("user"))
        return air.RedirectResponse(dashboard.url())
    title = "TODOs Login"
    return layout(
        air.Title(title),
        air.H1(title),
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
            air.P(air.Button("Login / Create Account", type="submit")),
            action="/login",
            method="post",
        ),
    )


@app.post("/login")
async def login(request: air.Request):
    form = await request.form()
    request.session["username"] = form.get("username")
    return air.RedirectResponse("/dashboard", status_code=303)


@app.post("/logout")
async def logout(request: air.Request):
    request.session.pop("user")
    return air.Div(**{"hx_on::load": "window.location.replace('/')"})


@app.page
async def dashboard(request: air.Request, username=require_login):
    title = f"TODOs Dashboard for {username}"
    return layout(air.Title(title), air.H1(title), air.P(air.U("Logout", hx_post=logout.url())), air.Ol())
