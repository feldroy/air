import air

app = air.Air()


@app.page
def index():  # routes is "/"
    return air.H1("I am the home page")


@app.page
def data():  # route is "/data"
    return air.H1("I am the data page")


@app.page
def about_us():  # route is "/about-us"
    return air.H1("I am the about page")
