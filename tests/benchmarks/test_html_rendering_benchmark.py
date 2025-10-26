"""Benchmark comparing Air Tags vs Jinja2 template rendering performance.

This benchmark measures the performance of Air's tag-based HTML generation
against traditional Jinja2 template rendering for equivalent HTML output.
"""

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from starlette.requests import Request
from starlette.templating import _TemplateResponse

import air
from air import Html
from air.templating import JinjaRenderer


def create_complex_page_with_tags() -> Html:
    """Generate a complex HTML page using Air Tags."""
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
                            id=f"product-{i}",
                        )
                        for i in range(1, 21)  # 20 products
                    ],
                    class_="product-grid",
                ),
            ),
            air.Footer(air.P("&copy; 2024 Product Store", class_="copyright")),
        ),
    )


def create_complex_page_with_jinja(jinja_renderer: JinjaRenderer, mock_request: Mock) -> _TemplateResponse:
    """Generate the same complex HTML page using Jinja2 templates."""
    context = {
        "title": "Product Catalog",
        "products": [
            {"id": i, "name": f"Product {i}", "description": f"Description for product {i}", "price": f"${i * 10}.99"}
            for i in range(1, 21)  # 20 products
        ],
    }
    return jinja_renderer(mock_request, "complex_page.html", context=context)


def test_air_tags_vs_jinja_rendering_benchmark(benchmark: Any) -> None:
    """Benchmark Air Tags vs Jinja2 template rendering for equivalent HTML.

    This tests the performance of Air's tag-based approach against traditional template rendering.
    """

    # Create a temporary template for Jinja2
    template_content = """<html>
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

    # Set up temporary template directory
    with tempfile.TemporaryDirectory() as temp_dir:
        template_path = Path(temp_dir) / "complex_page.html"
        template_path.write_text(template_content)

        jinja_renderer = JinjaRenderer(directory=temp_dir)

        # Create minimal mock request object
        from unittest.mock import Mock

        from starlette.datastructures import URL

        mock_request = Mock(spec=Request)
        mock_request.url = URL("http://localhost/test")

        # Benchmark Air Tags rendering
        def render_with_air_tags() -> str:
            page = create_complex_page_with_tags()
            return page.render()

        # Benchmark Jinja2 rendering
        def render_with_jinja() -> _TemplateResponse:
            return create_complex_page_with_jinja(jinja_renderer, mock_request)

        # Benchmark Air Tags rendering
        benchmark(render_with_air_tags)


def test_simple_air_tags_rendering_benchmark(benchmark: Any) -> None:
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
