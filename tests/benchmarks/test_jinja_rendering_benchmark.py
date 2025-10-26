"""Benchmark Jinja2 template rendering performance in Air.

This provides a comparison baseline for Air Tags performance by measuring
equivalent HTML generation using Jinja2 templates.
"""

import tempfile
from pathlib import Path
from typing import Any

from starlette.requests import Request
from starlette.templating import _TemplateResponse

from air.templating import JinjaRenderer


def test_jinja_complex_page_rendering_benchmark(benchmark: Any) -> None:
    """Benchmark Jinja2 template rendering for complex HTML structure."""

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

    with tempfile.TemporaryDirectory() as temp_dir:
        template_path = Path(temp_dir) / "complex_page.html"
        template_path.write_text(template_content)

        jinja_renderer = JinjaRenderer(directory=temp_dir)

        # Create minimal mock request object
        from unittest.mock import Mock

        from starlette.datastructures import URL

        mock_request = Mock(spec=Request)
        mock_request.url = URL("http://localhost/test")

        context = {
            "title": "Product Catalog",
            "products": [
                {
                    "id": i,
                    "name": f"Product {i}",
                    "description": f"Description for product {i}",
                    "price": f"${i * 10}.99",
                }
                for i in range(1, 21)  # 20 products
            ],
        }

        def render_jinja_page() -> _TemplateResponse:
            return jinja_renderer(mock_request, "complex_page.html", context=context)

        benchmark(render_jinja_page)
