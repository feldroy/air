from typing import Annotated

from fastapi.testclient import TestClient

from air import H1, Air, is_htmx_request


def test_is_htmx() -> None:
    """Test the is_htmx method, which only works if the response is wrapped."""

    app = Air()

    @app.get("/test")
    def test_endpoint(is_htmx: Annotated[bool, is_htmx_request]):
        return H1(f"Is HTMX request: {is_htmx}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: True</h1>"

    response = client.get("/test", headers={"hx-request": "false"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"

    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"
