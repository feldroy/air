"""Tests for air.form: validation, error handling, and rendering.

Validation tests extracted from air/tests/test_forms.py. Rendering
tests exercise the full AirField metadata vocabulary that Daniel's
original default_form_widget didn't yet support.
"""

import re
from typing import Annotated

import annotated_types
import pytest
from pydantic import BaseModel, Field
from starlette.datastructures import FormData

from air.field import AirField
from air.form import (
    AirForm,
    SafeHTML,
    default_form_widget,
    errors_to_dict,
    get_user_error_message,
    pydantic_type_to_html_type,
)

# ── Validation tests (from Air) ─────────────────────────────────────


def test_form_sync_check() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm):
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


def test_airform_notimplementederror() -> None:
    with pytest.raises(NotImplementedError) as exc:
        AirForm()
    assert "model" in str(exc.value)


def test_airform_validate() -> None:
    class KareKareModel(BaseModel):
        name: str
        servings: int

    class KareKareForm(AirForm):
        model = KareKareModel

    form = KareKareForm()
    assert not form.is_valid
    form.validate({})
    assert not form.is_valid
    form.validate({"name": "Kare-Kare"})
    assert not form.is_valid
    form.validate({"name": "Kare-Kare", "servings": 4})
    assert form.is_valid
    assert form.errors is None


def test_airform_validate_accepts_mapping() -> None:
    """validate() accepts any Mapping, not just dict (e.g. Starlette FormData)."""

    class KareKareModel(BaseModel):
        name: str
        servings: int

    class KareKareForm(AirForm):
        model = KareKareModel

    form = KareKareForm()
    form_data = FormData({"name": "Kare-Kare", "servings": "4"})
    form.validate(form_data)
    assert form.is_valid
    assert form.data.name == "Kare-Kare"


def test_airform_generic_validates() -> None:
    class AutoModel(BaseModel):
        name: str
        age: int

    class AutoForm(AirForm[AutoModel]):
        pass

    form = AutoForm()
    form.validate({"name": "Test", "age": 3})
    assert form.is_valid is True


def test_airform_generic_type_parameter() -> None:
    class JeepneyRouteModel(BaseModel):
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


def test_airform_data_before_validation_raises() -> None:
    class IslandModel(BaseModel):
        name: str

    class IslandForm(AirForm[IslandModel]):
        pass

    form = IslandForm()
    with pytest.raises(AttributeError, match="No validated data"):
        form.data  # noqa: B018


def test_airform_data_after_failed_validation_raises() -> None:
    class IslandModel(BaseModel):
        name: str

    class IslandForm(AirForm[IslandModel]):
        pass

    form = IslandForm()
    form.validate({})
    assert not form.is_valid
    with pytest.raises(AttributeError, match="No validated data"):
        form.data  # noqa: B018


def test_airform_explicit_model_not_overridden() -> None:
    class ModelA(BaseModel):
        x: str

    class ModelB(BaseModel):
        y: str

    class ExplicitForm(AirForm[ModelA]):
        model = ModelB

    assert ExplicitForm.model is ModelB


def test_airform_revalidation_resets_state() -> None:
    class SariSariModel(BaseModel):
        item: str
        price: int

    class SariSariForm(AirForm[SariSariModel]):
        pass

    form = SariSariForm()
    form.validate({"item": "Chicharon", "price": 25})
    assert form.is_valid
    assert form.data.item == "Chicharon"

    form.validate({})
    assert not form.is_valid
    with pytest.raises(AttributeError, match="No validated data"):
        form.data  # noqa: B018


def test_airform_multi_level_inheritance() -> None:
    class BarangayModel(BaseModel):
        name: str
        captain: str

    class BaseBarangayForm(AirForm[BarangayModel]):
        pass

    class SpecificBarangayForm(BaseBarangayForm):
        pass

    assert SpecificBarangayForm.model is BarangayModel
    form = SpecificBarangayForm()
    form.validate({"name": "San Antonio", "captain": "Kap. Reyes"})
    assert form.is_valid
    assert form.data.captain == "Kap. Reyes"


def test_airform_generic_data_access() -> None:
    class PalengkeModel(BaseModel):
        vendor: str
        stall_number: int

    class PalengkeForm(AirForm[PalengkeModel]):
        pass

    form = PalengkeForm()
    form.validate({"vendor": "Aling Nena", "stall_number": 42})
    assert form.is_valid
    assert form.data.vendor == "Aling Nena"
    assert form.data.stall_number == 42


# ── Helper function tests ───────────────────────────────────────────


def test_get_user_error_message() -> None:
    assert get_user_error_message({"type": "missing"}) == "This field is required."
    assert get_user_error_message({"type": "int_parsing"}) == "Please enter a valid number."
    assert get_user_error_message({"type": "unknown", "msg": "Some error"}) == "Some error"
    assert get_user_error_message({"type": "unknown"}) == "Please correct this error."


def test_errors_to_dict() -> None:
    errors = [
        {"type": "missing", "loc": ("name",), "msg": "Field required"},
        {"type": "int_parsing", "loc": ("age",), "msg": "Invalid integer"},
    ]
    result = errors_to_dict(errors)
    assert "name" in result
    assert "age" in result
    assert result["name"]["type"] == "missing"


def test_errors_to_dict_none() -> None:
    assert errors_to_dict(None) == {}


def test_pydantic_type_to_html_type() -> None:
    class TestModel(BaseModel):
        name: str
        age: int
        score: float
        active: bool

    assert pydantic_type_to_html_type(TestModel.model_fields["name"]) == "text"
    assert pydantic_type_to_html_type(TestModel.model_fields["age"]) == "number"
    assert pydantic_type_to_html_type(TestModel.model_fields["score"]) == "number"
    assert pydantic_type_to_html_type(TestModel.model_fields["active"]) == "checkbox"


def test_pydantic_type_to_html_type_semantic_widgets() -> None:
    """Semantic widget names map to valid HTML input types."""

    class WidgetModel(BaseModel):
        on_off: bool = AirField(widget="toggle")
        intensity: int = AirField(widget="slider")
        mobile: str = AirField(widget="phone")
        price: float = AirField(widget="currency")
        query: str = AirField(widget="search")
        notes: str = AirField(widget="rich_text")
        source: str = AirField(widget="code")

    assert pydantic_type_to_html_type(WidgetModel.model_fields["on_off"]) == "checkbox"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["intensity"]) == "range"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["mobile"]) == "tel"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["price"]) == "number"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["query"]) == "search"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["notes"]) == "textarea"
    assert pydantic_type_to_html_type(WidgetModel.model_fields["source"]) == "textarea"


def test_pydantic_type_to_html_type_unknown_widget_passes_through() -> None:
    """Unknown widget kinds pass through as-is (e.g. valid HTML types like 'date')."""

    class DateModel(BaseModel):
        birthday: str = AirField(type="date")

    assert pydantic_type_to_html_type(DateModel.model_fields["birthday"]) == "date"


# ── Render tests: Daniel's pattern + full AirField vocabulary ────────


def test_render_blank_form() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm[CheeseModel]):
        pass

    html = CheeseForm().render()
    assert '<label for="name">' in html
    assert "<input" in html
    assert 'name="name"' in html
    assert 'name="age"' in html
    assert 'type="number"' in html
    assert "required" in html


def test_render_with_initial_data() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm[CheeseModel]):
        pass

    html = CheeseForm({"name": "Cheddar", "age": 3}).render()
    assert 'value="Cheddar"' in html
    assert 'value="3"' in html


def test_render_preserves_submitted_data_on_error() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm[CheeseModel]):
        pass

    form = CheeseForm()
    form.validate({"name": "Brie", "age": "not-a-number"})
    assert not form.is_valid
    html = form.render()
    assert 'value="Brie"' in html
    assert 'aria-invalid="true"' in html
    assert "air-field-error" in html
    assert 'role="alert"' in html


def test_render_with_errors_shows_messages() -> None:
    class CheeseModel(BaseModel):
        name: str
        age: int

    class CheeseForm(AirForm[CheeseModel]):
        pass

    form = CheeseForm()
    form.validate({})
    html = form.render()
    assert "This field is required." in html


def test_render_airfield_label() -> None:
    """Labels from AirField metadata appear in rendered HTML."""

    class CompanionModel(BaseModel):
        name: str = AirField(label="Companion Name")
        role: str = AirField(type="email", label="Missive Address")

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert "Companion Name" in html
    assert "Missive Address" in html
    assert 'type="email"' in html


def test_render_airfield_placeholder() -> None:
    class CompanionModel(BaseModel):
        name: str = AirField(placeholder="e.g. Konstantina")

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert 'placeholder="e.g. Konstantina"' in html


def test_render_airfield_help_text() -> None:
    class QuestModel(BaseModel):
        objective: str = AirField(
            widget="textarea",
            help_text="Be specific. 'Slay the dragon' is not a plan.",
        )

    class QuestForm(AirForm[QuestModel]):
        pass

    html = QuestForm().render()
    assert "<textarea" in html
    assert "air-field-help" in html
    assert "Be specific." in html


def test_render_airfield_choices() -> None:
    class CompanionModel(BaseModel):
        role: str = AirField(
            label="Party Role",
            choices=[
                ("tank", "The One Who Gets Hit"),
                ("healer", "The One Who Complains"),
                ("dps", "The One Who Takes Credit"),
                ("bard", "The One With Snacks"),
            ],
        )

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert "<select" in html
    assert '<option value="tank">The One Who Gets Hit</option>' in html
    assert '<option value="bard">The One With Snacks</option>' in html
    assert "Select...</option>" in html


def test_render_airfield_choices_with_selected() -> None:
    class CompanionModel(BaseModel):
        role: str = AirField(
            choices=[
                ("tank", "The One Who Gets Hit"),
                ("healer", "The One Who Complains"),
                ("dps", "The One Who Takes Credit"),
            ],
        )

    html = default_form_widget(model=CompanionModel, data={"role": "healer"})
    assert 'value="healer" selected' in html


def test_render_airfield_autofocus() -> None:
    class CompanionModel(BaseModel):
        name: str = AirField(label="Name", autofocus=True)

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert "autofocus" in html


def test_render_airfield_primary_key_skipped() -> None:
    class CompanionModel(BaseModel):
        id: int | None = AirField(default=None, primary_key=True)
        name: str

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert 'name="id"' not in html
    assert 'name="name"' in html


def test_render_airfield_textarea() -> None:
    class QuestModel(BaseModel):
        backstory: str = AirField(widget="textarea", placeholder="It all started in a tavern...")

    class QuestForm(AirForm[QuestModel]):
        pass

    html = QuestForm().render()
    assert "<textarea" in html
    assert 'placeholder="It all started in a tavern..."' in html


def test_render_airfield_textarea_with_value() -> None:
    class QuestModel(BaseModel):
        backstory: str = AirField(widget="textarea")

    html = default_form_widget(model=QuestModel, data={"backstory": "The wizard was late, as usual."})
    assert ">The wizard was late, as usual.</textarea>" in html


def test_render_checkbox() -> None:
    class WaiverModel(BaseModel):
        accepted: bool = AirField(default=False, label="I understand the dragon may eat me")

    class WaiverForm(AirForm[WaiverModel]):
        pass

    html = WaiverForm().render()
    assert 'type="checkbox"' in html
    # Label comes after input for checkboxes
    input_pos = html.index("<input")
    label_pos = html.index("<label")
    assert input_pos < label_pos


def test_render_checkbox_checked_when_true() -> None:
    """Checkbox renders with 'checked' attribute when value is True."""

    class WaiverModel(BaseModel):
        accepted: bool = AirField(default=False, label="Accept terms")

    html = default_form_widget(model=WaiverModel, data={"accepted": True})
    assert "checked" in html
    assert 'value="True"' not in html  # uses checked, not value


def test_render_checkbox_unchecked_when_false() -> None:
    """Checkbox renders without 'checked' when value is False."""

    class WaiverModel(BaseModel):
        accepted: bool = AirField(default=False, label="Accept terms")

    html = default_form_widget(model=WaiverModel, data={"accepted": False})
    assert "checked" not in html


def test_render_toggle_widget_as_checkbox() -> None:
    """widget='toggle' renders as a checkbox input."""

    class SettingsModel(BaseModel):
        is_public: bool = AirField(default=True, widget="toggle", label="Public")

    class SettingsForm(AirForm[SettingsModel]):
        pass

    html = SettingsForm().render()
    assert 'type="checkbox"' in html
    # Label after input (checkbox behavior)
    input_pos = html.index("<input")
    label_pos = html.index("<label")
    assert input_pos < label_pos


def test_validate_unchecked_checkbox_is_false() -> None:
    """Unchecked checkboxes send nothing; missing bool fields become False."""

    class WaiverModel(BaseModel):
        name: str
        accepted: bool = AirField(default=True)

    class WaiverForm(AirForm[WaiverModel]):
        pass

    form = WaiverForm()
    # HTML checkbox omits the field entirely when unchecked
    form.validate({"name": "Audrey"})
    assert form.is_valid
    assert form.data.accepted is False


def test_validate_checked_checkbox_is_true() -> None:
    """Checked checkboxes send 'on'; Pydantic coerces to True."""

    class WaiverModel(BaseModel):
        name: str
        accepted: bool = AirField(default=False)

    class WaiverForm(AirForm[WaiverModel]):
        pass

    form = WaiverForm()
    form.validate({"name": "Audrey", "accepted": "on"})
    assert form.is_valid
    assert form.data.accepted is True


def test_render_optional_not_required() -> None:
    class CompanionModel(BaseModel):
        catchphrase: str | None = None

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert "required" not in html


def test_render_min_max_length() -> None:
    class CompanionModel(BaseModel):
        name: str = AirField(min_length=2, max_length=50)

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert 'minlength="2"' in html
    assert 'maxlength="50"' in html


def test_render_annotated_constraints() -> None:
    class CompanionModel(BaseModel):
        name: Annotated[str, annotated_types.MinLen(2), annotated_types.MaxLen(50)]

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert 'minlength="2"' in html
    assert 'maxlength="50"' in html


def test_render_standard_field_constraints() -> None:
    class CompanionModel(BaseModel):
        name: str = Field(min_length=3, max_length=20)

    class CompanionForm(AirForm[CompanionModel]):
        pass

    html = CompanionForm().render()
    assert 'minlength="3"' in html
    assert 'maxlength="20"' in html


def test_custom_widget_swap() -> None:
    """Swappable widget pattern: replace the renderer."""

    class CompanionModel(BaseModel):
        name: str
        role: str

    def tavern_widget(
        *, model: type, data: dict | None = None, errors: list | None = None, excludes: set | None = None
    ) -> str:
        return "<p>Fill this out or the barkeep gets cross.</p>"

    class CompanionForm(AirForm[CompanionModel]):
        widget = staticmethod(tavern_widget)

    html = CompanionForm().render()
    assert "<p>Fill this out or the barkeep gets cross.</p>" in html
    assert 'name="csrf_token"' in html  # CSRF token still included


# ── Empty string vs. too-short error message tests (pottery/ceramics) ──


@pytest.mark.parametrize(
    ("input_value", "expected_message"),
    [
        pytest.param("", "This field is required.", id="empty-string-means-required"),
        pytest.param("a", "This value is too short.", id="too-short-stays-too-short"),
    ],
)
def test_get_user_error_message_string_too_short(input_value: str, expected_message: str) -> None:
    """Empty string + string_too_short should say 'required', not 'too short'."""
    error = {
        "type": "string_too_short",
        "loc": ("glaze_name",),
        "msg": "String should have at least 2 characters",
        "input": input_value,
        "ctx": {"min_length": 2},
    }
    assert get_user_error_message(error) == expected_message


def test_get_user_error_message_missing_field() -> None:
    """A completely missing field still says 'required' (existing behavior)."""
    error = {
        "type": "missing",
        "loc": ("kiln_temp",),
        "msg": "Field required",
        "input": {},
    }
    assert get_user_error_message(error) == "This field is required."


def test_render_empty_string_min_length_shows_required() -> None:
    """Submitting an empty string to a min_length field should render 'required' message."""

    class StonewareModel(BaseModel):
        glaze_name: str = AirField(min_length=2)

    class StonewareForm(AirForm[StonewareModel]):
        pass

    form = StonewareForm()
    form.validate({"glaze_name": ""})
    assert not form.is_valid
    html = form.render()
    assert "This field is required." in html
    assert "This value is too short." not in html


# ── CSRF tests (polymer clay jewelry making) ────────────────────────


def test_render_includes_csrf_token() -> None:
    """Every rendered form gets a CSRF hidden input automatically."""

    class EarringModel(BaseModel):
        clay_color: str
        shape: str

    class EarringForm(AirForm[EarringModel]):
        pass

    html = EarringForm().render()
    assert 'type="hidden"' in html
    assert 'name="csrf_token"' in html


def test_validate_without_render_skips_csrf() -> None:
    """Direct validate() without render() skips CSRF (programmatic use)."""

    class EarringModel(BaseModel):
        clay_color: str

    class EarringForm(AirForm[EarringModel]):
        pass

    form = EarringForm()
    form.validate({"clay_color": "terracotta"})
    assert form.is_valid
    assert form.data.clay_color == "terracotta"


def test_render_then_validate_enforces_csrf() -> None:
    """After render(), validate() requires a valid CSRF token."""

    class EarringModel(BaseModel):
        clay_color: str
        shape: str = "teardrop"

    class EarringForm(AirForm[EarringModel]):
        pass

    form = EarringForm()
    html = form.render()

    # Extract the token from the rendered HTML
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match
    token = match.group(1)

    # Submit with the rendered token
    form.validate({"clay_color": "sage green", "shape": "arch", "csrf_token": token})
    assert form.is_valid
    assert form.data.clay_color == "sage green"
    assert form.data.shape == "arch"


def test_render_then_validate_rejects_missing_csrf() -> None:
    """After render(), submitting without a CSRF token fails."""

    class PendantModel(BaseModel):
        design: str

    class PendantForm(AirForm[PendantModel]):
        pass

    form = PendantForm()
    form.render()  # sets _csrf_token
    form.validate({"design": "botanical press"})
    assert not form.is_valid


def test_render_then_validate_rejects_bad_csrf() -> None:
    """After render(), a tampered CSRF token fails validation."""

    class PendantModel(BaseModel):
        design: str

    class PendantForm(AirForm[PendantModel]):
        pass

    form = PendantForm()
    form.render()
    form.validate({"design": "botanical press", "csrf_token": "fake:token:value"})
    assert not form.is_valid


def test_csrf_token_not_on_validated_data() -> None:
    """The CSRF field doesn't leak into form.data."""

    class BraceletModel(BaseModel):
        bead_count: int
        pattern: str = "alternating"

    class BraceletForm(AirForm[BraceletModel]):
        pass

    form = BraceletForm()
    html = form.render()
    match = re.search(r'value="([^"]+)"', html)
    assert match
    token = match.group(1)

    form.validate({"bead_count": "12", "pattern": "gradient", "csrf_token": token})
    assert form.is_valid
    assert form.data.bead_count == 12
    assert not hasattr(form.data, "csrf_token")


def test_csrf_token_excluded_from_field_rendering() -> None:
    """The CSRF token is a hidden input, not a visible form field."""

    class RingModel(BaseModel):
        band_width: str = AirField(label="Band Width")
        stone: str = AirField(label="Stone Type")

    class RingForm(AirForm[RingModel]):
        pass

    html = RingForm().render()
    # CSRF token rendered as hidden input
    assert 'name="csrf_token"' in html
    assert 'type="hidden"' in html
    # Not rendered as a labeled field with air-field wrapper
    assert '<label for="csrf_token">' not in html
    assert 'class="air-field"' not in html.split('name="csrf_token"')[0]
    # User fields are rendered normally
    assert "Band Width" in html
    assert "Stone Type" in html


# ── SafeHTML / __html__ protocol tests ───────────────────────────────


def test_render_returns_safe_html() -> None:
    """render() returns a SafeHTML instance, not a plain str."""

    class GlazeModel(BaseModel):
        color: str

    class GlazeForm(AirForm[GlazeModel]):
        pass

    result = GlazeForm().render()
    assert isinstance(result, SafeHTML)
    assert isinstance(result, str)
    assert hasattr(result, "__html__")
    assert callable(result.__html__)
    assert result.__html__() == str(result)  # noqa: PLC2801


def test_safe_html_preserves_content() -> None:
    """SafeHTML behaves like a str for all practical purposes."""

    class GlazeModel(BaseModel):
        color: str = AirField(label="Glaze Color")

    class GlazeForm(AirForm[GlazeModel]):
        pass

    html = GlazeForm().render()
    assert "Glaze Color" in html
    assert '<label for="color">' in html
    # String operations work
    assert html.count("air-field") >= 1


# ── Excludes tests (woodworking) ─────────────────────────────────────


def test_excludes_bare_string_excludes_from_display_and_save() -> None:
    """A bare string in excludes hides the field from rendering and from save data."""

    class WorkbenchModel(BaseModel):
        wood_type: str
        length: int
        created_at: str = AirField(default="2026-01-01")

    class WorkbenchForm(AirForm[WorkbenchModel]):
        excludes = ("created_at",)

    # Display: created_at not rendered
    html = WorkbenchForm().render()
    assert "wood_type" in html
    assert "length" in html
    assert "created_at" not in html

    # Save: created_at not in save_data
    form = WorkbenchForm()
    form.validate({"wood_type": "oak", "length": "72"})
    assert form.is_valid
    assert form.data.wood_type == "oak"
    assert "created_at" not in form.save_data()


def test_excludes_tuple_display_only() -> None:
    """A ('field', 'display') tuple hides the field from rendering but keeps it in save_data."""

    class WorkbenchModel(BaseModel):
        wood_type: str
        finish: str = AirField(default="natural")

    class WorkbenchForm(AirForm[WorkbenchModel]):
        excludes = (("finish", "display"),)

    # Display: finish not rendered
    html = WorkbenchForm().render()
    assert "wood_type" in html
    assert "finish" not in html

    # Save: finish is in save_data (only display-excluded, not save-excluded)
    form = WorkbenchForm()
    form.validate({"wood_type": "walnut", "finish": "lacquer"})
    assert form.is_valid
    assert form.data.finish == "lacquer"
    assert "finish" in form.save_data()


def test_excludes_tuple_save_only() -> None:
    """A ('field', 'save') tuple renders the field but strips it from save_data."""

    class WorkbenchModel(BaseModel):
        wood_type: str
        internal_notes: str = AirField(default="")

    class WorkbenchForm(AirForm[WorkbenchModel]):
        excludes = (("internal_notes", "save"),)

    # Display: internal_notes is rendered
    html = WorkbenchForm().render()
    assert "internal_notes" in html

    # Save: internal_notes still on form.data but excluded from save_data
    form = WorkbenchForm()
    form.validate({"wood_type": "maple", "internal_notes": "check grain"})
    assert form.is_valid
    assert form.data.internal_notes == "check grain"
    assert "internal_notes" not in form.save_data()


def test_excludes_primary_key_default_display_exclude() -> None:
    """PrimaryKey fields are default display excludes."""

    class WorkbenchModel(BaseModel):
        id: int = AirField(default=0, primary_key=True)
        wood_type: str

    class WorkbenchForm(AirForm[WorkbenchModel]):
        pass

    html = WorkbenchForm().render()
    assert "wood_type" in html
    assert 'name="id"' not in html


def test_excludes_csrf_default_save_exclude() -> None:
    """CsrfToken fields are default save excludes, not in form.data."""

    class WorkbenchModel(BaseModel):
        wood_type: str

    class WorkbenchForm(AirForm[WorkbenchModel]):
        pass

    form = WorkbenchForm()
    html = form.render()

    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match
    token = match.group(1)

    form.validate({"wood_type": "cherry", "csrf_token": token})
    assert form.is_valid
    assert form.data.wood_type == "cherry"
    assert not hasattr(form.data, "csrf_token")


def test_excludes_user_extends_defaults() -> None:
    """User excludes merge with metadata defaults, not replace them."""

    class WorkbenchModel(BaseModel):
        id: int = AirField(default=0, primary_key=True)
        wood_type: str
        created_at: str = AirField(default="2026-01-01")

    class WorkbenchForm(AirForm[WorkbenchModel]):
        excludes = ("created_at",)

    html = WorkbenchForm().render()
    # id excluded from display (PrimaryKey default)
    assert 'name="id"' not in html
    # created_at excluded from display (user)
    assert "created_at" not in html
    # wood_type rendered
    assert "wood_type" in html


def test_excludes_multiple_scopes_in_tuple() -> None:
    """A tuple can list multiple scopes."""

    class WorkbenchModel(BaseModel):
        wood_type: str
        secret_code: str = AirField(default="")

    class WorkbenchForm(AirForm[WorkbenchModel]):
        excludes = (("secret_code", "display", "save"),)

    # Display: secret_code not rendered
    html = WorkbenchForm().render()
    assert "secret_code" not in html

    # Save: secret_code not in save_data
    form = WorkbenchForm()
    form.validate({"wood_type": "birch"})
    assert form.is_valid
    assert "secret_code" not in form.save_data()
