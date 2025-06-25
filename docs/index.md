# Air

> A FastAPI-powered breath of fresh air for Python web development.

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

## Basic usage

```python
# main.py
from fastapi import FastAPI
from air.responses import TagResponse
import air

app = FastAPI()


@app.get("/")
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

Call with `fastapi` CLI:

```sh
fastapi dev
```

## Generate HTML and API

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