import air

app = air.Air()


@app.page
def index():  # routes is "/"
    return air.H1("This is the home page.")


@app.page
def data():  # route is "/data"
    return air.H1("This is the data page.")


@app.page
def about_us():  # route is "/about-us"
    return air.H1("This is the about page.")


@app.page
def contact_us():  # route is /contact-us"
    return air.H1("This is the contact us page.")
