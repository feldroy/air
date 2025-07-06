from typing import Annotated

from fastapi import Depends, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

import air


def test_form_validation_dependency_injection():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(cheese: Annotated[CheeseForm, Depends(CheeseForm.validate)]):
        if cheese.is_valid:
            return air.Html(air.H1(cheese.data.name))
        return air.Html(air.H1(air.RawHTML(str(len(cheese.errors)))))  # type: ignore [arg-type]

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    # Test with invalid form data
    response = client.post("/cheese", data={})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>2</h1></html>"


def test_form_validation_in_view():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request):
        cheese = await CheeseForm.validate(request)
        if cheese.is_valid:
            return air.Html(air.H1(cheese.data.name))
        return air.Html(air.H1(air.RawHTML(str(len(cheese.errors)))))  # type: ignore [arg-type]

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    # Test with invalid form data
    response = client.post("/cheese", data={})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>2</h1></html>"
