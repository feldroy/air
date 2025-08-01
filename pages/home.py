import air


def render(request: air.Request):
    return air.Children(
        air.Img(src="https://air-svgs.fastapicloud.dev/static/air-3color.svg", width="400", alt="Air logo"),
        air.H2("The new Python web framework built on FastAPI.")
    )
