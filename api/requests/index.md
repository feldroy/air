# Requests

`air.requests.Request` is an wrapper for [`starlette.requests.Request`](https://www.starlette.io/requests/), giving Air users a consistent import path. It adds an `htmx` object that includes a lot of quite useful utility methods.

______________________________________________________________________

## Usage

```
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

```
import air
from air.requests import Request

app = air.Air()

@app.get("/search")
async def search(request: Request):
    query = request.query_params.get("q", "none")
    return air.Pre(query)
```

### Reading JSON Body

```
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

```
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

```
import air

app = air.Air()

@app.page
def index(request: air.AirRequest):
    return air.layouts.mvpcss(
        air.H1(f'From HTMX?'),
        air.P(f"This request came from an HTMX element on a page: {request.htmx}")
    )
```

Tools for handling requests.

## AirRequest

Bases: `Request`

A wrapper around `starlette.requests.Request` that includes the `HtmxDetails` object.

Note

AirRequest is available in Air 0.36.0+

## HtmxDetails

```
HtmxDetails(headers, url)
```

Attached to every Request served by Air; provides helpers for HTMX-aware handling. Derived values are computed once in `__post_init__`.

### __bool__

```
__bool__()
```

`True` if the request was made with htmx, otherwise `False`. Detected by checking if the `HX-Request` header equals `true`.

This method allows you to change content for requests made with htmx:

Example:

```
import air
from random import randint

app = air.Air()


@app.page
def index(request: air.Request):

    if request.htmx:
        return air.H1(
            "Click me: ", randint(1, 100),
            id="number",
            hx_get="/",
            hx_swap="outerHTML"
        )
    return air.layouts.mvpcss(
        air.H1(
            "Click me: ", randint(1, 100),
            id="number",
            hx_get="/",
            hx_swap="outerHTML"
        )
    )
```

Source code in `src/air/requests.py`

```
def __bool__(self) -> bool:
    """`True` if the request was made with htmx, otherwise `False`. Detected by checking if the `HX-Request` header equals `true`.

    This method allows you to change content for requests made with htmx:

    Example:

        import air
        from random import randint

        app = air.Air()


        @app.page
        def index(request: air.Request):

            if request.htmx:
                return air.H1(
                    "Click me: ", randint(1, 100),
                    id="number",
                    hx_get="/",
                    hx_swap="outerHTML"
                )
            return air.layouts.mvpcss(
                air.H1(
                    "Click me: ", randint(1, 100),
                    id="number",
                    hx_get="/",
                    hx_swap="outerHTML"
                )
            )
    """

    return self.headers.get("HX-Request") == "true"
```

### boosted

```
boosted = field(init=False)
```

`True` if the request came from an element with the `hx-boost` attribute. Detected by checking if the `HX-Boosted` header equals `true`.

Example:

```
import air
from random import randint

app = air.Air()


@app.page
def index(request: air.Request):

    if request.htmx.boosted:
        # Do something here
```

### current_url

```
current_url = field(init=False)
```

The current URL in the browser that htmx made this request from, or `None` for non-htmx requests. Based on the `HX-Current-URL` header.

### current_url_abs_path

```
current_url_abs_path = field(init=False)
```

The absolute-path form of `current_url`, that is the URL without scheme or netloc, or None for non-htmx requests.

This value will also be `None` if the scheme and netloc do not match the request. This could happen if the request is cross-origin, or if Air is not configured correctly.

### history_restore_request

```
history_restore_request = field(init=False)
```

`True` if the request is for history restoration after a miss in the local history cache. Detected by checking if the `HX-History-Restore-Request` header equals `true`.

### prompt

```
prompt = field(init=False)
```

The user response to `hx-prompt` if it was used, or `None`.

### target

```
target = field(init=False)
```

The `id` of the target element if it exists, or `None`. Based on the `HX-Target` header.

### trigger

```
trigger = field(init=False)
```

The `id` of the triggered element if it exists, or `None`. Based on the `HX-Trigger` header.

### trigger_name

```
trigger_name = field(init=False)
```

The name of the triggered element if it exists, or `None`. Based on the `HX-Trigger-Name` header.
