from typing import Any

import air


def index(title: str, content: Any) -> air.Html:
    return air.Html(air.Title(title), air.H1(content))
