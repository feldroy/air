import air
from fastapi import HTTPException
from pathlib import Path
from air_markdown import TailwindTypographyMarkdown as Markdown
import importlib

renderer = air.JinjaRenderer('templates')

app = air.Air()
                

def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception('First arg of layout needs to be an air.Request')
    head_tags = air.layouts.filter_head_tags(content)
    body_tags = air.layouts.filter_body_tags(content)
    return renderer(request, 'page.html',
                    head_tags=air.Children(*head_tags),
                    body_tags=air.Children(*body_tags)
    )


import json
import random


def sorted_random_list():
    return [0] + sorted(random.sample(range(1, 9), 4)) + [10]

def generate_data():
    return json.dumps(
        {
            "data": [
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )

@app.page
def index(request: air.Request):
    data = generate_data()
    return layout(
        request,
        air.Title('Air: The New FastAPI-Powered Python Web Framework (2025)'),
        air.Script(src="https://cdn.plot.ly/plotly-3.0.1.min.js"),
        Markdown("""
# Why use Air?

- **Powered by FastAPI** - Designed to work with FastAPI so you can server your API and web pages from one app
- **Fast to code** - Tons of intuitive shortcuts and optimizations designed to expedite coding HTML with FastAPI
- **Air Tags** - Easy to write and performant HTML content generation using Python classes to render HTML
- **Jinja Friendly** - No need to write `response_class=HtmlResponse` and `templates.TemplateResponse` for every HTML view
- **Mix Jinja and Air Tags** - Jinja and Air Tags both are first class citizens. Use either or both in the same view!
- **HTMX friendly** - We love HTMX and provide utilities to use it with Air
- **HTML form validation powered by pydantic** - We love using pydantic to validate incoming data. Air Forms provide two ways to use pydantic with HTML forms (dependency injection or from within views)
- **Easy to learn yet well documented** - Hopefully Air is so intuitive and well-typed you'll barely need to use the documentation. In case you do need to look something up we're taking our experience writing technical books and using it to make documentation worth boasting about

**Documentation**: <a href="https://feldroy.github.io/air/" target="_blank">https://feldroy.github.io/air/</a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank">https://github.com/feldroy/air</a>


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
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```
"""),
        Markdown("# Air loves charts!"),
        air.Div(id="randomChart"),
        air.Children( 
            # Call the Plotly library to plot the library
            air.Script( 
                f"var data = {data}; Plotly.newPlot('randomChart', data);",
                # Used to help HTMX know where to replace data
                id="dataSource",
                # Trigger HTMX to call new data every 2 seconds
                hx_trigger="every 2s",
                # Use HTMX to fetch new info from the /data route
                hx_get="/data",
                # When the data is fetched, replace the whole tag
                hx_swap='outerHTML'
            )
        ),
        
    )

@app.page
def data():
    data = generate_data()
    # This replaces the script in the web page with new data, and triggers
    # an animation of the transition
    return air.Script(
        f"var data = {data}; Plotly.animate('randomChart', data);",
        id="dataSource",
        hx_trigger="every 2s",
        hx_get="/data",
        hx_swap='outerHTML'
    )

@app.get('/{slug:path}')
def airpage(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(
            request, Markdown(text)
        )
    path = Path(f"pages/{slug}.py")
    if path.exists():
        module_name = f'pages.{slug.replace('/', '.')}'     
        mod = importlib.import_module(module_name)
        return layout(
            request, mod.render(request)
        )
    raise HTTPException(status_code=404)

    

