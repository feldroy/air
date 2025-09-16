import air


def index(title, content):
    return air.Html(air.Title(title), air.H1(content))
