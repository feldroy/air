# Tutorial: Combining FastAPI and Air

Air is just a layer over FastAPI. So it is trivial to combine sophisticated HTML pages and a REST API into one app. 

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

@app.get("/")
def landing_page():
    return air.layouts.mvpcss(
        air.Head(air.Title("Awesome SaaS")),
        air.Body(
            air.H1("Awesome SaaS"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )

@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}

# Combining the Air and and FastAPI apps into one
app.mount("/api", api)
```
<br>

## Using Jinja2 with Air

Want to use Jinja2 instead of Air Tags? We've got you covered.

```python
import air
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
<!doctype html
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
