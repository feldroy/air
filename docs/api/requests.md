# Requests

`air.requests.Request` is an alias for [`starlette.requests.Request`](https://www.starlette.io/requests/), giving Air users a consistent import path.

While it behaves identically to Starlette’s implementation, it’s documented here for discoverability and ease of use.

---

## Usage

```python
import air
from air.requests import Request

app = air.Air()

@app.page
def request_info(request: Request):
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
from air.responses import JSONResponse

app = air.Air()

@app.get("/search")
async def search(request: Request):
    query = request.query_params.get("q", "none")
    return JSONResponse({"query": query})
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
from air.requests import Request
from air.responses import JSONResponse

app = air.Air()

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    return JSONResponse({"username": form.get("username")})
```
