import air

app = air.Air()


@app.page
def index() -> air.BaseTag:
    return air.layouts.mvpcss(
        air.Title("Home page"),
        air.H1("Home page"),
    )
