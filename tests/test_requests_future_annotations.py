"""Test that air.Request works with PEP 563 postponed annotations.

This file must have 'from __future__ import annotations' at the module level
to properly test the fix for string annotations.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

import air


def test_request_param_with_future_annotations() -> None:
    """Ensure Request parameter works with 'from __future__ import annotations'."""
    app = air.Air()

    @app.get("/test")
    def htmx_status(request: air.Request, *, is_htmx: bool = air.is_htmx_request) -> air.Div:
        htmx_status = "htmx" if is_htmx else "no-htmx"
        return air.Div(f"Status: {htmx_status}", class_="status")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert "Status: no-htmx" in response.text
    assert 'class="status"' in response.text


def test_request_param_with_htmx_detection() -> None:
    """Ensure air.Request works with HTMX detection for both HTMX and non-HTMX requests."""
    app = air.Air()

    @app.get("/htmx")
    def htmx_endpoint(request: air.Request, *, is_htmx: bool = air.is_htmx_request) -> air.H1:
        htmx_status = "HTMX" if is_htmx else "no HTMX"
        return air.H1(f"Request status: {htmx_status}")

    client = TestClient(app)

    # Test without HTMX header
    response = client.get("/htmx")
    assert response.status_code == 200
    assert "Request status: no HTMX" in response.text

    # Test with HTMX header
    response = client.get("/htmx", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert "Request status: HTMX" in response.text


def test_request_with_query_params() -> None:
    """Ensure Request parameter doesn't conflict with query parameters."""
    app = air.Air()

    @app.get("/query")
    def query_endpoint(request: air.Request, name: str = "World", *, is_htmx: bool = air.is_htmx_request) -> air.P:
        htmx_status = "HTMX" if is_htmx else "no HTMX"
        return air.P(f"Hello, {name}! ({htmx_status})")

    client = TestClient(app)

    # Test with default query param
    response = client.get("/query")
    assert response.status_code == 200
    assert "Hello, World!" in response.text
    assert "no HTMX" in response.text

    # Test with custom query param
    response = client.get("/query?name=Alice")
    assert response.status_code == 200
    assert "Hello, Alice!" in response.text
    assert "no HTMX" in response.text
