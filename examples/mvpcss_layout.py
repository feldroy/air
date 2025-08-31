import air
from air.routing import AirRouter

app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(air.H1("Home page"), air.P(air.A("Click", href=item.url(id=3))))


@app.get("/{id}")
def item(id: int):
    return air.layouts.mvpcss(air.H1(f"Item {id}"), air.P(air.A("Click", href=index.url())))


# From a router too:
router = AirRouter()


@router.get("/users/{name}", name="user")
def user(name: str):
    return {"name": name}


app.include_router(router)

assert index.url() == "/"
assert item.url(id=5, ref="home") == "/5?ref=home"
assert user.url(name="alice") == "/users/alice"
