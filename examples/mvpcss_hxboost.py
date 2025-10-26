import air

app = air.Air()


@app.page
def index(is_htmx=air.is_htmx_request):
    return air.layouts.mvpcss(
        air.Title("Home"),
        air.Article(
            air.H1("Welcome to Air"), air.P(air.A("Click to go to Dashboard", href="/dashboard")), hx_boost="true"
        ),
        is_htmx=is_htmx,
    )


@app.page
def dashboard(is_htmx=air.is_htmx_request):
    return air.layouts.mvpcss(
        air.Title("Dashboard"),
        air.Article(air.H1("Dashboard"), air.P(air.A("Go home", href="/")), hx_boost="true"),
        is_htmx=is_htmx,
    )
