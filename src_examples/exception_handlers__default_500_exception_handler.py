import air

app = air.Air()


@app.get("/")
def index():
    return air.AirResponse(air.P("500 Internal Server Error"), status_code=500)
