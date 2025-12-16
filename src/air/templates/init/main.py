import air
from .config import settings


app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(
        air.Title("Home page"),
        air.H1("Home page"),
    )

