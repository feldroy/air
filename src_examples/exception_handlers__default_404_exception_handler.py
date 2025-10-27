import air

app = air.Air()


@app.get("/")
def index():
    return air.AirResponse(
        air.P("404 Not Found"),
        status_code=404
    )
