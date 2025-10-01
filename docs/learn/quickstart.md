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

```python title="main.py"
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

## Routing

Routing is how users on paths are directed to the correct 'view' function that handles their request.

### Basics

Air wraps FastAPI so you can use the same decorator patterns for specifying URLs:

```python  hl_lines="5 12 25"
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

### app.page decorator

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

## Air Tags

[Air Tags](learn/air_tags) are one of Air's two ways to generate HTML output. They are useful for keeping file size down, general HTML delivery, and especially with fragment responses via HTMX.


### JavaScript Files

Using Air Tags to call external JavaScript files:

```python hl_lines="7"
import air

app = air.Air()

@app.page
def index():
    return air.Script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.7/dist/htmx.min.js")
```

### Inline Scripts

When you need to use JavaScript inline in Air Tags:


```python hl_lines="7"
import air

app = air.Air()

@app.page
def index():
    return air.Script("alert('The Last Airbender is an awesome series.')")
```

### CSS Files

Here's how to use Air Tags to call external CSS files:

```python hl_lines="9"
import air

app = air.Air()

@app.page
def index():
    return air.Html(
        air.Head(
            air.Link(rel="stylesheet", href="https://unpkg.com/mvp.css"),
        ),
        air.Body(
            air.Main(
                air.H1("Air Web Framework"),
                air.P("The web framework for Air Nomads.")
            )
        )
    )
```

### Inline CSS Styles

Inline CSS styles via Air are a good way to control design elements at runtime.

```python hl_lines="9"
import air

app = air.Air()

@app.page
def index():
    return air.Html(
        air.Head(
            air.Style("h1 {color: red;}"),
        ),
        air.Body(
            air.H1("Air Web Framework"),
            air.P("The web framework for Air Nomads.")
        )
    )
```

## Want to learn more?

Check out these documentation sections:

- [Learn](/learn)
- [API Reference](/api)