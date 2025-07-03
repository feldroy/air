# Air

> A FastAPI-powered breath of fresh air in Python web development.



- Designed to work with FastAPI so you can have your API and web pages server from one app
- When it comes to HTML generation, Jinja2 and Air tags both are first class citizens 
- ⁠Shortcut Response class for jinja2 rendering
- Air tags, for quick HTML content generation using Python classes
- Built from the beginning with ⁠HTMX in mind
- ⁠Shortcut utility functions galore
- Static site generation
- ⁠Serious documentation powered by material-for-mkdocs
- Lots of tests

Planned features

- ⁠pydantic-powered html forms

---

**Documentation**: <a href="https://feldroy.github.io/air/" target="_blank">https://feldroy.github.io/air/</a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank">https://github.com/feldroy/air</a>

---

The key features are:

- Use your FastAPI skills to build web pages to go along with your API
- Air tags, for quick HTML content generation using Python classes
- ⁠Shortcut Response class for jinja2 rendering
- Jinja2 and Air tags both are first class citizens 
- Built from the beginning with ⁠HTMX in mind
- Documented
- Robust


## Installation

If you are a more advanced user who plans to contribute to Air (and we invite you to!), follow the install instructions in CONTRIBUTING.md instead of the following.

Otherwise, create a virtualenv and install the air package, like:

```sh
uv venv
source .venv/bin/activate
uv add air
uv add fastapi[standard]
```

## Example

Create a `main.py` with:

```python
import air

app = air.Air()


@app.get("/")
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

> [!NOTE]  
> This example uses Air Tags, which are Python classes that render as HTML. Air Tags are typed and documented, designed to work well with any code completion tool.

## Example using Jinja2

```python
from air import Jinja2Renderer

render = Jinja2Renderer(directory="templates")

@app.get("/test")
def test_endpoint(request: Request):
    return render(
        request,
        name="home.html",
        context={"title": "Test Page", "content": "Hello, World!"},
    )
```

## HTTP GET page shortcut decorator

For when you want to write pages real fast.

```python
@app.page
def dashboard():
    return air.H1("Hello, World")
```

Using the function's name, `@app.page` maps the `dashboard` view to the `/dashboard` URL. 


## Raw HTML Content

For cases where you need to render raw HTML from the tag engine:

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
html = air.Air()

@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@html.get("/")
async def index():
    return air.H1("Welcome to Air")

# Combine into one app
app.mount("/", html)
```

URLs to see the results:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api
- http://127.0.0.1:8000/docs
