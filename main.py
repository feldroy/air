import air
from airdocs.utils import get_readme_as_html
from pathlib import Path

renderer = air.JinjaRenderer('templates')

app = air.Air()

def layout(request: air.Request, *content):
    head_tags = air.layouts.filter_head_tags(content)
    body_tags = air.layouts.filter_body_tags(content)
    return renderer(request, 'page.html',
                    head_tags=air.Children(*head_tags),
                    body_tags=air.Children(*body_tags)
    )


@app.page
def index(request: air.Request):
    return layout(
        request,
        air.Title('Air: The New FastAPI-Powered Python Web Framework (2025)'),
        air.H1('Air Documentation'),
        air.Raw(get_readme_as_html(Path('README.md'))),
        air.P("TODO: docs index")
    )
    