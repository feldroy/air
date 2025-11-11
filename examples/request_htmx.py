"""Example: Inspecting request.htmx in an Air app.

Usage:
    uv run examples/request_htmx.py

Then open http://127.0.0.1:8000/ in your browser.
"""

import air

app = air.Air()


@app.page
def index(request: air.Request):
    """ "Index page demonstrating request.htmx interaction.

    This page:

    - Loads the table automatically into the #display div via HTMX on page load.
    - Let's you reload the table via a normal HTMX request.
    - Let's you trigger a table load from a different element (to show trigger/target behavior).
    """
    return air.layouts.mvpcss(
        air.H1("Example: request.htmx"),
        air.P(
            "This example shows how ",
            air.Code("request.htmx"),
            " is populated for HTMX-driven requests.",
        ),
        air.Ul(
            air.Li("The first table loads automatically when the page loads."),
            air.Li("Use the button to reload it via a normal HTMX request."),
            air.Li(
                "Use the second button to trigger a request from a different element, "
                "so you can inspect the trigger/target values."
            ),
        ),
        # Controls
        air.Div(
            air.Button(
                "Reload table (normal HTMX request)",
                hx_get="/table",
                hx_target="#display",
                hx_swap="innerHTML",
            ),
            air.Button(
                "Load second table (trigger from this button)",
                id="other-trigger",
            ),
            id="controls",
        ),
        # This div will load the table once on page load via HTMX.
        air.Div(
            id="display",
            hx_get="/table",
            hx_trigger="load",
        ),
        # This second div demonstrates hx_trigger using a different element
        # as the source of the event (`click from:#other-trigger`).
        air.Div(
            id="display-2",
            hx_get="/table?source=external-trigger",
            hx_trigger="click from:#other-trigger",
        ),
    )


@app.page
def table(request: air.Request):
    """Render a table of key request.htmx attributes.

    This view is used as an HTMX target and shows:

    - The full request URL.
    - The raw request.htmx object.
    - Common HTMX attributes such as boosted, current_url, target, trigger, and prompt.
    """
    # We wrap values in str(...) so both the template and the type checker are happy.
    htmx = request.htmx

    return air.Table(
        air.Thead(
            air.Tr(
                air.Th("Attribute"),
                air.Th("Value"),
            )
        ),
        air.Tbody(
            air.Tr(
                air.Td("request.url"),
                air.Td(str(request.url)),
            ),
            air.Tr(
                air.Td("request.htmx"),
                air.Td(str(htmx)),
            ),
            air.Tr(
                air.Td("request.htmx.boosted"),
                air.Td(str(htmx.boosted)),
            ),
            air.Tr(
                air.Td("request.htmx.current_url"),
                air.Td(str(htmx.current_url)),
            ),
            air.Tr(
                air.Td("request.htmx.target"),
                air.Td(str(htmx.target)),
            ),
            air.Tr(
                air.Td("request.htmx.trigger"),
                air.Td(str(htmx.trigger)),
            ),
            air.Tr(
                air.Td("request.htmx.prompt"),
                air.Td(str(htmx.prompt)),
            ),
        ),
    )


if __name__ == "__main__":
    # Allow running this file directly:
    #   uv run python examples/request_htmx.py
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
