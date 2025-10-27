import uvicorn

import air

app = air.Air()


@app.page
def about_page() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("URL Helper Sample"),
        air.H1("About Page"),
        air.P("This is a home page!"),
        air.A("Go back to home page", href=index.url()),
    )


@app.page
def index() -> air.Children | air.Html:
    return air.layouts.mvpcss(
        air.Title("URL Helper Sample"),
        air.H1("URL Helper Sample"),
        air.A("Go to About Page", href=about_page.url()),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("url_helper_sample:app", host="127.0.0.1", port=8005, reload=True)
