import air
from airdocs.utils import get_readme_as_html
from pathlib import Path
from pydantic import BaseModel
import xml
from html2tags import html_to_air_tags

renderer = air.JinjaRenderer('templates')

app = air.Air()

def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception('First arg of layout needs to be an air.Request')
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
    

@app.page
def convert(request: air.Request):
    title = 'Convert HTML to Air Tags'
    return layout(
        request,
        air.Title(title),
        air.H1(title),
        air.Form(
            air.Textarea(
                rows=10, cols="80",
                placeholder='HTML to be converted goes here...',
                id="html",
                name='html',
                hx_trigger="input changed delay:500ms",
                hx_post="/converter",
            ),
        ),
        air.Hr(),
        air.Div(
            air.P('Nothing changed'),
            id='result',
            hx_swap_oob="true"
        )
    )


class HtmlModel(BaseModel):
    html: str


class HtmlForm(air.AirForm):
    model = HtmlModel

@app.post('/converter')
async def converter(request: air.Request):
    form = await request.form()
    html = form.get('html', '')
    return air.Div(
        air.Pre(
            air.Code(html_to_air_tags(html))
        ),
        id='result',
        hx_swap_oob="true",
    )