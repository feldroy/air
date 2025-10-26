import air

app = air.Air()


@app.get("/")
def index(is_htmx: bool = air.is_htmx_request):
    return air.H1(f"Is HTMX request?: {is_htmx}")
