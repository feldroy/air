"""Tests for Air's AirForm integration.

AirForm validation and rendering are tested in the airform package.
AirField metadata is tested in the airfield package.
These tests cover Air-specific usage: from_request() with Starlette,
Depends(), embedding rendered HTML in Air Tags, and re-exports.
"""

from typing import Annotated, cast

from fastapi import Depends, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

import air
from air import AirForm


def test_form_validation_dependency_injection() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

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

    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    response = client.post("/cheese", data={})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>2</h1></html>"


def test_form_validation_in_view() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request) -> air.Html:
        cheese = await CheeseForm.from_request(request)
        if cheese.is_valid:
            data = cast("CheeseModel", cheese.data)
            return air.Html(air.H1(data.name))
        assert cheese.errors is not None
        return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))

    client = TestClient(app)

    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    response = client.post("/cheese", data={})
    assert response.status_code == 200
    assert response.text == "<!doctype html><html><h1>2</h1></html>"


def test_form_render_in_view() -> None:
    """render() output embeds in Air Tags via air.Raw()."""

    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request) -> air.Form:
        cheese = CheeseForm()
        return air.Form(air.Raw(cheese.render()))

    client = TestClient(app)

    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert "<form>" in response.text
    assert '<label for="name">name</label>' in response.text
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


def test_airform_reexports_helpers() -> None:
    """Air re-exports AirForm helper functions."""
    assert callable(air.forms.default_form_widget)
    assert callable(air.forms.errors_to_dict)
    assert callable(air.forms.get_user_error_message)
    assert callable(air.forms.pydantic_type_to_html_type)
