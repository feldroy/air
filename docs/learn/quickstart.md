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
uv add air
uv add "fastapi[standard]"
```

!!! note
    You can also do:

    ```sh
    pip install -U air "fastapi[standard]"
    ```

    or even 

    ```sh
    conda install air -c conda-forge
    conda install "fastapi[standard]" -c conda-forge
    ```


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

## Routing: Basics

Air wraps FastAPI so you can use the same decorator patterns for specifying URL:

```python
import air

app = air.Air()

@app.get("/")
def index():
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )

@app.get("/air-is-grounded")
def air_is_grounded():
    return air.layouts.mvpcss(
        air.H1("Air is Grounded"),
        air.P("Built on industry standard libraries including:"),
        air.Ul(
            air.Li('FastAPI'),
            air.Li('Starlette'),
            air.Li('Pydantic'),
            air.Li('Jinja'),
        )
    )

@app.post('/form-handler')
async def form_handler(request: air.Request): # (1)!
    ...
```

1. Form handling in Air requires `async` functions and usually an `air.Request` argument. We cover forms later on this page as well as in numerous places across the Air documentation.

## Routing: app.page decorator

To expedite `HTTP GET` pages we provide the `app.page` decorator, which can replace the `app.get()` decorator for views without arguments. `app.page` converts the name of the function to the route, converting underscores to dashes:

```python hl_lines="5-6 12-13"
import air

app = air.Air()

@app.page # Renders as '/'
def index(): # (1)!
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )

@app.page # Renders as '/air-is-grounded'
def air_is_grounded(): # (2)!
    return air.layouts.mvpcss(
        air.H1("Air is Grounded"),
        air.P("Built on industry standard libraries including:"),
        air.Ul(
            air.Li('FastAPI'),
            air.Li('Starlette'),
            air.Li('Pydantic'),
            air.Li('Jinja'),
        )
    )
```  

1. `app.page` used over functions named `index` are converted to the `/` route.
2. `app.page` used over functions are converted to a route based on their name, with underscores converted to dashes. 

## Want to learn more?

Check out these documentation sections:

- [Learn](/learn)
- [API Reference](/api)