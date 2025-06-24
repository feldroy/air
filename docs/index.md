# Air

> A breath of fresh air in python web development. Built on top of FastAPI and pydantic.

Current Features 

- Designed to work with FastAPI so you can have your API and web pages server from one app
- HTML generation from jinja2 or Python classes. Pick one or both!
- ⁠Shortcut Response  class and fastapi tags
- Built from the beginning with ⁠HTMX in mind
- ⁠Shortcut utility functions galore
- Static site generation
- ⁠Serious documentation powered by material-for-mkdocs
- Lots of tests

Planned features

- ⁠pydantic-powered html forms
- ⁠Shortcut Response class for jinja2


## Installation

```sh
pip install air
```

## Use with fastapi tags

```python
from fastapi import FastAPI
from air.responses import TagResponse
from air import tags as tg

app = FastAPI()


@app.get("/", response_class=TagResponse)
async def index():
    return tg.Html(tg.H1("Hello, world!", style="color: blue;"))
```

## Generate HTML and API

```python
from fastapi import FastAPI
from air.responses import TagResponse
from air import tags as tg

app = FastAPI()


@app.get("/", response_class=TagResponse)
async def index():
    return tg.Html(
        tg.H1("Hello, world!", style="color: blue;"),
        tg.A("Go to API docs", href="/docs"),
    )


@app.get("/api")
async def api_root():
    return {}
```