from typing import Annotated

from fastapi import Form
from fastapi.testclient import TestClient
import air


def test_is_form_response_html():
    """Test if form responses are HTML, regardless if valid data or not."""

    app = air.Air()

    @app.post("/cheese/")
    async def new_cheese_form(cheese: Annotated[str, Form()]):
        return air.Html(air.H1(cheese))

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/cheese", data={'cheese': 'cheddar'})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"
    
    # Test with empty form data
    response = client.post("/cheese", data={})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == 'asfsad'   