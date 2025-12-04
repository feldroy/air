import air

app = air.Air()


@app.page
async def index(request: air.Request) -> air.Html | air.Children:
    return air.layouts.mvpcss(
        air.Title("Home"),
        air.Article(
            air.H1("Welcome to Air"),
            air.P(air.A("Click to go to Dashboard", href="/dashboard")),
            hx_boost="true",
        ),
        is_htmx=request.htmx.is_hx_request,
    )


@app.page
async def dashboard(request: air.Request) -> air.Html | air.Children:
    return air.layouts.mvpcss(
        air.Title("Dashboard"),
        air.Article(
            air.H1("Dashboard"),
            air.P(air.A("Go home", href="/")),
            hx_boost="true",
        ),
        is_htmx=request.htmx.is_hx_request,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
