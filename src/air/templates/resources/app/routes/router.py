import air

router = air.AirRouter()


@router.get('/')
def {{name}}_index():
    return air.layouts.mvpcss(
        air.Title("{{name}}"),
        air.H1("{{name}}")
    )