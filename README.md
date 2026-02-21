<p align="center">
  <br>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/feldroy/air/main/img/air-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/feldroy/air/main/img/air.svg" />
    <img alt="Air" src="https://raw.githubusercontent.com/feldroy/air/main/img/air.svg" width="180" />
  </picture>
  <br>
  <br>
</p>

<p align="center">
  The first web framework designed for AI to write.<br>
  Built on FastAPI, Pydantic, and HTMX.
  <br>
  <br>
</p>

<p align="center">
  <a href="https://github.com/feldroy/air/actions/workflows/ci.yml?query=branch%3Amain+event%3Apush"><img src="https://img.shields.io/github/actions/workflow/status/feldroy/air/ci.yml?branch=main&logo=githubactions&label=CI" alt="CI - main" /></a>
  <a href="https://github.com/feldroy/air/blob/main/LICENSE"><img src="https://img.shields.io/github/license/feldroy/air?logo=github&label=License" alt="GitHub License" /></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/air"><img src="https://img.shields.io/pypi/v/air?logo=pypi&label=Pypi&logoColor=fff" alt="PyPI - Version" /></a>
  <a href="https://pypi.org/project/air"><img src="https://img.shields.io/pypi/pyversions/air?logo=python&logoColor=fff&label=Python" alt="Python Versions" /></a>
  <a href="https://pepy.tech/projects/air"><img src="https://static.pepy.tech/badge/air" alt="PyPI Total Downloads" /></a>
  <a href="https://pepy.tech/projects/air"><img src="https://static.pepy.tech/badge/air/month" alt="PyPI Monthly Downloads" /></a>
  <a href="https://pepy.tech/projects/air"><img src="https://static.pepy.tech/badge/air/week" alt="PyPI Weekly Downloads" /></a>
</p>

<p align="center">
  <img src="https://custom-icon-badges.demolab.com/badge/Windows%2011-%230079d5?logo=windows11&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/MacOS-000000?logo=apple&logoColor=white&color=2e2e2e" alt="macOS" />
  <img src="https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white&color=orange" alt="Ubuntu" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/commit-activity/t/feldroy/air?logo=github&label=Commits" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/commits-since/feldroy/air/latest?logo=github" alt="GitHub commits since latest release" />
  <a href="https://github.com/feldroy/air/commit/main"><img src="https://img.shields.io/github/last-commit/feldroy/air?logo=github&label=Last%20Commit" alt="GitHub last commit" /></a>
  <a href="https://github.com/feldroy/air/releases/latest"><img src="https://img.shields.io/github/release-date/feldroy/air?logo=github&label=Release%20Date" alt="GitHub Release Date" /></a>
</p>

<p align="center">
  <a href="https://github.com/feldroy/air/graphs/contributors"><img src="https://img.shields.io/github/contributors/feldroy/air?logo=github&label=Contributors" alt="GitHub contributors" /></a>
  <a href="https://discord.gg/znf8vPsz47"><img src="https://img.shields.io/discord/1388403469505007696?logo=discord&label=Discord" alt="Discord" /></a>
  <a href="https://x.com/AirWebFramework"><img src="https://img.shields.io/badge/Air%20💨-%23000000.svg?logo=X&logoColor=white" alt="X" /></a>
  <a href="https://bsky.app/profile/airwebframework.bsky.social"><img src="https://img.shields.io/badge/Air%20💨-0285FF?logo=bluesky&logoColor=fff" alt="Bluesky" /></a>
  <a href="https://feldroy.github.io/air"><img src="https://img.shields.io/badge/MkDocs-526CFE?logo=materialformkdocs&logoColor=fff" alt="MkDocs" /></a>
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://docs.pydantic.dev/latest"><img src="https://img.shields.io/badge/Pydantic-1B0613.svg?logo=pydantic&logoColor=E35AF3" alt="Pydantic" /></a>
  <a href="https://jinja.palletsprojects.com/en/latest"><img src="https://img.shields.io/badge/jinja-white.svg?&logo=Jinja&logoColor=black" alt="Jinja" /></a>
  <a href="https://docs.astral.sh"><img src="https://img.shields.io/badge/uv|ruff|ty-black.svg?logo=astral&logoColor=D1FF4F" alt="Astral" /></a>
</p>

---

> [!CAUTION]
> Air is currently in an alpha state. While breaking changes are becoming less common, nevertheless, anything and everything could change.

> [!IMPORTANT]
> If you have an idea for a new feature, discuss it with us by opening an issue before writing any code. Do understand that we are working to remove features from core, and for new features you will almost always create your own package that extends or uses Air instead of adding to this package. This is by design, as our vision is for the Air package ecosystem to be as much a "core" part of Air as the code in this minimalist base package.

## Why use Air?

- **Designed for AI to write** - No magic, no implicit behavior. Comprehensive types and docstrings mean AI agents and editors understand the API without external docs
- **Powered by FastAPI** - Designed to work with FastAPI so you can serve your API and web pages from one app
- **Fast to code** - Tons of intuitive shortcuts and optimizations designed to expedite coding HTML with FastAPI
- **Air Tags** - Easy to write and performant HTML content generation using Python classes to render HTML
- **Jinja Friendly** - No need to write `response_class=HtmlResponse` and `templates.TemplateResponse` for every HTML view
- **Mix Jinja and Air Tags** - Jinja and Air Tags both are first class citizens. Use either or both in the same view!
- **HTMX friendly** - We love HTMX and provide utilities to use it with Air
- **HTML form validation powered by pydantic** - We love using pydantic to validate incoming data. Air Forms provide two ways to use pydantic with HTML forms (dependency injection or from within views)
- **Easy to learn yet well documented** - Hopefully Air is so intuitive and well-typed you'll barely need to use the documentation. In case you do need to look something up we're taking our experience writing technical books and using it to make documentation worth boasting about

---

**Website**: <a href="https://airwebframework.org" target="_blank"><https://airwebframework.org></a>

**Documentation**: <a href="https://docs.airwebframework.org" target="_blank"><https://docs.airwebframework.org></a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank"><https://github.com/feldroy/air></a>

## Installation

Install Air with `uv`:

```sh
uv venv
source .venv/bin/activate
uv init
uv add air
```

### Install optional features (with `uv add`)

You can install each optional feature (extras) like this:

1. **Standard** — FastAPI’s recommended extras

   ```sh
   uv add "air[standard]"
   ```

## Built for AI-Assisted Development

Air's API is fully typed and comprehensively documented in-source. AI coding assistants can understand the framework by reading the installed package, without fetching external documentation.

For AI context, use [llms-full.txt](https://docs.airwebframework.org/llms-full.txt) (complete docs) or [llms.txt](https://docs.airwebframework.org/llms.txt) (index with links to individual sections).

Third-party context providers: [Code Wiki by Google](https://codewiki.google/github.com/feldroy/air), [DeepWiki by Devin](https://deepwiki.com/feldroy/air).

## Two Ways to Build

Air gives you two paths to HTML. Start with whichever fits your workflow.

### Start with HTML

Have your AI generate an HTML mockup, or write one yourself. Drop it in a template, wire it up with minimal Python:

`templates/index.html`:

```html
<!doctype html>
<html>
  <head>
    <title>My App</title>
  </head>
  <body>
    <h1>Hello, world!</h1>
  </body>
</html>
```

`main.py`:

```python
import air

app = air.Air()
jinja = air.JinjaRenderer(directory="templates")


@app.get("/")
def index(request: air.Request):
    return jinja(request, name="index.html")
```

### Start with Python

Write HTML as typed Python classes. Your editor autocompletes attributes, your type checker validates nesting:

`main.py`:

```python
import air

app = air.Air()


@app.get("/")
def index():
    return air.Html(air.H1("Hello, world!"))
```

### Run either one

```sh
air run
```

Open <http://127.0.0.1:8000> to see the result. Both paths produce the same thing: a working web page.

## Combining FastAPI and Air

Air is just a layer over FastAPI. So it is trivial to combine sophisticated HTML pages and a REST API into one app.

```python
from fastapi import FastAPI

import air

app = air.Air()
api = FastAPI()


@app.get("/")
def landing_page():
    return air.Html(
        air.Head(air.Title("Awesome SaaS")),
        air.Body(
            air.H1("Awesome SaaS"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )


@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}


# Combining the Air and FastAPI apps into one
app.mount("/api", api)
```

## Combining FastAPI and Air using Jinja2

Want to use Jinja2 instead of Air Tags? We've got you covered.

```python
from fastapi import FastAPI

import air
from air.requests import Request

app = air.Air()
api = FastAPI()

# Air's JinjaRenderer is a shortcut for using Jinja templates
jinja = air.JinjaRenderer(directory="templates")


@app.get("/")
def index(request: Request):
    return jinja(request, name="home.html")


@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}


# Combining the Air and FastAPI apps into one
app.mount("/api", api)
```

Don't forget the Jinja template!

```html
<!doctype html>
<html>
  <head>
    <title>Awesome SaaS</title>
  </head>
  <body>
    <h1>Awesome SaaS</h1>
    <p>
      <a target="_blank" href="/api/docs">API Docs</a>
    </p>
  </body>
</html>
```

> [!NOTE]
> Using Jinja with Air is easier than with FastAPI. That's because as much as we enjoy Air Tags, we also love Jinja!

## Sponsors

Maintenance of this project is made possible by all
the [contributors](https://github.com/feldroy/air/graphs/contributors)
and [sponsors](https://github.com/sponsors/feldroy).
If you would like to support this project and have your avatar or company logo appear below,
please [sponsor us](https://github.com/sponsors/feldroy). 💖💨

<!-- SPONSORS -->

<!-- SPONSORS -->

Consider this low-barrier form of contribution yourself.
Your [support](https://github.com/sponsors/feldroy) is much appreciated.

## Contributing

For guidance on setting up a development environment and how to make a contribution to Air,
see [Contributing to Air](https://github.com/feldroy/air/blob/main/CONTRIBUTING.md).

## Contributors

Thanks to all the contributors to the Air 💨 web framework!

<a href="https://github.com/feldroy/air/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=feldroy/air" />
</a>

## PyPI Stats

- [pypistats](https://pypistats.org/packages/air)
- [libraries.io](https://libraries.io/pypi/air)
- [deps.dev](https://deps.dev/pypi/air)
- [PePy](https://pepy.tech/projects/air)

## Star History

<a href="https://www.star-history.com/#feldroy/air&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=feldroy/air&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=feldroy/air&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=feldroy/air&type=date&legend=top-left" />
 </picture>
</a>
