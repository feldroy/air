from typing import Annotated

from fastapi import Form
from fastapi.testclient import TestClient
import air


def test_is_form_response_html():
    """Test if form responses are HTML, regardless if valid data or not."""

    app = air.Air()

    @app.post("/login/")
    async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
        return air.Html(air.H1(username), air.H2(password))

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/login", data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>testuser</h1><h2>testpass</h2></html>"
    
    # Test with empty form data
    response = client.post("/login", data={})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == 'asfsad'   