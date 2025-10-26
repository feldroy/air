"""
This project define an index page and displaying a table.
As soon as the page loads, the table coming from the table function will be displayed.
"""

import air

app = air.Air()


@app.page
def index(request: air.AirRequest):
    return air.layouts.mvpcss(
        air.H1('Example: request.htmx'),
        air.Div(
            hx_get='/table',
            hx_trigger='load',
            id='display'
        )
    )

@app.page
def table(request: air.AirRequest):
    return  air.Table(
            air.Thead(air.Tr(air.Th("Attr"), air.Th("value"))),
            air.Tr(air.Td("request.htmx"), air.Td(request.htmx)),
            air.Tr(air.Td("request.htmx.boosted"), air.Td(request.htmx.boosted)),
            air.Tr(air.Td("request.htmx.current_url"), air.Td(request.htmx.current_url)),
            air.Tr(air.Td("request.htmx.prompt"), air.Td(request.htmx.prompt)),
            air.Tr(air.Td("request.htmx.target"), air.Td(request.htmx.target)),
            air.Tr(air.Td("request.htmx.trigger"), air.Td(request.htmx.trigger)),
        )

