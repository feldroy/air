# Air

> The new web framework that breathes fresh air into Python web development. Built with FastAPI, Starlette, and Pydantic.

<p align="center">
<a href="https://github.com/feldroy/air/actions?query=workflow%3Apython-package+event%3Apush+branch%main" target="_blank">
    <img src="https://github.com/feldroy/air/actions/workflows/python-package.yml/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://pypi.org/project/air" target="_blank">
    <img src="https://img.shields.io/pypi/v/air?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/air" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/air.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>


> [!CAUTION]
> Air is currently in an alpha state. While breaking changes are becoming less common, nevertheless, anything and everything could change.
>
> We ask that you hold off on contributing mostly for now, to give us space to focus on
> getting our ideas down. If you happen to fix a bug, though, little PRs for that are welcome.

## Why use Air?


- **Powered by FastAPI** - Designed to work with FastAPI so you can server your API and web pages from one app
- **Fast to code** - Tons of intuitive shortcuts and optimizations designed to expedite coding HTML with FastAPI
- **Air Tags** - Easy to write and performant HTML content generation using Python classes to render HTML
- **Jinja Friendly** - No need to write `response_class=HtmlResponse` and `templates.TemplateResponse` for every HTML view
- **Mix Jinja and Air Tags** - Jinja and Air Tags both are first class citizens. Use either or both in the same view!
- **HTMX friendly** - We love HTMX and provide utilities to use it with Air
- **HTML form validation powered by pydantic** - We love using pydantic to validate incoming data. Air Forms provide two ways to use pydantic with HTML forms (dependency injection or from within views)
- **Easy to learn yet well documented** - Hopefully Air is so intuitive and well-typed you'll barely need to use the documentation. In case you do need to look something up we're taking our experience writing technical books and using it to make documentation worth boasting about

---

**Documentation**: <a href="https://feldroy.github.io/air/" target="_blank">https://feldroy.github.io/air/</a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank">https://github.com/feldroy/air</a>


## Installation

Install using `pip install -U air` or `conda install air -c conda-forge`.

For `uv` users, just create a virtualenv and install the air package, like:

```sh
uv venv
source .venv/bin/activate
uv add air
uv add fastapi[standard]
```

## A Simple Example

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

jinja = Jinja2Renderer(directory="templates")

@app.get("/test")
def index(request: Request):
    return jinja(
        request,
        name="home.html",
        context={"title": "Hello World Page"}, content="Hello, World",
    )
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to Air, see [Contributing to Air](https://github.com/feldroy/air/blob/main/CONTRIBUTING.md).