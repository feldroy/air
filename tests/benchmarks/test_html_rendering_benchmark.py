"""Benchmark comparing Air Tags vs Jinja2 template rendering performance.

This benchmark measures the performance of Air's tag-based HTML generation
against traditional Jinja2 template rendering for equivalent HTML output.
"""

import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import HTMLResponse

import air
from air import Html
from air.templating import JinjaRenderer


def create_complex_page_with_tags() -> Html:
    """Generate a complex HTML page using Air Tags.

    Returns:
        Complete HTML page with product catalog.
    """
    return air.Html(
        air.Head(
            air.Title("Product Catalog"),
            air.Meta(charset="utf-8"),
            air.Link(rel="stylesheet", href="/static/styles.css"),
        ),
        air.Body(
            air.Header(
                air.Nav(
                    air.Ul(
                        air.Li(air.A("Home", href="/")),
                        air.Li(air.A("Products", href="/products")),
                        air.Li(air.A("About", href="/about")),
                        class_="nav-list",
                    )
                )
            ),
            air.Main(
                air.H1("Product Catalog", class_="page-title"),
                air.Section(
                    *[
                        air.Article(
                            air.H2(f"Product {i}", class_="product-title"),
                            air.P(f"Description for product {i}", class_="product-desc"),
                            air.Div(
                                air.Span(f"${i * 10}.99", class_="price"),
                                air.Button("Add to Cart", class_="btn btn-primary", data_product=str(i)),
                                class_="product-actions",
                            ),
                            class_="product-card",
                            id_=f"product-{i}",
                        )
                        for i in range(1, 21)  # 20 products
                    ],
                    class_="product-grid",
                ),
            ),
            air.Footer(air.P("&copy; 2024 Product Store", class_="copyright")),
        ),
    )


def create_complex_page_with_jinja(jinja_renderer: JinjaRenderer, mock_request: Mock) -> HTMLResponse:
    """Generate the same complex HTML page using Jinja2 templates.

    Returns:
        TemplateResponse with rendered Jinja2 template.
    """
    context = {
        "title": "Product Catalog",
        "products": [
            {"id": i, "name": f"Product {i}", "description": f"Description for product {i}", "price": f"${i * 10}.99"}
            for i in range(1, 21)  # 20 products
        ],
    }
    return jinja_renderer(mock_request, "complex_page.html", context=context)


JINJA_TEMPLATE_CONTENT = """<html>
<head>
    <title>{{ title }}</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <header>
        <nav>
            <ul class="nav-list">
                <li><a href="/">Home</a></li>
                <li><a href="/products">Products</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h1 class="page-title">{{ title }}</h1>
        <section class="product-grid">
            {% for product in products %}
            <article class="product-card" id="product-{{ product.id }}">
                <h2 class="product-title">{{ product.name }}</h2>
                <p class="product-desc">{{ product.description }}</p>
                <div class="product-actions">
                    <span class="price">{{ product.price }}</span>
                    <button class="btn btn-primary" data-product="{{ product.id }}">Add to Cart</button>
                </div>
            </article>
            {% endfor %}
        </section>
    </main>
    <footer>
        <p class="copyright">&copy; 2024 Product Store</p>
    </footer>
</body>
</html>"""


@pytest.fixture
def jinja_setup() -> Generator[tuple[JinjaRenderer, Mock], None, None]:
    """Set up Jinja renderer and mock request for benchmarking."""
    with tempfile.TemporaryDirectory() as temp_dir:
        template_path = Path(temp_dir) / "complex_page.html"
        template_path.write_text(JINJA_TEMPLATE_CONTENT)
        jinja_renderer = JinjaRenderer(directory=temp_dir)
        mock_request = Mock(spec=Request)
        mock_request.url = URL("http://localhost/test")
        yield jinja_renderer, mock_request


def test_air_tags_complex_rendering_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark Air Tags rendering for complex HTML page."""

    def render_with_air_tags() -> str:
        page = create_complex_page_with_tags()
        return page.render()

    benchmark(render_with_air_tags)


def test_jinja_complex_rendering_benchmark(
    benchmark: BenchmarkFixture,
    jinja_setup: tuple[JinjaRenderer, Mock],
) -> None:
    """Benchmark Jinja2 rendering for complex HTML page."""
    jinja_renderer, mock_request = jinja_setup

    def render_with_jinja() -> HTMLResponse:
        return create_complex_page_with_jinja(jinja_renderer, mock_request)

    benchmark(render_with_jinja)


def test_simple_air_tags_rendering_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark simple Air Tags rendering for baseline performance."""

    def render_simple_page() -> str:
        page = air.Html(
            air.Head(air.Title("Simple Page")),
            air.Body(
                air.H1("Welcome"),
                air.P("This is a simple page"),
                air.Div(air.A("Click here", href="/next"), class_="container"),
            ),
        )
        return page.render()

    benchmark(render_simple_page)
