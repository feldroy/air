import air

router = air.AirRouter()


@router.page
def dashboard() -> air.BaseTag:
    return air.layouts.mvpcss(air.H1("Avatar Data Dashboard"), air.P(air.A("<- Home", href="/")))
