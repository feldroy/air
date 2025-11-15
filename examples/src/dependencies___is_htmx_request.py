import air

app = air.Air()


@app.get("/")
def index_get(is_htmx: bool = air.is_htmx_request):
    return air.H1(f"Is HTMX request?: {is_htmx}")


@app.post("/")
def index_post(is_htmx: bool = air.is_htmx_request):
    return air.H1(f"Is HTMX request?: {is_htmx}")


@app.patch("/")
def index_patch(is_htmx: bool = air.is_htmx_request):
    return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))


@app.put("/")
def index_put(is_htmx: bool = air.is_htmx_request):
    return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))


@app.delete("/")
def index_delete(is_htmx: bool = air.is_htmx_request):
    return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))
