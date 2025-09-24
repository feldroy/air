from typing import Annotated, cast

import pytest
from fastapi import Depends, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

import air


def test_form_sync_check() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

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
        },
    ]


def test_form_validation_dependency_injection() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(
        cheese: Annotated[CheeseForm, Depends(CheeseForm.from_request)],
    ):
        if cheese.is_valid:
            data = cast(CheeseModel, cheese.data)
            return air.Html(air.H1(data.name))
        assert cheese.errors is not None
        return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))

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


def test_form_validation_in_view() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(request: Request):
        cheese = await CheeseForm.from_request(request)
        if cheese.is_valid:
            data = cast(CheeseModel, cheese.data)
            return air.Html(air.H1(data.name))
        assert cheese.errors is not None
        return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))

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


def test_form_render() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm()

    form = cheese.render()
    assert (
        form == '<label for="name">name</label><input name="name" type="text" id="name" />'
        '<label for="age">age</label><input name="age" type="number" id="age" />'
    )


def test_form_render_with_values() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm({"name": "Cheddar", "age": 3})

    assert (
        cheese.render() == '<label for="name">name</label><input name="name" type="text" value="Cheddar" id="name" />'
        '<label for="age">age</label><input name="age" type="number" value="3" id="age" />'
    )


def test_form_render_in_view() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

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
        response.text == '<form><label for="name">name</label><input name="name" type="text" id="name" />'
        '<label for="age">age</label><input name="age" type="number" id="age" /></form>'
    )


def test_form_render_with_errors() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm()

    # render without validation
    html = cheese.render()
    assert "Please correct this error." not in html

    # render with validation
    cheese.validate({})
    html = cheese.render()

    assert (
        html == '<label for="name">name</label><input aria-invalid="true" name="name" type="text" id="name" />'
        '<small id="name-error">This field is required.</small><label for="age">age</label>'
        '<input aria-invalid="true" name="age" type="number" id="age" />'
        '<small id="age-error">This field is required.</small>'
    )


def test_html_input_field_types() -> None:
    class ContactModel(BaseModel):
        name: str
        email: str | None = Field(json_schema_extra={"email": True})
        date_and_time: str = Field(json_schema_extra={"datedatetime-local": True})

    class ContactForm(air.AirForm):
        model = ContactModel

    contact_form = ContactForm()
    html = contact_form.render()
    assert 'type="datedatetime-local"' in html
    assert 'type="email"' in html


def test_air_field() -> None:
    class ContactModel(BaseModel):
        name: str
        email: str = air.AirField(type="email", label="Email")
        date_and_time: str = air.AirField(type="datedatetime-local", label="Date and Time")

    class ContactForm(air.AirForm):
        model = ContactModel

    contact_form = ContactForm()
    html = contact_form.render()
    assert (
        html == '<label for="name">name</label><input name="name" type="text" id="name" />'
        '<label for="email">Email</label><input name="email" type="email" id="email" />'
        '<label for="date_and_time">Date and Time</label>'
        '<input name="date_and_time" type="datedatetime-local" id="date_and_time" />'
    )


def test_airform_notimplementederror() -> None:
    with pytest.raises(NotImplementedError) as exc:
        air.AirForm()

    assert "model" in str(exc.value)


def test_airform_validate() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese_form = CheeseForm()
    assert not cheese_form.is_valid
    cheese_form.validate({})
    assert not cheese_form.is_valid
    cheese_form.validate({"name": "Cheddar"})
    assert not cheese_form.is_valid
    cheese_form.validate({"name": "Cheddar", "age": 5})
    assert cheese_form.is_valid
    assert cheese_form.errors == [
        {
            "type": "missing",
            "loc": ("age",),
            "msg": "Field required",
            "input": {"name": "Cheddar"},
            "url": "https://errors.pydantic.dev/2.11/v/missing",
        },
    ]


def test_airform_autofocus() -> None:
    class CheeseModel(BaseModel):
        name: str = air.AirField(label="Name", autofocus=True)
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    html = CheeseForm().render()
    assert "autofocus" in html


def test_air_field_json_schema_extra() -> None:
    class CheeseModel(BaseModel):
        name: str = air.AirField(json_schema_extra={"autofocus": True})
        age: int = air.AirField(json_schema_extra={"label": "my-age"})

    class CheeseForm(air.AirForm):
        model = CheeseModel

    html = CheeseForm().render()
    assert '<input name="name" type="text" autofocus id="name" />' in html
    assert '<label for="age">my-age</label>' in html


def test_field_includes() -> None:
    class PlaneModel(BaseModel):
        id: int
        name: str
        year_released: int
        max_airspeed: str

    # Control test - make sure existing system still works
    class PlaneForm(air.AirForm):
        model = PlaneModel

    html = PlaneForm().render()
    assert '<label for="id">id</label><input name="id" type="number" id="id" />' in html

    # Test with includes active, removing id field
    class PlaneForm(air.AirForm):
        model = PlaneModel
        includes = ("name", "year_released", "max_airspeed")

    html = PlaneForm().render()
    assert '<label for="id">id</label><input name="id" type="number" id="id" />' not in html
