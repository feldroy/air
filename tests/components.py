from air.tags.models.special import Html
import air


def index(title, content) -> Html:
    return air.Html(air.Title(title), air.H1(content))
