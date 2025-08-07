import air
from air_markdown.tags import AirMarkdown


def render(request: air.Request):
    with open("quickstart.md", "r") as f:
        md_content = f.read()
    return air.Children(
        air.Title("Learn > Quickstart"),
        AirMarkdown(md_content),
    )
