
## HTTP GET page shortcut decorator

For when you want to write pages real fast.

```python
@app.page
def dashboard():
    return air.H1("Hello, World")
```

Using the function's name, `@app.page` maps the `dashboard` view to the `/dashboard` URL


## Raw HTML Content

For cases where you need to render raw HTML from the tag engine:

```python
from air import RawHTML

# Render raw HTML content
raw_content = RawHTML('<strong>Bold text</strong> and <em>italic</em>')

# Note: RawHTML only accepts a single string argument
# For multiple elements, combine them first:
html_string = '<p>First</p><p>Second</p>'
raw = RawHTML(html_string)
```

## REST + HTML without HTML in the docs

For when you need FastAPI docs but without the web pages appearing in the docs:

```python
from fastapi import FastAPI
import air

# API app
app = FastAPI()
# HTML page app
html = air.Air()

@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@html.get("/")
async def index():
    return air.H1("Welcome to Air")

# Combine into one app
app.mount("/", html)
```

URLs to see the results:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api
- http://127.0.0.1:8000/docs
