import air

app = air.Air()

jinja = air.JinjaRenderer(".")


@app.page
def index(request: air.Request) -> air.BaseTag:
    return air.layouts.mvpcss(air.Title("Home Page"), jinja(request, "jinja_in_air_tags.html", as_string=True))
