<p align="center">
  <img src="https://raw.githubusercontent.com/feldroy/air/refs/heads/main/img/air-neon.svg" />
</p>

## Air 💨: The new web framework that breathes fresh air into Python web development. Built with FastAPI, Starlette, and Pydantic.

[![CI - main](https://img.shields.io/github/actions/workflow/status/feldroy/air/CI.yaml?branch=main&logo=githubactions&label=CI)](https://github.com/feldroy/air/actions/workflows/CI.yaml?query=branch%3Amain+event%3Apush)
[![CI - Latest Tag](https://img.shields.io/github/check-runs/feldroy/air/latest?logo=githubactions&label=CI%20Tag)](https://github.com/feldroy/air/actions/workflows/python-package.yml?query=tag%3Alatest+event%3Apush)
[![codecov](https://codecov.io/gh/feldroy/air/graph/badge.svg?token=928SXPA1SU)](https://codecov.io/gh/feldroy/air)
[![GitHub License](https://img.shields.io/github/license/feldroy/air?logo=github&label=License)](https://github.com/feldroy/air/blob/main/LICENSE)

[![PyPI - Version](https://img.shields.io/pypi/v/air?logo=pypi&label=Pypi&logoColor=fff)](https://pypi.org/project/air)
[![PyPI Total Downloads](https://static.pepy.tech/badge/air)](https://pepy.tech/projects/air)
[![PyPI Monthly Downloads](https://static.pepy.tech/badge/air/month)](https://pepy.tech/projects/air)
[![PyPI Weekly Downloads](https://static.pepy.tech/badge/air/week)](https://pepy.tech/projects/air)

![Running on](https://img.shields.io/badge/Running%20on:-magenta?labelColor=black&logo=hotwire&logoColor=yellow)
![Windows](https://custom-icon-badges.demolab.com/badge/Windows%2011-%230079d5?logo=windows11&logoColor=white)
![macOS](https://img.shields.io/badge/MacOS-000000?logo=apple&logoColor=white&color=2e2e2e)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white&color=orange)
[![Python Versions](https://img.shields.io/pypi/pyversions/air?logo=python&logoColor=fff&label=Python)](https://pypi.org/project/air)

![GitHub commit activity](https://img.shields.io/github/commit-activity/t/feldroy/air?logo=github&label=Commits)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/feldroy/air/latest?logo=github)
[![GitHub last commit](https://img.shields.io/github/last-commit/feldroy/air?logo=github&label=Last%20Commit)](https://github.com/feldroy/air/commit/main)
[![GitHub Release Date](https://img.shields.io/github/release-date/feldroy/air?logo=github&label=Release%20Date)](https://github.com/feldroy/air/releases/latest)

[![GitHub contributors](https://img.shields.io/github/contributors/feldroy/air?logo=github&label=Contributors)](https://github.com/feldroy/air/graphs/contributors)
[![Discord](https://img.shields.io/discord/1388403469505007696?logo=discord&label=Discord)](https://discord.gg/znf8vPsz47)
[![X](https://img.shields.io/badge/Air%20💨-%23000000.svg?logo=X&logoColor=white)](https://x.com/AirWebFramework)
[![Bluesky](https://img.shields.io/badge/Air%20💨-0285FF?logo=bluesky&logoColor=fff)](https://bsky.app/profile/airwebframework.bsky.social)
[![MkDocs](https://img.shields.io/badge/MkDocs-526CFE?logo=materialformkdocs&logoColor=fff)](https://feldroy.github.io/air)

![Frameworks](https://img.shields.io/badge/Frameworks:-magenta?labelColor=black&logo=framework&logoColor=yellow)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-1B0613.svg?logo=pydantic&logoColor=E35AF3)](https://docs.pydantic.dev/latest)
[![Jinja](https://img.shields.io/badge/jinja-white.svg?&logo=Jinja&logoColor=black)](https://jinja.palletsprojects.com/en/latest)
[![Astral](https://img.shields.io/badge/uv|ruff|ty-black.svg?logo=astral&logoColor=D1FF4F)](https://docs.astral.sh)

---

> [!CAUTION]
> Air is currently in an alpha state. While breaking changes are becoming less common, nevertheless, anything and everything could change.


> [!IMPORTANT]
> If you have an idea for a new feature, discuss it with us by opening an issue before writing any code. Do understand that we are working to remove features from core, and for new features you will almost always create your own package that extends or uses Air instead of adding to this package. This is by design, as our vision is for the Air package ecosystem to be as much a "core" part of Air as the code in this minimalist base package.

## Why use Air?

- **Powered by FastAPI** - Designed to work with FastAPI so you can serve your API and web pages from one app
- **Fast to code** - Tons of intuitive shortcuts and optimizations designed to expedite coding HTML with FastAPI
- **Air Tags** - Easy to write and performant HTML content generation using Python classes to render HTML
- **Jinja Friendly** - No need to write `response_class=HtmlResponse` and `templates.TemplateResponse` for every HTML view
- **Mix Jinja and Air Tags** - Jinja and Air Tags both are first class citizens. Use either or both in the same view!
- **HTMX friendly** - We love HTMX and provide utilities to use it with Air
- **HTML form validation powered by pydantic** - We love using pydantic to validate incoming data. Air Forms provide two ways to use pydantic with HTML forms (dependency injection or from within views)
- **Easy to learn yet well documented** - Hopefully Air is so intuitive and well-typed you'll barely need to use the documentation. In case you do need to look something up we're taking our experience writing technical books and using it to make documentation worth boasting about

---

**Documentation**: <a href="https://airdocs.fastapicloud.dev/" target="_blank">https://airdocs.fastapicloud.dev</a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank">https://github.com/feldroy/air</a>

## Installation

Install using `pip install -U air` or `conda install air -c conda-forge`.

For `uv` users, just create a virtualenv and install the air package, like:

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
2. **SQL** — SQLModel / SQLAlchemy support
   ```sh
   uv add "air[sqlmodel]"
   ```
3. **Auth** — OAuth clients via Authlib
   ```sh
   uv add "air[auth]"
   ```
4. **All** — everything above in one go
   ```sh
   uv add "air[all]"
   ```
> Tip: you can also combine extras in one command, for example:
> `uv add "air[sqlmodel,sql]"`

## A Simple Example

Create a `main.py` with:

```python
import air

app = air.Air()


@app.get("/")
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

Run the app with:

```sh
fastapi dev
```

If you have fastapi installed globally, you may see an error:
```sh
To use the fastapi command, please install "fastapi[standard]":

	pip install "fastapi[standard]"
```
In that case, run the app with:
```sh
uv run fastapi dev
```

> [!NOTE]
> This example uses Air Tags, which are Python classes that render as HTML. Air Tags are typed and documented, designed to work well with any code completion tool.
> You can also run this with `uv run uvicorn main:app --reload` if you prefer using Uvicorn directly.

Then open your browser to <http://127.0.0.1:8000> to see the result.

## Combining FastAPI and Air

Air is just a layer over FastAPI. So it is trivial to combine sophisticated HTML pages and a REST API into one app.

```python
import air
from fastapi import FastAPI

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
import air
from air.requests import Request
from fastapi import FastAPI

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

# Combining the Air and and FastAPI apps into one
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

Maintenance of this project is made possible by all the [contributors](https://github.com/feldroy/air/graphs/contributors) and [sponsors](https://github.com/sponsors/feldroy).
If you would like to support this project and have your avatar or company logo appear below, please [sponsor us](https://github.com/sponsors/feldroy). 💖💨

<!-- SPONSORS -->

<!-- SPONSORS -->

Consider this low-barrier form of contribution yourself.
Your [support](https://github.com/sponsors/feldroy) is much appreciated.

## Contributing

For guidance on setting up a development environment and how to make a contribution to Air, see [Contributing to Air](https://github.com/feldroy/air/blob/main/CONTRIBUTING.md).

## Contributors

Thanks to all the contributors to the Air 💨 web framework!

<a href="https://github.com/feldroy/air/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=feldroy/air" />
</a>

## PyPI Stats

- [pypistats](https://pypistats.org/packages/air)
- [libraries.io](https://libraries.io/pypi/air)
- [deps.dev](https://deps.dev/pypi/air)

## Star History

<a href="https://www.star-history.com/#feldroy/air&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=feldroy/air&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=feldroy/air&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=feldroy/air&type=date&legend=top-left" />
 </picture>
</a>
