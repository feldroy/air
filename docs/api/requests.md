# Requests

`air.requests.Request` is an wrapper for [`starlette.requests.Request`](https://www.starlette.io/requests/), giving Air users a consistent import path. It adds an `htmx` object that includes a lot of quite useful utility methods.

---

## Usage

```python
import air
from air.requests import Request

app = air.Air()

@app.page
async def request_info(request: Request):
    return air.layouts.mvpcss(
        air.H1("Request Info"),
        air.P(f"Method: {request.method}"),
        air.P(f"URL: {request.url}"),
        air.P(f"Headers: {dict(request.headers)}"),
        air.P(f"Query Params: {dict(request.query_params)}"),
    )
```

## Practical Recipes
Here are smaller, focused examples for specific use cases:

### Accessing Query Parameters
```python
import air
from air.requests import Request

app = air.Air()

@app.get("/search")
async def search(request: Request):
    query = request.query_params.get("q", "none")
    return air.Pre(query)
```

### Reading JSON Body
```python
import air
from air.requests import Request
from air.responses import JSONResponse

app = air.Air()

@app.post("/items")
async def create_item(request: Request):
    data = await request.json()
    return JSONResponse({"item": data})
```

### Reading Form Data
```python
import air
from air.requests import AirRequest
from air.responses import JSONResponse

app = air.Air()

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    return air.layouts.mvpcss(
        air.Section(
            air.Aside({"username": form.get("username")})
        )
    )
```


### Accessing the HTMX object

This requires use of the `air.requests.AirRequest` object.

```python
import air

app = air.Air()

@app.page
def index(request: air.AirRequest):
    return air.layouts.mvpcss(
        air.H1(f'From HTMX?'),
        air.P(f"This request came from an HTMX element on a page: {request.htmx}")
    )
```


::: air.requests
    options:
      group_by_category: false
      members:
        - AirRequest
        - HtmxDetails      
