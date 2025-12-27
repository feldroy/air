# Responses

Air uses custom response classes to improve the developer experience.

## TagResponse

```
TagResponse = AirResponse
```

Alias for the `AirResponse` Response class; use it if it improves clarity.

## AirResponse

Bases: `HTMLResponse`

Response class to handle air.tags.Tags or HTML (from Jinja2).

### render

```
render(tag)
```

Render Tag elements to bytes of HTML.

Returns:

| Type    | Description  |
| ------- | ------------ |
| \`bytes | memoryview\` |

Source code in `src/air/responses.py`

```
@override
def render(self, tag: BaseTag | str) -> bytes | memoryview:  # ty: ignore[invalid-method-override]
    """Render Tag elements to bytes of HTML.

    Returns:
        Rendered HTML as bytes or memoryview.
    """
    return super().render(str(tag))
```

## RedirectResponse

```
RedirectResponse(
    url,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    headers=None,
    background=None,
)
```

Bases: `RedirectResponse`

Response class for HTTP redirects.

Use `air.RedirectResponse` to redirect users to a different URL.

Example

```
import air

app = air.Air()


@app.get("/old-page")
def old_page():
    # Permanent redirect (301) - browsers cache this
    return air.RedirectResponse(url="/new-page", status_code=301)


@app.page
def legacy():
    # Using @app.page works too - redirects from /legacy
    return air.RedirectResponse(url="/", status_code=301)
```

Parameters:

| Name          | Type                | Description                                                                                                                                                                                                                                                                                              | Default                                                     |
| ------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `url`         | \`str               | URL\`                                                                                                                                                                                                                                                                                                    | The target URL to redirect to.                              |
| `status_code` | `int`               | HTTP status code for the redirect. Defaults to 307 (Temporary Redirect). Common values: - 301: Permanent redirect (SEO-friendly, browsers cache) - 302: Temporary redirect (traditional) - 307: Temporary redirect (preserves HTTP method, default) - 303: See Other (use after POST to redirect to GET) | `HTTP_307_TEMPORARY_REDIRECT`                               |
| `headers`     | \`Mapping[str, str] | None\`                                                                                                                                                                                                                                                                                                   | Optional additional headers to include in the response.     |
| `background`  | \`BackgroundTask    | None\`                                                                                                                                                                                                                                                                                                   | Optional background task to run after the response is sent. |

Source code in `src/air/responses.py`

```
def __init__(
    self,
    url: str | URL,
    status_code: int = status.HTTP_307_TEMPORARY_REDIRECT,
    headers: Mapping[str, str] | None = None,
    background: BackgroundTask | None = None,
) -> None:
    super().__init__(url=url, status_code=status_code, headers=headers, background=background)
```

## SSEResponse

Bases: `StreamingResponse`

Response class for Server Sent Events

Example:

```
# For tags
import random
from asyncio import sleep

import air

app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(
        air.Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
        air.Title("Server Sent Event Demo"),
        air.H1("Server Sent Event Demo"),
        air.P("Lottery number generator"),
        air.Section(
            hx_ext="sse",
            sse_connect="/lottery-numbers",
            hx_swap="beforeend show:bottom",
            sse_swap="message",
        ),
    )

async def lottery_generator():
    while True:
        lottery_numbers = ", ".join(
            [str(random.randint(1, 40)) for x in range(6)]
        )
        # Tags work seamlessly
        yield air.Aside(lottery_numbers)
        # As do strings. Non-strings are cast to strings via the
        # str built-in
        yield "Hello, world"
        await sleep(1)


@app.get("/lottery-numbers")
async def get():
    return air.SSEResponse(lottery_generator())
```
