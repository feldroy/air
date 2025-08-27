import air

app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("Home"),
                air.Ul(
                    air.Li(air.A("One")),
                    air.Li(air.A("Two")),
                ),
            ),
            air.H1("Hello, world"),
        ),
        air.H2("Here we are"),
    )
