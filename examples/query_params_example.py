import air
from air import Children, Html

app = air.Air()


@app.page
def search(q: str = air.Query(""), page: int = air.Query(1)) -> Children | Html:
    return air.layouts.mvpcss(
        air.Title(f"Search: {q}"),
        air.H1(f"Search Results for '{q}'"),
        air.P(f"Page: {page}"),
        air.Hr(),
        air.P(f"Query string received: q={q}, page={page}"),
        air.P(air.A("Back to home", href=index.url())),
    )


@app.page
def filter_tags(
    tags: list[str] | None = air.Query(None),  # noqa: B008
) -> Children | Html:
    tags_display = tags or []
    return air.layouts.mvpcss(
        air.Title("Filter by Tags"),
        air.H1("Filter Results"),
        air.P(f"Tags: {', '.join(tags_display) if tags_display else 'None'}"),
        air.Hr(),
        air.P(f"Received {len(tags_display)} tag(s): {tags_display}"),
        air.P(air.A("Back to home", href=index.url())),
    )


@app.page
def advanced_search(
    q: str = air.Query(""),
    page: int = air.Query(1),
    tags: list[str] | None = air.Query(None),  # noqa: B008
) -> Children | Html:
    tags_display = tags or []
    return air.layouts.mvpcss(
        air.Title(f"Advanced Search: {q}"),
        air.H1("Advanced Search Results"),
        air.Dl(
            air.Dt("Query:"),
            air.Dd(q),
            air.Dt("Page:"),
            air.Dd(str(page)),
            air.Dt("Tags:"),
            air.Dd(", ".join(tags_display) if tags_display else "None"),
        ),
        air.Hr(),
        air.P(f"Full query: q={q}, page={page}, tags={tags_display}"),
        air.P(air.A("Back to home", href=index.url())),
    )


@app.page
def index() -> Children | Html:
    return air.layouts.mvpcss(
        air.Title("Query Parameters Example"),
        air.H1("Query Parameters in Air"),
        air.P("Air supports FastAPI's Query() for parameter validation and query_params for URL generation."),
        air.H2("Scalar Query Parameters"),
        air.Ul(
            air.Li(air.A("Page 1", href=search.url(query_params={"q": "air", "page": 1}))),
            air.Li(air.A("Page 2", href=search.url(query_params={"q": "air", "page": 2}))),
            air.Li(air.A("Page 3", href=search.url(query_params={"q": "air", "page": 3}))),
        ),
        air.H2("List Query Parameters"),
        air.Ul(
            air.Li(
                air.A(
                    "Python & JavaScript",
                    href=filter_tags.url(query_params={"tags": ["python", "javascript"]}),
                )
            ),
            air.Li(
                air.A(
                    "Web & API",
                    href=filter_tags.url(query_params={"tags": ["web", "api"]}),
                )
            ),
            air.Li(air.A("Single Tag", href=filter_tags.url(query_params={"tags": ["htmx"]}))),
        ),
        air.H2("Combined Parameters"),
        air.P(
            air.A(
                "Search 'framework' on page 2 with tags",
                href=advanced_search.url(
                    query_params={
                        "q": "framework",
                        "page": 2,
                        "tags": ["python", "web"],
                    }
                ),
            )
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
