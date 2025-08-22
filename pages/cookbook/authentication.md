# Authentication

How to handle login and authentication in your application. It does not cover authorization, which is a separate topic covering what permissions a user has.

## A minimal authentication example

This first example shows how to create a password-less authentication flow using Air. This is a toy example that uses sessions to keep track of the logged-in user. In a real application, you would want to use a more secure method of authentication, with passwords or OAuth.


```python
import air
from time import time

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")


@app.page
async def index(request: air.Request):
    if "username" in request.session:
        # User is logged in provide a logout link
        action = air.Tags(
            air.H1(request.session["username"]),
            air.P(request.session.get("logged_in_at")),
            air.P(air.A("Logout", href="/logout")),
        )
    else:
        # login the user
        action = air.Form(
            air.Label("Name:", for_="username"),
            air.Input(type="text", name="username", id="username", required=True, autofocus=True),
            air.Button("Login", type="submit"),
            action="/login",
            method="post",
        )
    return air.layouts.mvpcss(action)


@app.post("/login")
async def login(request: air.Request):
    form = await request.form()
    if username := form.get("username"):
        # Create session
        request.session["username"] = username
        request.session["logged_in_at"] = time()

    return air.responses.RedirectResponse("/", status_code=302)


@app.page
async def logout(request: air.Request):
    request.session.pop("username")
    return air.responses.RedirectResponse("/")
```