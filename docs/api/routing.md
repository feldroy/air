Routing

If you need to knit several Python modules with their own Air views into one, that's where Routing is used. They allow the near seamless combination of multiple Air apps into one. Larger sites are often built from multiple routers.

Let's imagine we have an e-commerce store with a shopping cart app. Use instantiate a `router` object using `air.AirRouter()` just as we would with `air.App()`:

```python
# cart.py
import air

router = air.AirRouter()


@router.page
def cart():
    return air.H1("I am a shopping cart")
```

Then in our main page we can load that and tie it into our main `app`.

```python
import air
from cart import router as cart_router

app = air.Air()
app.include_router(cart_router)


@app.page
def index():
    return air.H1("Home page")
```

Note that the router allows sharing of sessions and other application states.

In addition, we can add links through the `.url()` method available on route functions, which generates URLs programmatically:

```python
import air
from cart import router as cart_router, cart

app = air.Air()
app.include_router(cart_router)


@app.page
def index():
    return air.Div(air.H1("Home page"), air.A("View cart", href=cart.url()))
```

## Query Parameters

Air supports query parameters through FastAPI's `Query()` validator, which you can import as `air.Query()`:

```python
import air

app = air.Air()


@app.get("/search")
def search(q: str = air.Query(""), page: int = air.Query(1)):
    return air.H1(f"Search: {q} (page {page})")


# Generate URLs with query parameters
@app.page
def index():
    return air.Div(
        air.A("Search", href=search.url(query_params={"q": "air", "page": 1}))
    )
```

The `.url()` method accepts a `query_params` argument for generating URLs with query strings. This works with both scalar values and lists:

```python
@app.get("/filter")
def filter_items(
    tags: list[str] | None = air.Query(None),
):  # List parameters require explicit air.Query(None) for parsing
    return air.H1(f"Filtered by: {tags}")


# Generates: /filter?tags=python&tags=web
url = filter_items.url(query_params={"tags": ["python", "web"]})
```

## Sync vs Async Handlers

Air dispatches `def` and `async def` handlers differently:

| You write | Air runs it in | Good for |
|---|---|---|
| `def handler():` | **threadpool** (off the event loop) | Blocking I/O: database queries, file reads, synchronous HTTP clients |
| `async def handler():` | **event loop** | Non-blocking I/O: `await request.form()`, async database drivers, `await client.get(...)` |

**Use `def` when you don't need `await`.** Sync handlers run in a threadpool, so blocking calls (ORM queries, file I/O, `httpx.Client()`) won't freeze other requests:

```python
@app.get("/users/{user_id}")
def user_detail(user_id: int):
    user = db.get_user(user_id)  # blocking call, safe in threadpool
    return air.H1(user.name)
```

**Use `async def` when you need `await`.** The handler runs directly on the event loop, so use async libraries for I/O:

```python
@app.post("/submit")
async def handle_form(request: air.Request):
    form = await request.form()  # needs await
    return air.H1(f"Got: {form['name']}")
```

!!! warning
    An `async def` handler that makes blocking calls (e.g., `time.sleep()`, synchronous database queries) will block the entire event loop, freezing all other requests until it finishes. If you're calling blocking code, use `def` instead.

---

::: air.routing
