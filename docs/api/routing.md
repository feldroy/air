Routing

If you need to knit several Python modules with their own Air views into one, that's where Routing is used. They allow the near seamless combination of multiple Air apps into one. Larger sites are often built from multiple routers.

Let's imagine we have an e-commerce store with a shopping cart app. Use instantiate a `router` object using `air.AirRouter()` just as we would with `air.App()`:

```python
# cart.py
import air

router = air.AirRouter()

@router.page
def cart():
    return air.H1('I am a shopping cart')
```

Then in our main page we can load that and tie it into our main `app`.

```python
import air
from cart import router as cart_router

app = air.Air()
app.include_router(cart_router)

@app.page
def index():
    return air.H1('Home page')
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
    return air.Div(
        air.H1('Home page'),
        air.A('View cart', href=cart.url())
    )
```

---

::: air.routing
