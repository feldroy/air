import air


def index(title, content) -> air.Html:
    return air.Html(air.Title(title), air.H1(content))
