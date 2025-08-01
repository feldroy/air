import air


def render(request: air.Request):
    return air.Children(
        air.H1("Air"),
        air.H2("The new Python web framework built on FastAPI.")
    )
