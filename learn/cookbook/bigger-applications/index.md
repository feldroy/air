# Bigger Applications

When building larger applications with Air, you may find yourself needing to organize your code better, manage multiple routes, or even mount different applications together. This guide will help you understand how to structure your Air applications for scalability and maintainability.

## Routing Separate Apps Together

Note

This approach shares state between the composited efforts. This means that authentication, database pooling, and other things will be usable between components. The [API reference](../../../api/routing/) for this documentation displays options for more controls like Router-specific lifespans, URL prefixes, and more.

Let's imagine we have a landing page that links to a sophisticated dashboard. While our example dashboard is trivial, let's assume it is complicated enough that we want it in a separate Python module yet share state. We design the `main.py` as we would a normal Air application:

main.py

```
import air

app = air.Air()

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1('Avatar Data'),
        air.P(air.A('Dashboard', href='/dashboard'))
    )
```

Now for the dashboard, instead of using the typical `air.Air` tool to instantiate our application, we use `air.AirRouter` like so:

dashboard.py

```
import air

router = air.AirRouter()

@router.page
def dashboard():
    return air.layouts.mvpcss(
        air.H1('Avatar Data Dashboard'),
        air.P(air.A('<- Home', href='/'))
    )
```

Now if we go back to our `main.py` we can use the `app.include_router()` method to include the dashboard in our app:

main.py

```
import air
from .dashboard import router

app = air.Air()
app.include_router(router)

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1('Avatar Data'),
        air.P(air.A('Dashboard', href='/dashboard'))
    )
```

If run locally these links should work:

- http://localhost:8000
- http://localhost:8000/dashboard

## Mounting Air and FastAPI apps inside Air apps

Warning

This approach does not share state between the apps. That means attempting to share authentication and database pooling will not function predictably, if at all.

One of the really nice features of Air is the ability to mount apps inside each other. This allows you to create modular applications where different parts of your app can be developed and maintained independently. To do this, we lean on Starlette's `mount` functionality that Air inherits through FastAPI.

```
import air

# Create the main app, which serves as the entry point
app = air.Air(title='Air')

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1('Air landing page'),
        air.P(air.A('Shop', href='/shop'))
    )

# Creating a separate app for the shop,
# which could be placed in a different file
shop = air.Air(title='Air shop')

@shop.page
def index():
    return air.layouts.mvpcss(
        air.H1('Shop for Air things')
    )

# Mount the shop app to the main app
# This allows you to access the shop at /shop
app.mount('/shop', shop)
```

## Mounting FastAPI inside of Air apps

You can easily mount a FastAPI app inside an Air app. A common scenario is to have a FastAPI app that serves an API, while your main Air app serves the landing, billing, and usage frontends.

```
import air
from fastapi import FastAPI

# Create the landing page app using Air
app = air.Air()

@app.get("/")
def landing_page():
    return air.Html(
        air.Head(air.Title("Awesome SaaS")),
        air.Body(
            air.H1("Awesome SaaS"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )

api = FastAPI()

@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}

# Combining the Air and and FastAPI apps into one
app.mount("/api", api)
```

## Mounting FastAPI apps inside each other

Mounting one FastAPI app is outside the scope of this guide. We recommend reading [FastAPI's Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications) reference.
