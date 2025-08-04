# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app.

Let's start by combining Air and FastAPI. With just a few lines of code, you can serve a homepage and an API side by side:

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

@app.get("/")
def landing_page():
    return air.layouts.mvpcss(
        air.Head(air.Title("My Awesome Startup")),
        air.Body(
            air.H1("My Awesome Startup"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )

@api.get("/")
def api_root():
    return {"message": "My Awesome Startup is powered by FastAPI"}

# Bring it all together: mount your API under /api
app.mount("/api", api)
```

---

## Prefer Jinja2 Templates?

If you love working with Jinja2, Air makes it effortless to use your favorite templates. Here’s how you can render a Jinja2 template for your homepage, while still serving your API from the same app:

First, create your template (for example, `home.html`):

```html
<!doctype html>
<html>
    <head>
        <title>My Awesome Startup</title>
    </head>
    <body>
        <h1>My Awesome Startup</h1>
        <p>
            <a target="_blank" href="/api/docs">API Docs</a>
        </p>
    </body>
</html>
```

Then, use Air’s JinjaRenderer to serve it:

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

# JinjaRenderer makes using Jinja templates a breeze
jinja = air.JinjaRenderer(directory="templates")

@app.get("/")
def index(request: Request):
    return jinja(request, name="home.html")

@api.get("/")
def api_root():
    return {"message": "My Awesome Startup is powered by FastAPI"}

# Mount your API just like before
app.mount("/api", api)
```

---

You can mix and match Air Tags or Jinja2 to suit your style. A common workflow is to use AI to generate a static HTML template, then convert it to Jinja2, and gradually replace pieces with Air Tags as they become more dynamic.

The goal is to help you build apps that are both delightful and powerful—with as little friction as possible. If you have questions or want to explore more, check out the API docs or dive into the Concepts section.
