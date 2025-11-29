# Authentication

How to handle login and authentication in your application. It does not cover authorization, which is a separate topic covering what permissions a user has.

## A minimal authentication example

This first example shows how to create a password-less authentication flow using Air. This is a toy example that uses sessions to keep track of the logged-in user. In a real application, you would want to use a more secure method of authentication, with passwords or OAuth.

```
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

## Authentication with Dependencies

In Air and FastAPI apps we frequently rely on dependencies to handle authentication. Dependencies are a powerful way to share logic between different parts of your application. Here's a simple authentication dependency example:

```
import air
from fastapi import HTTPException

def require_login(request: air.Request):
    # Replace this with your actual login check
    user = request.session.get("user") if hasattr(request, "session") else None  

    if not user:
        # Redirect if not logged in
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
        )
    return user
```

In Air, like FastAPI, session objects need to be serializable to JSON. That means you can't store complex objects like database models directly in the session. Instead, store simple identifiers (like user IDs) and fetch the full user details from your database as needed.

Attaching this dependency to a route ensures that only authenticated users can access it. If a user is not authenticated, they will be redirected to the login page. Here's how you can use the `require_login` dependency in a route:

```
import air

app = air.Air()
air.add_middleware(air.SessionMiddleware, secret_key="change-me")

# --- Dependency ---
def require_login(request: air.Request):
    # Replace this with your actual login check
    user = request.session.get("user") if hasattr(request, "session") else None  

    if not user:
        # Redirect if not logged in
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
        )
    return user

# --- Routes ---
@app.page
async def dashboard(request: air.Request, user=Depends(require_login)):
    return air.layouts.mvpcss(
        air.H1(f"Dashboard for {request.session['user']['username']}"),
        air.P(air.A('Logout', href='/logout'))
    )
```

Here's a more complete example that includes a login page, a protected dashboard page, and logout functionality using the `require_login` dependency:

```
import air
from fastapi import Depends, HTTPException

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")

# --- Dependency ---
def require_login(request: air.Request):
    # Replace this with your actual login check
    user = request.session.get("user") if hasattr(request, "session") else None  

    if not user:
        # Redirect if not logged in
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
        )
    return user

# --- Routes ---
@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1('Landing page'),
        air.P(air.A('Dashboard', href='/dashboard'))
    )    

@app.page
async def login():
    return air.layouts.mvpcss(
        air.H1('Login'),
        # login the user
        air.Form(
            air.Label("Name:", for_="username"),
            air.Input(type="text", name="username", id="username", required=True, autofocus=True),
            air.Label("Password:", for_="password"),
            air.Input(type="password", name="password", id="password", required=True, autofocus=True),            
            air.Button("Login", type="submit"),
            action="/login",
            method="post",
        )    
    )


@app.page
async def dashboard(request: air.Request, user=Depends(require_login)):
    return air.layouts.mvpcss(
        air.H1(f"Dashboard for {request.session['user']['username']}"),
        air.P(air.A('Logout', href='/logout'))
    )

@app.post('/login')
async def login(request: air.Request):
    form = await request.form()
    request.session['user'] = dict(username=form.get('username'))
    return air.RedirectResponse('/dashboard', status_code=303)

@app.page
async def logout(request: air.Request):
    request.session.pop('user')
    return air.RedirectResponse('/', status_code=303)
```
