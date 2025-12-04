import air

app = air.Air()
router = air.AirRouter()


@app.page
def index() -> air.H1:  # route is "/"
    return air.H1("I am the home page")


@router.page
def data() -> air.H1:  # route is "/data"
    return air.H1("I am the data page")


@router.page
def about_us() -> air.H1:  # route is "/about-us"
    return air.H1("I am the about page")


app.include_router(router)
