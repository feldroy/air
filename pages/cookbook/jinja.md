# Jinja templates

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

You can mix and match Air Tags or Jinja2 to suit your style. A common workflow is to use AI to generate a static HTML template, then convert it to Jinja2, and gradually replace pieces with Air Tags as they become more dynamic.
