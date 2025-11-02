from typing import Annotated, cast

import annotated_types
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
            "url": "https://errors.pydantic.dev/2.12/v/int_parsing",
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
        form == '<label for="name">name</label><input name="name" type="text" required id="name">'
        '<label for="age">age</label><input name="age" type="number" required id="age">'
    )


def test_form_render_with_values() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(air.AirForm):
        model = CheeseModel

    cheese = CheeseForm({"name": "Cheddar", "age": 3})

    assert (
        cheese.render()
        == '<label for="name">name</label><input name="name" type="text" value="Cheddar" required id="name">'
        '<label for="age">age</label><input name="age" type="number" value="3" required id="age">'
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
        response.text == '<form><label for="name">name</label><input name="name" type="text" required id="name">'
        '<label for="age">age</label><input name="age" type="number" required id="age"></form>'
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
        html == '<label for="name">name</label><input aria-invalid="true" name="name" type="text" required id="name">'
        '<small id="name-error">This field is required.</small><label for="age">age</label>'
        '<input aria-invalid="true" name="age" type="number" required id="age">'
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
        html == '<label for="name">name</label><input name="name" type="text" required id="name">'
        '<label for="email">Email</label><input name="email" type="email" required id="email">'
        '<label for="date_and_time">Date and Time</label>'
        '<input name="date_and_time" type="datedatetime-local" required id="date_and_time">'
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
            "url": "https://errors.pydantic.dev/2.12/v/missing",
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
    assert '<input name="name" type="text" required autofocus id="name">' in html
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
    assert '<label for="id">id</label><input name="id" type="number" required id="id">' in html

    # Test with includes active, removing id field
    class PlaneForm(air.AirForm):
        model = PlaneModel
        includes = ("name", "year_released", "max_airspeed")

    html = PlaneForm().render()
    assert '<label for="id">id</label><input name="id" type="number" required id="id">' not in html


def test_default_form_widget_basic():
    """
    Test that the default form widget is applied correctly to all fields in a form.
    """

    class TestModel(BaseModel):
        name: str
        age: int

    html = air.forms.default_form_widget(TestModel)
    # Check that the generated HTML contains the expected input fields
    assert '<label for="name">name</label>' in html
    assert '<input name="name" type="text" required id="name"' in html
    assert '<label for="age">age</label>' in html
    assert '<input name="age" type="number" required id="age"' in html

    # Check no errors and invalid states
    assert 'aria-invalid="true"' not in html
    assert "<small" not in html


def test_default_form_widget_with_data():
    """
    Test form widget with pre-populated data.
    """

    class TestModel(BaseModel):
        name: str
        age: int

    data = {"name": "John", "age": 27}
    html = air.forms.default_form_widget(TestModel, data=data)
    assert 'value="John"' in html
    assert 'value="27"' in html


def test_default_form_widget_with_errors():
    """
    Test form widget rendering with validation errors.
    """

    class TestModel(BaseModel):
        name: str
        age: int

    errors = [
        {"type": "missing", "loc": ("name",), "msg": "Field required"},
        {"type": "int_parsing", "loc": ("age",), "msg": "Invalid integer"},
    ]

    html = air.forms.default_form_widget(TestModel, errors=errors)
    # check for invalid states
    assert 'aria-invalid="true"' in html
    # check for error messages
    assert "This field is required." in html
    assert "Please enter a valid number." in html


def test_default_form_widget_bool_field():
    """Test form widget with boolean field."""

    class TestModel(BaseModel):
        active: bool

    html = air.forms.default_form_widget(TestModel)
    assert 'type="checkbox"' in html


def test_default_form_widget_includes():
    """Test form widget with includes."""

    class TestModel(BaseModel):
        id: int
        name: str
        age: int

    html = air.forms.default_form_widget(TestModel, includes=("name", "age"))
    # Ensure excluded fields are not present
    assert '<label for="id">' not in html
    assert '<input name="id"' not in html

    # Ensure included fields are present
    assert '<label for="name">name</label>' in html
    assert '<input name="name" type="text" required id="name">' in html
    assert '<label for="age">age</label>' in html
    assert '<input name="age" type="number" required id="age">' in html


def test_default_form_widget_optional_fields():
    """Test form widget with optional fields."""

    class AnotherInterestingTestModel(BaseModel):
        name: str | None

    html = air.forms.default_form_widget(AnotherInterestingTestModel)
    # Ensure fields are present but not marked as required
    assert '<label for="name">name</label>' in html
    assert '<input name="name" type="text" id="name">' in html
    assert "required" not in html


def test_default_form_widget_custom_label():
    """Test form widget with custom label via json_schema_extra."""

    class CustomLabelTestModel(BaseModel):
        name: str = Field(json_schema_extra={"label": "Full Name"})

    html = air.forms.default_form_widget(CustomLabelTestModel)
    assert '<label for="name">Full Name</label>' in html


def test_default_form_widget_autofocus():
    """Test form widget with autofocus attribute via json_schema_extra."""

    class AutofocusTestModel(BaseModel):
        name: str = Field(json_schema_extra={"autofocus": True})

    html = air.forms.default_form_widget(AutofocusTestModel)
    assert "autofocus" in html


def test_air_field_with_extra_kwargs() -> None:
    """Test AirField with extra keyword arguments."""

    class TestModel(BaseModel):
        name: str = air.AirField(label="Name", custom_attr="custom_value")

    # Verify the field was created successfully with extra kwargs
    assert TestModel.model_fields["name"].json_schema_extra == {
        "label": "Name",
        "custom_attr": "custom_value",
    }


def test_air_field_with_default_factory() -> None:
    """Test AirField with default_factory parameter."""

    def name_factory() -> str:
        return "default_name"

    class TestModel(BaseModel):
        name: str = air.AirField(default_factory=name_factory, label="Name")

    # Verify the default_factory works
    instance = TestModel()
    assert instance.name == "default_name"


def test_air_field_with_default_value() -> None:
    """Test AirField with default value parameter."""

    class TestModel(BaseModel):
        name: str = air.AirField("default_name", label="Name")
        age: int = air.AirField(25, ge=0, le=150)

    # Verify the default values work
    instance = TestModel()
    assert instance.name == "default_name"
    assert instance.age == 25


def test_html5_validation_attributes() -> None:
    """Test that HTML5 validation attributes are generated from Pydantic constraints."""

    class ContactModel(BaseModel):
        name: str = air.AirField(min_length=2, max_length=50)
        email: str = air.AirField(type="email", label="Email Address")
        message: str = air.AirField(min_length=10, max_length=500)

    class ContactForm(air.AirForm):
        model = ContactModel

    html = ContactForm().render()

    # Check minlength and maxlength attributes
    assert 'minlength="2"' in html
    assert 'maxlength="50"' in html
    assert 'minlength="10"' in html
    assert 'maxlength="500"' in html

    # Check required attribute (all fields are required since they don't have defaults)
    assert html.count("required") == 3

    # Check email type is preserved
    assert 'type="email"' in html


def test_html5_validation_optional_fields() -> None:
    """Test that optional fields don't get required attribute."""

    class OptionalModel(BaseModel):
        name: str
        nickname: str | None = None

    class OptionalForm(air.AirForm):
        model = OptionalModel

    html = OptionalForm().render()

    # Only the name field should have required attribute
    assert 'name="name"' in html and "required" in html
    assert 'name="nickname"' in html and '<input name="nickname" type="text" id="nickname">' in html


def test_html5_validation_with_standard_field() -> None:
    """Test HTML5 validation with standard Pydantic Field (not AirField)."""

    class StandardModel(BaseModel):
        name: str = Field(min_length=3, max_length=20)
        age: int

    class StandardForm(air.AirForm):
        model = StandardModel

    html = StandardForm().render()

    # Check that constraints from standard Field are also applied
    assert 'minlength="3"' in html
    assert 'maxlength="20"' in html
    assert html.count("required") == 2  # Both fields required


def test_html5_validation_with_annotated() -> None:
    """Test HTML5 validation with Annotated type constraints."""

    class AnnotatedModel(BaseModel):
        name: Annotated[str, annotated_types.MinLen(2), annotated_types.MaxLen(50)]
        age: int

    class AnnotatedForm(air.AirForm):
        model = AnnotatedModel

    html = AnnotatedForm().render()

    # Check that Annotated constraints are applied
    assert 'minlength="2"' in html
    assert 'maxlength="50"' in html


def test_html5_validation_optional_with_constraints() -> None:
    """Test that optional fields with constraints get minlength/maxlength but not required."""

    class OptionalConstrainedModel(BaseModel):
        nickname: Annotated[str | None, annotated_types.MinLen(2)] = None

    class OptionalConstrainedForm(air.AirForm):
        model = OptionalConstrainedModel

    html = OptionalConstrainedForm().render()

    # Should have minlength but not required
    assert 'minlength="2"' in html
    assert "required" not in html


def test_html5_validation_field_with_default() -> None:
    """Test that fields with defaults don't get required attribute."""

    class DefaultedModel(BaseModel):
        name: str = Field("default_name", min_length=2, max_length=20)
        age: int = 25

    class DefaultedForm(air.AirForm):
        model = DefaultedModel

    html = DefaultedForm().render()

    # Should have minlength/maxlength but not required
    assert 'minlength="2"' in html
    assert 'maxlength="20"' in html
    assert "required" not in html
