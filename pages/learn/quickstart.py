import air
from air_markdown import TailwindTypographyMarkdown as Markdown

def render(request: air.Request):
    with open("quickstart.md", "r") as f:
        md_content = f.read()
    return air.Children(
        air.Title("Learn > Quickstart"),
        Markdown(md_content),
    )
