import csv
from pathlib import Path
from time import time
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
    request.session.pop("username")
    return air.Div(**{"hx_on::load": "window.location.replace('/')"})


CSV_PATH = Path(__file__).resolve().parent / "todos.csv"


def _createdb() -> None:
    # Ensure todos.csv exists, create it if it does not
    if CSV_PATH.exists():
        return
    CSV_PATH.write_text("id,title,status,username,order")
    return


def read_todo_by_username(username: str) -> list[dict]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return [x for x in csv.DictReader(f) if x["username"] == username]


def new_todo_form():
    return air.Form(
        air.P(
            air.Label("New todo:", for_="title"),
            air.Input(
                type="text", name="title", id_="title", required=True, autofocus=True, placeholder="Thing I need to do"
            ),
            air.Button("New TODO", type="submit"),
        ),
        hx_post="/new-todo",
        hx_swap="afterbegin",
        hx_target="#listOfTodos",
        hx_swap_oob="true",
        id_="#newTodoForm",
    )


@app.page
async def dashboard(request: air.Request, username=require_login):
    _createdb()
    title = f"TODOs Dashboard for {username}"
    records = read_todo_by_username(username)
    return layout(
        air.Title(title),
        air.H1(title),
        air.P(air.U("Logout", hx_post=logout.url())),
        new_todo_form(),
        air.Ul(*[air.Li(x["title"], id_=x["id"]) for x in records], id_="listOfTodos"),
    )


@app.post("/new-todo")
async def new_todo(request: air.Request, username=require_login) -> air.BaseTag:
    form = await request.form()
    title = form.get("title")
    # Write the next line
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "title", "completed", "username", "order"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(dict(title=title, username=username, completed="False", id=int(time()), order=1))
    return air.Children(
        air.Li(title),
        new_todo_form(),
    )
