import air
from air_markdown import TailwindTypographyMarkdown as Markdown

def render(request: air.Request):
    return air.Children(
        air.Title("Learn > Quickstart"),
        Markdown("""# Quickstart

Here are the tutorials for learning Air. While not necessary, it helps if you have experience with [FastAPI](https://fastapi.tiangolo.com/).

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
    return air.layouts.mvpcss(air.H1("Hello, world!", style="color: blue;"))
```

Serve with this command-line action:

```python
fastapi dev
```
<br>
"""),
    )
