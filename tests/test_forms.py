from typing import Annotated

from fastapi import Depends, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

import air


def test_form_sync_check():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm()
    cheese.validate({"name": "Parmesan", "age": "Hello"})
    assert cheese.is_valid is False
    assert cheese.errors == [
        {
            "type": "int_parsing",
            "loc": ("age",),
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "Hello",
            "url": "https://errors.pydantic.dev/2.11/v/int_parsing",
        }
    ]


def test_form_validation_dependency_injection():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(
        cheese: Annotated[CheeseForm, Depends(CheeseForm.from_request)],
    ):
        if cheese.is_valid:
            return air.Html(air.H1(cheese.data.name))  # type: ignore [union-attr]
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
        cheese = await CheeseForm.from_request(request)
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


def test_form_render():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm()

    assert (
        cheese.render()
        == '<fieldset><label>name<input name="name" type="text" id="name"></input></label><label>age<input name="age" type="number" id="age"></input></label></fieldset>'
    )


def test_form_render_with_values():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm(dict(name="Cheddar", age=3))

    assert (
        cheese.render()
        == '<fieldset><label>name<input name="name" type="text" id="name" value="Cheddar"></input></label><label>age<input name="age" type="number" id="age" value="3"></input></label></fieldset>'
    )


def test_form_render_in_view():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request):
        cheese = CheeseForm()
        return air.Form(cheese.render())

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == '<form><fieldset><label>name<input name="name" type="text" id="name"></input></label><label>age<input name="age" type="number" id="age"></input></label></fieldset></form>'
    )


def test_form_render_with_errors():
    class CheeseModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        age: int  # type: ignore [annotation-unchecked]

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm()

    # render without validation
    html = cheese.render()
    assert "Please correct this error." not in html

    # render with validation
    cheese.validate({})
    html = cheese.render()

    assert "Please correct this error." in html

    assert (
        html
        == '<fieldset><label>name<input name="name" type="text" id="name" aria-invalid="true"></input><small id="name-error">Please correct this error.</small></label><label>age<input name="age" type="number" id="age" aria-invalid="true"></input><small id="age-error">Please correct this error.</small></label></fieldset>'
    )


def test_html_input_field_types():
    class ContactModel(BaseModel):
        name: str  # type: ignore [annotation-unchecked]
        email: str = Field(json_schema_extra={"email": True})  # type: ignore [annotation-unchecked]
        date_and_time: str = Field(json_schema_extra={"datedatetime-local": True})  # type: ignore [annotation-unchecked]

    class ContactForm(air.AirForm):
        model = ContactModel

    contact_form = ContactForm()
    html = contact_form.render()
    assert 'type="datedatetime-local"' in html
    assert 'type="email"' in html
