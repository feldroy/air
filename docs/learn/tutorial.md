# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app.

Let's start by combining Air and FastAPI. With just a few lines of code, you can serve a homepage and an API side by side:

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

@app.get("/")
def landing_page():
    return air.layouts.mvpcss(
        air.Head(air.Title("My Awesome Startup")),
        air.Body(
            air.H1("My Awesome Startup"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )

@api.get("/")
def api_root():
    return {"message": "My Awesome Startup is powered by FastAPI"}

# Bring it all together: mount your API under /api
app.mount("/api", api)
```

## TODO

Add the rest of this tutorial page.


## Want to learn more?

Want to see a handy batch of recipes for doing things in Air? [Check out the Air Cookbook!](cookbook/index.md)


