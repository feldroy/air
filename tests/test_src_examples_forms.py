import pytest
from src_examples.forms__AirForm__example import FlightForm, FlightModel

from air.forms import default_form_widget, pydantic_type_to_html_type


def test_airfield_json_schema_extra_and_type_mapping():
    # Check that AirField() added json_schema_extra keys
    field_info = FlightModel.model_fields["flight_number"]
    assert field_info.json_schema_extra.get("label") == "Flight Number"
    assert field_info.json_schema_extra.get("autofocus") is True

    # int field should map to number
    seats_info = FlightModel.model_fields["seats"]
    assert pydantic_type_to_html_type(seats_info) == "number"


def test_default_form_widget_renders_inputs():
    html = default_form_widget(model=FlightModel, data={"flight_number": "AA123", "seats": 5}, errors=None)
    # inputs for field names should be present
    assert 'name="flight_number"' in html or "name='flight_number'" in html
    assert 'name="seats"' in html or "name='seats'" in html


def test_airform_validate_and_render():
    f = FlightForm(initial_data={"flight_number": "BB456", "seats": 2})
    ok = f.validate({"flight_number": "BB456", "seats": 2})
    assert ok is True
    assert f.is_valid is True
    # rendered HTML should include provided values
    rendered = f.render()
    assert "BB456" in str(rendered)


@pytest.mark.asyncio
async def test_airform_from_request_async():
    class DummyRequest:
        async def form(self):
            return {"flight_number": "CC789", "seats": 3}

    inst = await FlightForm.from_request(DummyRequest())
    assert inst.is_valid is True
    assert inst.data.flight_number == "CC789"
