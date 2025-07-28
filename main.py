import air
from airdocs.utils import get_readme_as_html
from fastapi import HTTPException
from pathlib import Path
from pydantic import BaseModel
from html2tags import html_to_air_tags
import mistletoe

renderer = air.JinjaRenderer('templates')

app = air.Air()

class AirDocHTMLRenderer(mistletoe.HTMLRenderer):
    pass

class Markdown(air.Tag):
    def __init__(self, *args, **kwargs):
        """Convert a Markdown string to HTML using mistletoe

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("Markdown tag accepts only one string argument")

        raw_string = args[0] if args else ""

        if not isinstance(raw_string, str):
            raise TypeError("Markdown tag only accepts string content")

        super().__init__(raw_string)

    def render(self) -> str:
        """Render the string with the Markdown library."""
        content = self._children[0] if self._children else ""
        return f'<article class="prose">{mistletoe.markdown(content, AirDocHTMLRenderer)}</article>'
                

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
        Markdown(get_readme_as_html(Path('README.md'))),
        air.P("TODO: docs index")
    )

@app.get('/{slug}')
def markdown_page(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(
            request, Markdown(text)
        )
    raise HTTPException(status_code=404)
    

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