from time import time

import uvicorn

import air
from air.caches import CacheFactory

app = air.Air(
    cache=CacheFactory.create(
        config={
            "engine": "redis",
            "url": "redis://username:password@localhost.com:6379/0",
        },
    )
)


@app.page(cache_ttl=60)  # 1 minute TTL
def about_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_factory_about_page_renders", 0) + 1
    globals()["_factory_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About — cache test"),
        air.H1(f"About Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P("If this page is cached the render count will not increase until the TTL expires."),
        air.A("Go back to home page", href=index.url()),
    )


@app.page(cache_ttl=30)  # 30 seconds TTL
async def aabout_page() -> air.Children | air.Html:
    # simple render counter stored in module globals to verify caching
    count: int = globals().get("_factory_async_about_page_renders", 0) + 1
    globals()["_factory_async_about_page_renders"] = count
    ts = time()

    return air.layouts.mvpcss(
        air.Title("About (async) — cache test"),
        air.H1(f"About (async) Page (render #{count})"),
        air.P(f"Render timestamp: {ts:.3f}"),
        air.P("If this page is cached the render count will not increase until the TTL expires."),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("Cache Factory Sample"),
        air.H1("Cache Factory Sample"),
        air.A("Go to About Page", href=about_page.url()),
        air.Br(),
        air.A("Go to About (async) Page", href=aabout_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("cache_factory:app", host="127.0.0.1", port=8005, reload=True)
