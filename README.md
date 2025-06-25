# Air

> A FastAPI-powered breath of fresh air for Python web development.

Current Features 

- Designed to work with FastAPI so you can have your API and web pages server from one app
- When it comes to HTML generation, Jinja2 and Air tags are both first class citizens 
- ⁠Shortcut Response class for jinja2 rendering
- Air tags, for quick HTML content generation using Pythonc lasses
- Built from the beginning with ⁠HTMX in mind
- ⁠Shortcut utility functions galore
- Static site generation
- ⁠Serious documentation powered by material-for-mkdocs
- Lots of tests

Planned features

- ⁠pydantic-powered html forms


## Installation

If you are a more advanced user who plans to contribute to Air (and we invite you to!), follow the install instructions in CONTRIBUTING.md instead of the following.

Otherwise, create a virtualenv and install the air package, like:

```sh
uv venv
source .venv/bin/activate
uv add air
```

## Use Air with tags

```python
from fastapi import FastAPI
import air

app = FastAPI()


@app.get("/", response_class=TagResponse)
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

## Use Air with Jinja2 shortcut

```python
from air import Jinja2Renderer

render = Jinja2Renderer(directory="tests/templates")

@app.get("/test")
def test_endpoint(request: Request):
    return render(
        request,
        name="home.html",
        context={"title": "Test Page", "content": "Hello, World!"},
    )
```

## Generate HTML and API

```python
from fastapi import FastAPI
from air.responses import TagResponse
import air

app = FastAPI()


@app.get("/", response_class=TagResponse)
async def index():
    return air.Html(
        air.H1("Hello, world!", style="color: blue;"),
        air.A("Go to API docs", href="/docs"),
    )


@app.get("/api")
async def api_root():
    return {}
```

## Raw HTML Content

For cases where you need to render raw HTML:

```python
from air import RawHTML

# Render raw HTML content
raw_content = RawHTML('<strong>Bold text</strong> and <em>italic</em>')

# Note: RawHTML only accepts a single string argument
# For multiple elements, combine them first:
html_string = '<p>First</p><p>Second</p>'
raw = RawHTML(html_string)
```

## REST + HTML without HTML in the docs

For when you need FastAPI docs but without the web pages appearing in the docs:

```python
from fastapi import FastAPI
import air

# API app
app = FastAPI()
# HTML page app
html = FastAPI()

@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@html.get("/", response_class=air.TagResponse)
async def index():
    return air.H1("Welcome to Air")

# Combine into one app
app.mount("/", html)
```

URLs to see the results:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api
- http://127.0.0.1:8000/docs
