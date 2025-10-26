from time import time

import air

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")


@app.page
async def index(request: air.Request):
    if "first-visited" not in request.session:
        request.session["first-visited"] = time()
    return air.layouts.mvpcss(
        air.H1(request.session.get("first-visited")),
        air.P("Refresh the page and the timestamp won't change"),
        air.P(air.A("Reset the time stamp", href="/reset")),
    )


@app.page
async def reset(request: air.Request):
    request.session.pop("first-visited")
    return air.responses.RedirectResponse("/")
