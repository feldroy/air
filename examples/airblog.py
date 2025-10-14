# /// script
# dependencies = [
#   "air",
#   "frontmatter",
#   "mistletoe",
#   "rich",
#   "uvicorn"
# ]
# ///
# ruff: noqa
# type: ignore
# pyrefly: ignore
"""
A markdown-powered blog for Air.

Usage:
    uv run airblog.py
"""

from functools import cache
from operator import itemgetter
from pathlib import Path

import mistletoe
import uvicorn
from frontmatter import Frontmatter
from rich import print

import air

app = air.Air()


@cache
def get_articles() -> list[dict]:
    articles = [Frontmatter.read_file(path) for path in Path("airblog").glob("*.md")]
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


@cache
def get_tags() -> dict[str, int]:
    articles = get_articles()
    unsorted_tags = {}
    for article in articles:
        for tag in article["attributes"].get("tags", []):
            if tag in unsorted_tags:
                unsorted_tags[tag] += 1
            else:
                unsorted_tags[tag] = 1
    tags: dict = dict(sorted(unsorted_tags.items(), key=itemgetter(1), reverse=True))
    return tags


def NavBar(request):
    return air.Nav(
        air.A("Home", href=request.url_for("index")),
        air.A("Tags", href="/tags"),
    )


def BlogPostPreview(article, request):
    return air.Aside(
        air.H3(
            air.A(
                article["attributes"]["title"],
                href=request.url_for("article_detail", slug=article["attributes"]["slug"]),
            )
        ),
        air.P(article["attributes"]["description"]),
        air.P(air.Small(article["attributes"]["date"])),
    )


@app.page
async def index(request: air.Request):
    title = "AirBlog!"
    return air.layouts.mvpcss(
        air.Title(title),
        air.Header(
            NavBar(request=request),
            air.H1(title),
            air.P("Your go-to platform for blogging with Air."),
        ),
        air.Section(*[BlogPostPreview(x, request) for x in get_articles()]),
    )


def get_article(slug: str) -> dict | None:
    # This function could be replaced with this code:
    # next((x for x in get_articles() if x['attributes']["slug"] == slug.strip()), None)
    for article in get_articles():
        if article["attributes"]["slug"].strip() == slug.strip():
            return article
    return None


@app.get("/article/{slug}")
async def article_detail(slug: str, request: air.Request):
    article = get_article(slug)
    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Header(
            NavBar(request=request),
            air.H1(article["attributes"]["title"]),
            air.P(air.I(article["attributes"].get("description"))),
            air.Time(air.Small(article["attributes"]["date"])),
        ),
        air.Article(air.Raw(mistletoe.markdown(article["body"]))),
        air.Footer(
            "Tags: ",
            *[air.Span(air.A(x, href=request.url_for("tag", slug=x)), " ") for x in article["attributes"]["tags"]],
            air.Br(),
            air.P(
                air.A("← Home", href="/"),
            ),
        ),
    )


@app.page
def tags(request: air.Request):
    return air.layouts.mvpcss(
        air.Title("Tags"),
        air.Header(
            NavBar(request=request),
            air.H1("Tags"),
            air.P("All the tags"),
        ),
        air.Article(
            air.Ul(*[air.Li(air.A(k, f" ({v})", href=request.url_for("tag", slug=k))) for k, v in get_tags().items()])
        ),
        air.Footer(
            air.P(
                air.A("← Home", href="/"),
            )
        ),
    )


@app.get("/tag/{slug}")
def tag(slug: str, request: air.Request):
    articles = (x for x in get_articles() if slug in x["attributes"]["tags"])
    return air.layouts.mvpcss(
        air.Title(f"Tag: {slug}"),
        air.Header(
            NavBar(request=request),
            air.H1(f"Tag: {slug}"),
        ),
        air.Section(*[BlogPostPreview(x, request) for x in articles]),
        air.Footer(
            air.P(
                air.A("← Home", href="/"),
            )
        ),
    )


if __name__ == "__main__":
    print("[bold]Demo server starting...[/bold]")  # noqa
    print("[bold]Open http://localhost:8005 in your browser[/bold]")
    uvicorn.run("airblog:app", host="127.0.0.1", port=8005, reload=True)
