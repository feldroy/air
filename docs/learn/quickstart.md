# Quickstart

The TL;DR for getting started with Air.

## Installation

To start a new Air project, create a directory and set up your environment:

```sh
mkdir helloair
cd helloair
uv venv
source .venv/bin/activate
uv init
uv add "air[standard]"
```

> [!TIP]
> You can also do `pip install -U air` or `conda install air -c conda-forge`, and similar for fastapi[standard], in any project directory.

## Hello, Air! Example

Create a `main.py` file in your new directory with:

```python
import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )
```

Serve your app with:

```sh
fastapi dev
```

Open your page by clicking this link: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

Here's a few interesting things about this page:

1. The page has an attractive layout and typography
2. The Python for this app is similar in design to how FastAPI code is written
3. If you typed the code out in an IDE with intellisense, you'll have seen every Air object includes useful instruction. Air is designed to be friendly to both humans and LLMs, hence every object is carefully typed and documented

## Want to see how to combine Air with FastAPI?

With just a few lines of code, you can serve a homepage and an API side by side:

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

## Want to learn more?

Want to see how Air combines with FastAPI? [Try out the tutorial!](tutorial.md)
 
