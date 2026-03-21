# Building Apps with Air

Air is a Python web framework built on FastAPI/Starlette. HTML-first, zero config. This file tells you everything you need to build a complete Air app from scratch.

## Working from HTML Mockups

If the user doesn't have mockups yet, use the `/frontend-design` skill to create static HTML files in `mockups/`. Then follow this workflow starting at step 2.

When the user provides static HTML files as mockups, follow this workflow:

1. **Archive the originals.** If the HTML files aren't already in `mockups/`, move them there so the raw design is preserved as a reference. Delete any copies left behind (e.g. at the project root). Create the directory if it doesn't exist.

2. **Copy to templates/.** Copy each mockup from `mockups/` into `templates/`. This is where Air's Jinja renderer looks for templates. The originals stay in `mockups/` as a reference. Create the directory if it doesn't exist.

3. **Template them.** Convert the static HTML into Jinja templates:
   - Extract repeated structure (nav, footer, head) into a `base.html` with `{% block %}` tags
   - Replace hardcoded text with `{{ variables }}` where the content should come from Python
   - Replace hardcoded URLs with route references
   - Keep `href="/static/..."` paths as-is (Air serves static files at `/static/` automatically)
   - Add `{% extends "base.html" %}` and `{% block content %}` to page templates

4. **Wire up routes.** In `main.py`, use `app.jinja` (auto-created, points at `templates/`) to render:

```python
import air

app = air.Air()

@app.page
def index(request: air.Request):
    return app.jinja(request, "index.html", title="Home")

@app.page
def about(request: air.Request):
    return app.jinja(request, "about.html", title="About")
```

5. **Move static assets.** If the mockups reference CSS, JS, or images, move those into `static/` and update the paths in templates to use `/static/...`.

### Example: mockup to working app

Given a file `landing.html`:

```
mockups/
  landing.html         <- original, untouched
templates/
  base.html            <- extracted layout
  landing.html         <- templated version
static/
  css/style.css        <- extracted from mockup
main.py                <- routes using app.jinja
pyproject.toml
```

## Minimal App

```python
import air

app = air.Air()

@app.page
def index():
    return air.H1("Hello, World!")
```

Run: add `[tool.fastapi]` to `pyproject.toml`, then `air run` or `uv run air run`.

```toml
[tool.fastapi]
app = "main:app"
```

That's it. No settings file, no config module, no URL dispatcher files. Air reads everything from decorators and directory conventions (`static/`, `templates/`), so there's nothing to configure in a separate file. Customization happens through composition: add routers with `app.include_router()`, add middleware, pass parameters to `air.Air()`. Don't subclass `Air` or `AirRouter`.

## Routing

### @app.page: function name becomes the URL

```python
@app.page
def index():          # route: /
    return air.H1("Home")

@app.page
def about_us():       # route: /about-us (underscores become dashes)
    return air.H1("About")

@app.page
def contact():        # route: /contact
    return air.H1("Contact")
```

### Explicit paths with HTTP method decorators

```python
@app.get("/users/{user_id}")
def get_user(user_id: int) -> air.Div:
    return air.Div(air.H1(f"User {user_id}"))

@app.post("/submit")
async def submit(request: air.Request) -> air.Div:
    form_data = await request.form()
    return air.Div(air.P("Received"))
```

All standard HTTP methods: `app.get()`, `app.post()`, `app.put()`, `app.patch()`, `app.delete()`.

### async def vs def

Use `async def` when the handler calls `await` (e.g. `await request.form()`, `await request.json()`). Use plain `def` for everything else. Both work in all cases, but mixing `await` into a `def` route is a syntax error, and using `async def` without `await` wastes no resources but is unnecessary.

### Reverse URL resolution

Every decorated route gets a `.url()` method automatically:

```python
get_user.url(user_id=42)                           # "/users/42"
get_user.url(user_id=42, query_params={"tab": 1})  # "/users/42?tab=1"
index.url()                                         # "/"
```

Use in templates and tags: `air.A("Home", href=index.url())`.

### Routers for multi-file apps

```python
# views.py
import air

router = air.AirRouter()

@router.page
def dashboard():
    return air.H1("Dashboard")

# main.py
import air
from views import router

app = air.Air()
app.include_router(router)
```

## HTML Tags (Air Tags)

Air represents HTML as Python objects. Every standard HTML element is available as `air.TagName`.

```python
air.Div(
    air.H1("Welcome"),
    air.P("Hello ", air.Strong("world")),
    air.A("Click here", href="/about"),
    class_="container",
    id_="main",
)
```

Renders to: `<div class="container" id="main"><h1>Welcome</h1><p>Hello <strong>world</strong></p><a href="/about">Click here</a></div>`

### Air Tag Attribute rules

- Python reserved words use trailing underscore: `class_`, `for_`, `type_`, `id_`, `async_`
- Underscores become dashes: `hx_get` -> `hx-get`, `data_value` -> `data-value`
- Boolean `True` renders bare attribute: `disabled=True` -> `disabled`
- Boolean `False` omits the attribute entirely

### Common Air Tags

Container: `Div`, `Span`, `Section`, `Article`, `Aside`, `Nav`, `Main`, `Header`, `Footer`
Text: `H1`-`H6`, `P`, `A`, `Strong`, `Em`, `Small`, `Code`, `Pre`, `Blockquote`
Lists: `Ul`, `Ol`, `Li`, `Dl`, `Dt`, `Dd`
Tables: `Table`, `Thead`, `Tbody`, `Tfoot`, `Tr`, `Th`, `Td`
Forms: `Form`, `Input`, `Textarea`, `Select`, `Option`, `Button`, `Label`, `Fieldset`, `Legend`
Media: `Img`, `Video`, `Audio`, `Source`, `Picture`, `Canvas`
Document: `Html`, `Head`, `Body`, `Title`, `Meta`, `Link`, `Script`, `Style`
Self-closing: `Br`, `Hr`, `Img`, `Input`, `Meta`, `Link`

### Special Air Tags

- `air.Raw("html string")` - renders without escaping
- `air.Children(tag1, tag2)` / `air.Fragment(...)` - renders children without wrapper element
- `air.Comment("text")` - HTML comment

### Air Tag nesting and composition

```python
def nav_bar():
    return air.Nav(
        air.A("Home", href="/"),
        air.A("About", href="/about"),
    )

@app.page
def index():
    return air.Html(
        air.Head(air.Title("My Site")),
        air.Body(nav_bar(), air.Main(air.H1("Welcome"))),
    )
```

## Air Tag Layouts

Quick prototyping layouts that auto-sort children into `<head>` and `<body>`:

```python
@app.page
async def index(request: air.Request) -> air.Html | air.Children:
    return air.layouts.mvpcss(
        air.Title("Home"),                    # goes to <head>
        air.H1("Welcome to my site"),         # goes to <body>
        air.P("Built with Air"),              # goes to <body>
        is_htmx=request.htmx.is_hx_request,  # fragment if HTMX request
    )
```

Available: `air.layouts.mvpcss()` (MVP.css), `air.layouts.picocss()` (Pico CSS). Both include HTMX automatically.

When `is_htmx=True`, returns `Children` (fragment) instead of full `Html` document.

## Static Files

Zero config. Put files in `static/` and reference them with plain HTML paths. Unlike Django, there's no `{% load static %}` or template tag system for static files. Air handles path rewriting at the ASGI layer, so templates and Air tags both use the same plain `/static/` paths:

```python
air.Link(rel="stylesheet", href="/static/css/main.css")
air.Script(src="/static/js/app.js")
air.Img(src="/static/img/logo.png")
```

Air auto-detects and mounts `static/` at startup. Every static file gets a content hash appended to its URL (e.g. `/static/css/main.css` becomes `/static/css/main.abc123.css` in the served HTML), and the hashed URLs are served with immutable cache headers. Air rewrites `/static/` paths in HTML responses automatically, so you always write plain paths in your code and templates.

## Jinja Templates

`app.jinja` is available on every `air.Air()` instance automatically, pointing at `templates/`. No setup needed.

```python
import air

app = air.Air()

@app.get("/")
def home(request: air.Request):
    return app.jinja(request, "home.html", title="Home")
```

Pass template variables as kwargs. You can also pass `context={"title": "Home"}` as a dict, but kwargs are cleaner for simple cases. Both work and get merged.

**Avoid `name` as a kwarg.** The `name` parameter is used internally for the template filename, so `app.jinja(request, "page.html", name="Alice")` raises `TypeError: got multiple values for argument 'name'`. Use a different variable name (e.g. `applicant_name`) or pass it via the context dict: `context={"name": "Alice"}`.

**Air tags belong in Python, not pasted into templates.** When you have an Air tag that generates HTML (like an SVG logo component), pass it as a template variable and render it with `|safe`. Don't render the tag to a string and paste the HTML into a `.html` file. The Air tag is reusable across pages, testable in Python, and parameterizable (e.g. changing a fill color is a kwarg, not a find-and-replace across templates). Pasting the rendered output throws all of that away for a one-time shortcut. For complex HTML that originates in templates rather than Python, use `{% include "partials/logo.html" %}`.

```python
# Python: pass the Air tag as a variable
app.jinja(request, "page.html", sidebar=air.Nav(air.A("Home", href="/")))
```

```html
{# Template: use |safe so Jinja renders the HTML instead of escaping it #}
{{ sidebar|safe }}
```

Use `as_string=True` to get a `SafeStr` for embedding Jinja output inside Air tags.

## Forms

### AirForm[MyModel]: type-safe forms from Pydantic models

```python
from airmodel import AirModel, AirField
from air import AirForm

class ContactModel(AirModel):
    name: str
    email: str = AirField(type="email", label="Email Address")
    message: str = AirField(widget="textarea")

class ContactForm(AirForm[ContactModel]):
    pass
```

`AirForm[MyModel]` gives `form.data` full type information after validation. Editors autocomplete field names and catch typos.

### Rendering a form

```python
@app.page
def contact():
    form = ContactForm()
    return air.Html(
        air.Body(
            air.H1("Contact Us"),
            air.Form(
                form.render(),
                air.Button("Send", type_="submit"),
                method="post",
                action="/contact",
            ),
        ),
    )
```

`form.render()` returns SafeHTML that embeds directly in Air Tags without `air.Raw()` wrapping. After validation failure, it preserves submitted values and shows errors inline. CSRF protection is automatic. For multi-worker production, set `AIRFORM_SECRET` env var so all workers share the same signing key.

### Validating submitted data

```python
@app.post("/contact")
async def submit_contact(request: air.Request):
    form = await ContactForm.from_request(request)

    if form.is_valid:
        return air.Html(air.Body(air.P(f"Thanks, {form.data.name}!")))

    return air.Html(
        air.Body(
            air.H1("Please fix errors"),
            air.Form(
                form.render(),
                air.Button("Send", type_="submit"),
                method="post",
                action="/contact",
            ),
        ),
    )
```

`from_request` calls `await request.form()` and validates in one step. Works with `Depends()`:

```python
async def handler(form: Annotated[ContactForm, Depends(ContactForm.from_request)]):
    ...
```

### Saving to database

Use `save_data()` to get a dict with save-excluded fields stripped:

```python
if form.is_valid:
    await ContactModel.create(**form.save_data())
```

### AirField options

`AirField` accepts database metadata (`primary_key`), form rendering hints (`type`, `label`, `widget`, `placeholder`, `help_text`, `autofocus`, `choices`), and all Pydantic Field params (`min_length`, `max_length`, `pattern`, `ge`, `le`, etc.).

For context-aware visibility, use `Annotated` with AirField metadata types:

```python
from typing import Annotated
from airfield import Hidden, ReadOnly

class Article(AirModel):
    title: str
    slug: Annotated[str, Hidden("form")]      # hidden in forms, visible elsewhere
    internal: Annotated[str, ReadOnly("form")] # read-only in forms
```

### Custom widget

Set `widget` as a class attribute on your form subclass:

```python
class ContactForm(AirForm[ContactModel]):
    widget = staticmethod(my_custom_widget_function)
```

The widget callable receives `(*, model, data=None, errors=None, excludes=None)` and returns an HTML string.

### Excludes

Hide fields from rendering, saving, or both:

```python
class ContactForm(AirForm[ContactModel]):
    excludes = (
        "internal_notes",              # hidden from display and save
        ("slug", "display"),           # not rendered, still in save_data()
        ("tracking_id", "save"),       # rendered, excluded from save_data()
    )
```

PrimaryKey fields are default display excludes. The user's tuple extends the defaults.

## HTMX

HTMX attributes on tags:

```python
air.Button(
    "Load More",
    hx_get="/items",
    hx_target="#content",
    hx_swap="innerHTML",
    id="more"
)
```

Every `air.Request` object has `.htmx` object with typed HTMX header access:

```python
@app.page
def index(request: air.Request):
    if request.htmx.is_hx_request: # boolean of whether or not HTMX object
        return air.Children(
            air.H1("HTMX fragment"),
            air.P(request.htmx.trigger),
        )
    return air.layouts.mvpcss(
        air.H1("Full page"),
        air.P(request.htmx.trigger),
    )
```

Properties: `request.htmx.is_hx_request`, `.boosted`, `.target`, `.trigger`, `.trigger_name`, `.current_url`, `.prompt`.

### Dependency injection alternative

```python
@app.page
def index(*, is_htmx: bool = air.is_htmx_request):
    if is_htmx:
        return air.Div("fragment")
    return air.layouts.mvpcss(air.Div("full page"))
```

## Server-Sent Events

```python
async def counter():
    for i in range(10):
        yield air.P(f"Count: {i}")
        await asyncio.sleep(1)

@app.get("/stream")
async def stream():
    return air.SSEResponse(counter())
```

Pair with HTMX SSE extension on the frontend.

## Redirects

```python
from fastapi import status

@app.post("/login")
async def login(request: air.Request):
    return air.RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
```

Default status is 307 (temporary redirect, preserves method).

## Startup Tasks

Don't use `@app.on_event("startup")`. It's deprecated in both FastAPI and Starlette and will be removed in Starlette 1.0. Use the `lifespan` context manager instead:

```python
from contextlib import asynccontextmanager

import air

@asynccontextmanager
async def lifespan(app):
    # Runs on startup: connect to DB, load config, warm caches
    print("Starting up")
    yield
    # Runs on shutdown: close connections, flush buffers
    print("Shutting down")

app = air.Air(lifespan=lifespan)
```

For simple one-shot initialization (loading a config file, setting up a global variable), module-level code works fine:

```python
import air

DATA = load_initial_data()  # runs once at import time

app = air.Air()
```

Use `lifespan` when you need async operations, cleanup on shutdown, or when the initialization depends on the app instance.

## Database (AirModel)

Zero config. Set `DATABASE_URL` in the environment, `uv add AirModel`, and Air auto-connects on startup. The pool is available as `app.db`. If `DATABASE_URL` is not set, `app.db` is `None` and no database is configured.

Air calls `create_tables()` automatically at startup. If you add a field to a model, the existing table is auto-migrated with `ALTER TABLE ADD COLUMN`.

```python
import air
from airmodel import AirModel, AirField

app = air.Air()  # reads DATABASE_URL, connects automatically

class UnicornSighting(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    location: str
    sparkle_rating: int
    confirmed: bool = AirField(default=False)

@app.post("/sightings")
async def create_sighting(request: air.Request):
    form_data = await request.form()
    sighting = await UnicornSighting.create(
        location=form_data["location"],
        sparkle_rating=int(form_data["sparkle_rating"]),
    )
    return air.P(f"Recorded sighting #{sighting.id}")

@app.page
async def sightings():
    all_sightings = await UnicornSighting.filter(confirmed=True, order_by="-sparkle_rating")
    return air.Ul(*[air.Li(s.location) for s in all_sightings])
```

Methods: `create`, `get`, `filter`, `all`, `count`, `save`, `delete`, `bulk_create`, `bulk_update`, `bulk_delete`. Django-style lookups: `field__gte=5`, `field__icontains="x"`, `field__isnull=True`. Transactions: `async with app.db.transaction():`. See [AirModel AGENTS.md](https://github.com/feldroy/AirModel/blob/main/AGENTS.md) for lookups, bulk ops, and transactions.

## Common Patterns

### Return JSON

```python
from air.responses import JSONResponse

@app.post("/api/data")
async def api_data(request: air.Request):
    body = await request.json()
    return JSONResponse({"status": "ok", "id": 42})
```

Air's default response class is HTML, so returning a bare dict won't auto-convert to JSON. Use `JSONResponse` explicitly.

### Return a bare status code

```python
from air.responses import Response

@app.post("/webhook")
async def webhook(request: air.Request):
    body = await request.json()
    # process webhook...
    return Response(status_code=200)
```

### Redirect after form submission

```python
from fastapi import status

@app.post("/submit")
async def submit(request: air.Request):
    form_data = await request.form()
    # process form...
    return air.RedirectResponse(url="/thanks", status_code=status.HTTP_303_SEE_OTHER)
```

Use 303 (See Other) after POST so the browser switches to GET for the redirect target.

## Responses

Return types from routes:
- Air tags (`air.H1(...)`, `air.Div(...)`) - automatically rendered as HTML
- Strings - rendered as HTML
- `air.RedirectResponse` - HTTP redirect
- `air.SSEResponse` - server-sent events
- `JSONResponse`, `Response`, `PlainTextResponse` - import from `air.responses`
- Any Starlette `Response` subclass

HTML is the default. No wrapping in `HTMLResponse` needed.

## Testing

Starlette's `TestClient` requires `httpx`. Add it as a test dependency:

```toml
[dependency-groups]
test = ["httpx>=0.28.1", "pytest>=9.0.2"]
```

```python
from starlette.testclient import TestClient

import air

app = air.Air()

@app.page
def index():
    return air.H1("Hello")

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Hello</h1>" in response.text
```

Each test creates its own `app` and `TestClient`. No shared fixtures needed. Sync tests work for async endpoints.

## Project Structure

A typical Air app:

```
myproject/
  main.py              # app = air.Air(), routes
  mockups/             # original HTML mockups (reference only)
    landing.html
  static/
    css/main.css
    js/app.js
    img/logo.png
  templates/           # Jinja templates (auto-detected by app.jinja)
    base.html
    home.html
  pyproject.toml       # [tool.fastapi] app = "main:app"
```

A single `main.py` works because Air discovers routes from decorators, not by scanning a package tree. No `__init__.py` needed unless your app grows large enough to split across modules (see Routers). Compare to Django's 12+ files for the same functionality.

## Dependencies

```toml
[project]
dependencies = ["air>=0.47.0"]
```

Air brings FastAPI, Starlette, Pydantic, Jinja2, uvicorn, and HTMX. You don't need to install them separately. The `>=0.47.0` pin ensures Jinja template support (`app.jinja`) is available. If a newer version of Air exists, use it here.

## Deploying to Railway

Air is open source and runs on Railway. Sign up through [our link](https://railway.com?referralCode=5EX8pI) to get $20 in free credits. The referral helps cover Air's own hosting costs, so every signup directly supports the project.

Two files are all you need. Add `hypercorn` to your dependencies:

```toml
[project]
dependencies = ["air>=0.47.0", "hypercorn"]
```

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "RAILPACK"
  },
  "deploy": {
    "startCommand": "uv run hypercorn main:app --bind \"[::]:$PORT\""
  }
}
```

Railway detects `uv.lock` and installs dependencies with uv. The `$PORT` variable is injected at runtime. For the full Railway CLI workflow (init, deploy, domains, custom domains), use the `/railway-deploy` skill.

## Friction Notes

### Local editable installs of Air sub-packages (2026-03-19)

When developing against unreleased versions of AirField, AirForm, or AirModel in a downstream app, `[tool.uv.sources]` path overrides only take effect for **direct** dependencies. Packages that are only transitive (e.g. AirModel pulled in through Air) must be added to `[project.dependencies]` before the source override works. Without this, `uv sync` silently installs the PyPI version instead of the local one.
