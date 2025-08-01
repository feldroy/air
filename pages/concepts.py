import air


def render(request: air.Request):
    return air.Children(
        air.Title("Concepts"),
        air.Article(
            air.H1("Concepts"), air.P("Why and how Air works."), class_="prose"
        ),
    )
