"""Tests for Air's AirForm integration.

AirForm validation and rendering are tested in the airform package.
AirField metadata is tested in the airfield package.
These tests cover Air-specific usage: from_request() with Starlette,
Depends(), embedding rendered HTML in Air Tags, and re-exports.
"""

import re
from typing import Annotated, cast

from fastapi import Depends, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

import air
from air import AirForm


def _extract_csrf_token(html: str) -> str:
    """Extract the CSRF token from rendered form HTML."""
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match, "No CSRF token found in rendered HTML"
    return match.group(1)


def test_form_validation_dependency_injection() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.get("/cheese")
    async def cheese_page(request: Request) -> air.Html:
        form = CheeseForm()
        return air.Html(form.render())

    @app.post("/cheese")
    async def cheese_form(
        cheese: Annotated[CheeseForm, Depends(CheeseForm.from_request)],
    ) -> air.Html:
        if cheese.is_valid:
            data = cast("CheeseModel", cheese.data)
            return air.Html(air.H1(data.name))
        assert cheese.errors is not None
        return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))

    client = TestClient(app)

    # GET the form to obtain a CSRF token
    get_response = client.get("/cheese")
    csrf_token = _extract_csrf_token(get_response.text)

    # POST with valid data + CSRF token
    response = client.post("/cheese", data={"name": "cheddar", "age": 5, "csrf_token": csrf_token})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    # POST with missing fields + fresh CSRF token (need a new one each time)
    get_response = client.get("/cheese")
    csrf_token = _extract_csrf_token(get_response.text)
    response = client.post("/cheese", data={"csrf_token": csrf_token})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>2</h1></html>"


def test_form_validation_in_view() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.get("/cheese")
    async def cheese_page(request: Request) -> air.Html:
        form = CheeseForm()
        return air.Html(form.render())

    @app.post("/cheese")
    async def cheese_form(request: Request) -> air.Html:
        cheese = await CheeseForm.from_request(request)
        if cheese.is_valid:
            data = cast("CheeseModel", cheese.data)
            return air.Html(air.H1(data.name))
        assert cheese.errors is not None
        return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))

    client = TestClient(app)

    get_response = client.get("/cheese")
    csrf_token = _extract_csrf_token(get_response.text)

    response = client.post("/cheese", data={"name": "cheddar", "age": 5, "csrf_token": csrf_token})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    get_response = client.get("/cheese")
    csrf_token = _extract_csrf_token(get_response.text)
    response = client.post("/cheese", data={"csrf_token": csrf_token})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>2</h1></html>"


def test_form_render_in_view() -> None:
    """render() output embeds directly in Air Tags via SafeHTML __html__ protocol."""

    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request) -> air.Form:
        cheese = CheeseForm()
        return air.Form(cheese.render())

    client = TestClient(app)

    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert "<form>" in response.text
    assert '<label for="name">name</label>' in response.text
    assert "csrf_token" in response.text
    assert "</form>" in response.text


def test_airform_generic_type_parameter() -> None:
    """AirForm[M] sets model from the type parameter."""

    class JeepneyRouteModel(air.AirModel):
        route_name: str
        origin: str
        destination: str

    class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
        pass

    assert JeepneyRouteForm.model is JeepneyRouteModel

    form = JeepneyRouteForm()
    form.validate({"route_name": "01C", "origin": "Antipolo", "destination": "Cubao"})
    assert form.is_valid
    assert form.data.route_name == "01C"
    assert isinstance(form.data, JeepneyRouteModel)


def test_airform_reexport() -> None:
    """Air re-exports AirForm from airform."""
    assert air.AirForm is AirForm
