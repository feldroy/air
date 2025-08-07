import air
from air_markdown.tags import AirMarkdown


def render(request: air.Request):
    with open("/Users/arg/foss/air-repos/airdocs/pages/learn/tutorial.md", "r") as f:
        md_content = f.read()
    return air.Children(
        air.Title("Learn > Tutorial 1: Combining FastAPI and Air"),
        AirMarkdown(md_content),
    )
