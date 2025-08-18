# Cookbook

A handy Air-themed list of recipes for common web app tasks.

## A minimal Air App

Similar to 

```python
import air

app = air.Air()

@app.get("/")
async def index():
    return air.H1("Hello, Air!", style="color: blue;")
```

## Charting in Air

Air is great for building charts. Using [plotly](https://plotly.com/javascript/), here's a simple chart example.

```python
import air
import json

app = air.Air()


@app.get("/")
def index():
    title = "Air Chart Demo"
    data = json.dumps(
        {
            "data": [
                {"x": [0, 4, 5, 7, 8, 10], "y": [2, 9, 0, 4, 3, 6], "type": "scatter"},
                {"x": [0, 1, 2, 4, 8, 10], "y": [9, 2, 4, 3, 5, 0], "type": "scatter"},
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )
    return air.layouts.mvpcss(
        air.Script(src="https://cdn.plot.ly/plotly-3.0.1.min.js"),
        air.Title(title),
        air.H1(title),
        air.Article(
            air.P(
                "Made with ",
                air.A("Air", href="https://airdocs.fastapicloud.dev/"),
                " and ",
                air.A("Plotly", href="https://plotly.com/javascript/"),
            ),
            air.Div(id="chart"),
            air.Script(f"var data = {data}; Plotly.newPlot('chart', data);"),
        ),
    )
```

Air makes it possible to build charts that pull data from servers and animate the results. Here's an example being supplied with random numbers for the Air server.

```air-live
air.Children(
    air.Div(id="randomChart"),
    air.Script("""
        var data = {"data": [{"x": [0, 4, 5, 7, 8, 10], "y": [2, 9, 0, 4, 3, 6], "type": "scatter"}, {"x": [0, 1, 2, 4, 8, 10], "y": [9, 2, 4, 3, 5, 0], "type": "scatter"}], "title": "Fun charts with Plotly and Air", "description": "This is a demonstration of how to build a chart using Plotly and Air", "type": "scatter"};
        Plotly.newPlot('randomChart', data);""",
        # ID is used to help HTMX know where to replace data
        id="dataSource",
        # Trigger HTMX to call new data every 2 seconds
        hx_trigger="every 2s",
        # Use HTMX to fetch new info from the /data route
        hx_get="/data",
        # When the data is fetched, replace the whole tag
        hx_swap="outerHTML",
    )
)
```



## The app.page decorator

For simple HTTP GET requests, Air provides the handy @app.page shortcut. It converts the name of the function to a URL, where underscores are replaced with dashes and `index` is replaced with '/'.

```python
import air

app = air.Air()


@app.page 
def index():
    # Same as route app.get('/')
    return air.H1('Welcome to our site!')

@app.page
def dashboard():
    # Same as route app.get('/dashboard')
    return air.H1('Dashboard')

@app.page
def show_item():
    # same as app.get('/get-item')
    return air.H1('Showing an item')
```

## Form validation with Air Forms

Built on Pydantic's `BaseModel`, the `air.AirForm` class is used to validate data coming from HTML forms.

```python
from typing import Annotated

from fastapi import Depends, Request
from pydantic import BaseModel
import air

app = air.Air()


class CheeseModel(BaseModel):
    name: str
    age: int


class CheeseForm(air.AirForm):
    model = CheeseModel

@app.page
async def index():
    return air.layouts.mvpcss(
        air.H1("Cheese Form"),
        air.Form(
            air.Input(name="name", placeholder='name of cheese'),
            air.Input(name="age", type="number", placeholder='age'),
            air.Button("Submit", type="submit"),
            method="post",
            action="/cheese-info",
        ),
    )

@app.post("/cheese-info")
async def cheese_info(request: Request):
    cheese = await CheeseForm.from_request(request)
    if cheese.is_valid:
        return air.Html(air.H1(f'{cheese.data.name} age {cheese.data.age}'))
    return air.Html(air.H1(f"Errors {len(cheese.errors)}"))
```

## Form handling using dependency injection

It is possible to use dependency injection to manage form validation

NOTE: This functionality is currently in development and this feature currently does not work

```python
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
import air

app = air.Air()


class CheeseModel(BaseModel):
    name: str
    age: int


class CheeseForm(air.AirForm):
    model = CheeseModel


@app.page
async def cheese():
    return air.Html(
        air.H1("Cheese Form"),
        air.Form(
            air.Input(name="name"),
            air.Input(name="age", type="number"),
            air.Button("Submit", type="submit"),
            method="post",
            action="/cheese-info",
        ),
    )


@app.post("/cheese-info")
async def cheese_info(cheese: Annotated[CheeseForm, Depends(CheeseForm.validate)]):
    if cheese.is_valid:
        return air.Html(air.H1(cheese.data.name))
    return air.Html(air.H1(f"Errors {len(cheese.errors)}"))
```

## Using a Jinja template for layouts

If you love working with Jinja2, Air makes it effortless to use your favorite templates. Here’s how you can render a Jinja2 template for your homepage, while still serving your API from the same app:

First, create your template (for example, `home.html`):

```html
<!doctype html>
<html>
    <head>
        <title>My Awesome Startup</title>
    </head>
    <body>
        <h1>My Awesome Startup</h1>
        <p>
            <a target="_blank" href="/api/docs">API Docs</a>
        </p>
    </body>
</html>
```

Then, use Air’s JinjaRenderer to serve it:

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

# JinjaRenderer makes using Jinja templates a breeze
jinja = air.JinjaRenderer(directory="templates")

@app.get("/")
def index(request: Request):
    return jinja(request, name="home.html")

@api.get("/")
def api_root():
    return {"message": "My Awesome Startup is powered by FastAPI"}

# Mount your API just like before
app.mount("/api", api)
```

---

You can mix and match Air Tags or Jinja2 to suit your style. A common workflow is to use AI to generate a static HTML template, then convert it to Jinja2, and gradually replace pieces with Air Tags as they become more dynamic.

The goal is to help you build apps that are both delightful and powerful—with as little friction as possible. If you have questions or want to explore more, check out the API docs or dive into the Concepts section.

## Serving static files (CSS, JS, images, etc.)

You can serve static files like CSS, JavaScript, and images using Air's built-in static file serving capabilities. In this example, we’ll create a simple Air app that serves static files from a `static` directory, but the name of the directory can be anything (`public` is also common).

```python
import air

app = air.Air()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1("Welcome to My Site!"),
        air.Link(rel="stylesheet", href="/static/styles.css"),
        air.Script(src="/static/scripts.js"),
        air.Img(src="/static/images/logo.png", alt="Logo"),
    )
```


## Checklist

All the things that may go into this page:

- [ ] Mounting static files
- [ ] Mounting with a FastAPI app
- [ ] File uploads
- [ ] SSE
- [ ] Web sockets
- [ ] Charts with plotly
- [ ] Debug mode
- [ ] Routing
- [ ] Using ayouts
- [ ] Making your own layout
- [ ] Adding markdown
- [ ] Definining components (function-based tags, class-based tags)
- [ ] Custom exception handlers
- [ ] Cookies
- [ ] Sessions
- [ ] Authentication
- [ ] Redirects