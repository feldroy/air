# Building Apps with Air

Air is a Python web framework built on FastAPI/Starlette. HTML-first, zero config. This file tells you everything you need to build a complete Air app from scratch.

## Working from HTML Mockups

When the user provides static HTML files as mockups, follow this workflow:

1. **Archive the originals.** Move the HTML files into `mockups/` so the raw design is preserved as a reference. Create the directory if it doesn't exist.

2. **Copy to templates/.** Copy each mockup from `mockups/` into `templates/`. This is where Air's Jinja renderer looks for templates. Create the directory if it doesn't exist.

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

That's it. No settings file, no config module, no URL dispatcher files.

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

### Attribute rules

- Python reserved words use trailing underscore: `class_`, `for_`, `type_`, `id_`, `async_`
- Underscores become dashes: `hx_get` -> `hx-get`, `data_value` -> `data-value`
- Boolean `True` renders bare attribute: `disabled=True` -> `disabled`
- Boolean `False` omits the attribute entirely

### Common tags

Container: `Div`, `Span`, `Section`, `Article`, `Aside`, `Nav`, `Main`, `Header`, `Footer`
Text: `H1`-`H6`, `P`, `A`, `Strong`, `Em`, `Small`, `Code`, `Pre`, `Blockquote`
Lists: `Ul`, `Ol`, `Li`, `Dl`, `Dt`, `Dd`
Tables: `Table`, `Thead`, `Tbody`, `Tfoot`, `Tr`, `Th`, `Td`
Forms: `Form`, `Input`, `Textarea`, `Select`, `Option`, `Button`, `Label`, `Fieldset`, `Legend`
Media: `Img`, `Video`, `Audio`, `Source`, `Picture`, `Canvas`
Document: `Html`, `Head`, `Body`, `Title`, `Meta`, `Link`, `Script`, `Style`
Self-closing: `Br`, `Hr`, `Img`, `Input`, `Meta`, `Link`

### Special tags

- `air.Raw("html string")` - renders without escaping
- `air.Children(tag1, tag2)` / `air.Fragment(...)` - renders children without wrapper element
- `air.Comment("text")` - HTML comment

### Nesting and composition

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

## Static Files

Zero config. Put files in `static/` and reference them with plain HTML paths:

```python
air.Link(rel="stylesheet", href="/static/css/main.css")
air.Script(src="/static/js/app.js")
air.Img(src="/static/img/logo.png")
```

Air auto-detects and mounts `static/` at startup with content-hash cache busting. No settings, no template tags, no configuration.

## Layouts

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

## Jinja Templates

`app.jinja` is available on every `air.Air()` instance automatically, pointing at `templates/`. No setup needed.

```python
import air

app = air.Air()

@app.get("/")
def home(request: air.Request):
    return app.jinja(request, "home.html", context={"title": "Home"})
```

Air tags work in Jinja context: `app.jinja(request, "page.html", sidebar=air.Nav(air.A("Home", href="/")))`.

Use `as_string=True` to get a `SafeStr` for embedding Jinja output inside Air tags.

## Forms

### Define model, get form for free

```python
class ContactModel(air.AirModel):
    name: str
    email: str = air.AirField(type="email", label="Email Address")
    message: str

@app.page
def contact():
    form = ContactModel.to_form()
    return air.Html(
        air.Body(
            air.H1("Contact Us"),
            air.Form(
                form.render(),
                air.Button("Send", type_="submit"),
                method="post",
                action=submit_contact.url(),
            ),
        ),
    )

@app.post("/contact")
async def submit_contact(request: air.Request):
    form = ContactModel.to_form()
    form_data = await request.form()

    if form.validate(form_data):
        return air.Html(air.Body(air.P(f"Thanks, {form.data.name}!")))

    return air.Html(
        air.Body(
            air.H1("Please fix errors"),
            air.Form(
                form.render(),  # re-renders with errors and preserved values
                air.Button("Send", type_="submit"),
                method="post",
                action=submit_contact.url(),
            ),
        ),
    )
```

`AirModel` extends Pydantic `BaseModel`. One class handles validation, form rendering, and error display.

`AirField` options: `type` (email, password, url, hidden), `label`, `autofocus`, plus all Pydantic `Field` params (`min_length`, `max_length`, `pattern`, etc.).

### Alternative: AirForm subclass

```python
class ContactForm(air.AirForm):
    model = ContactModel

form = ContactForm()
flight = await ContactForm.from_request(request)
```

`from_request` works with `Depends()`: `Annotated[ContactForm, Depends(ContactForm.from_request)]`.

## HTMX

Every request has `.htmx` with typed HTMX header access:

```python
@app.page
def index(request: air.Request):
    if request.htmx:
        return air.H1("HTMX fragment")
    return air.layouts.mvpcss(air.H1("Full page"))
```

Properties: `request.htmx.is_hx_request`, `.boosted`, `.target`, `.trigger`, `.trigger_name`, `.current_url`, `.prompt`.

HTMX attributes on tags:

```python
air.Button(
    "Load More",
    hx_get="/items",
    hx_target="#content",
    hx_swap="innerHTML",
)
```

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

## Responses

Return types from routes:
- Air tags (`air.H1(...)`, `air.Div(...)`) - automatically rendered as HTML
- Strings - rendered as HTML
- `air.RedirectResponse` - HTTP redirect
- `air.SSEResponse` - server-sent events
- Any Starlette `Response` subclass

HTML is the default. No wrapping in `HTMLResponse` needed.

## Testing

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

Compare to Django's 12+ files for the same functionality.

## Dependencies

```toml
[project]
dependencies = ["air"]
```

Air brings FastAPI, Starlette, Pydantic, Jinja2, uvicorn, and HTMX. You don't need to install them separately.

## What NOT to do

- Don't create a `settings.py` or config module. Air has no settings.
- Don't create separate URL dispatcher files. Routes are inline decorators.
- Don't use `{% load static %}` or template tags for static files. Use plain HTML paths.
- Don't subclass `Air` or `AirRouter`. They use composition, not inheritance.
- Don't use `HTMLResponse` to wrap tag output. Air tags render as HTML automatically.
- Don't create `__init__.py` files for your app package unless you need them. A single `main.py` works.
- Don't instantiate `JinjaRenderer` manually. Use `app.jinja` which is auto-created.
