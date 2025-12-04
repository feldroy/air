import air

app = air.Air()
router = air.AirRouter()


@router.get("/example")
def index() -> air.AirResponse:
    return air.AirResponse(air.P("I am an example route."), status_code=404)


app.include_router(router)
