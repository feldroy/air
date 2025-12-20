import air

app = air.Air()


@app.page
def index() -> air.BaseTag:
    return air.layouts.mvpcss(
        air.Title("{{cookiecutter.name}} home page"),
        air.H1("{{cookiecutter.name}} home page"),
    )
