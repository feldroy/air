import air


def index(title: str, content: str) -> air.Html:
    return air.Html(air.Title(title), air.H1(content))
