# Quickstart

The TL;DR for getting started with Air.

## Installation

To start a new Air project, create a directory and set up your environment:

```sh
mkdir helloair
cd helloair
uv venv
source .venv/bin/activate
uv add air
uv add fastapi[standard]
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
    return air.layouts.mvpcss(air.H1("Hello, Air!", style="color: blue;"))
```

Serve your app with:

```sh
fastapi dev
```
