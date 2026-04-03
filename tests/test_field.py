"""Tests for `air.field` package."""

from __future__ import annotations

from typing import Annotated

import pytest
from pydantic import BaseModel

import air.field
from air.field import (
    AirField,
    Autofocus,
    BasePresentation,
    Choices,
    HelpText,
    Hidden,
    Label,
    Placeholder,
    PrimaryKey,
    ReadOnly,
    Widget,
)


def test_import() -> None:
    """Verify the package can be imported."""
    assert air.field


# ---------------------------------------------------------------------------
# Helper to extract typed metadata from a field
# ---------------------------------------------------------------------------


def _get_meta(model: type[BaseModel], field_name: str, meta_type: type) -> object | None:
    """Return the first metadata object of meta_type from a field, or None."""
    field_info = model.model_fields[field_name]
    for m in field_info.metadata:
        if isinstance(m, meta_type):
            return m
    return None


def _get_all_meta(model: type[BaseModel], field_name: str, base: type = BasePresentation) -> list[object]:
    """Return all metadata objects that are instances of base."""
    field_info = model.model_fields[field_name]
    return [m for m in field_info.metadata if isinstance(m, base)]


# ---------------------------------------------------------------------------
# AirField produces typed metadata
# ---------------------------------------------------------------------------


class TestAirFieldProducesTypedMetadata:
    """AirField() kwargs should produce typed metadata objects in field_info.metadata."""

    def test_label(self) -> None:
        class M(BaseModel):
            name: str = AirField(label="Full Name")

        meta = _get_meta(M, "name", Label)
        assert meta is not None
        assert meta.text == "Full Name"

    def test_widget_from_type_kwarg(self) -> None:
        """AirField(type="email") should produce Widget("email")."""

        class M(BaseModel):
            email: str = AirField(type="email")

        meta = _get_meta(M, "email", Widget)
        assert meta is not None
        assert meta.kind == "email"

    def test_widget_from_widget_kwarg(self) -> None:
        """AirField(widget="textarea") should produce Widget("textarea")."""

        class M(BaseModel):
            bio: str = AirField(widget="textarea")

        meta = _get_meta(M, "bio", Widget)
        assert meta is not None
        assert meta.kind == "textarea"

    def test_placeholder(self) -> None:
        class M(BaseModel):
            email: str = AirField(placeholder="you@example.com")

        meta = _get_meta(M, "email", Placeholder)
        assert meta is not None
        assert meta.text == "you@example.com"

    def test_help_text(self) -> None:
        class M(BaseModel):
            password: str = AirField(help_text="At least 8 characters")

        meta = _get_meta(M, "password", HelpText)
        assert meta is not None
        assert meta.text == "At least 8 characters"

    def test_choices(self) -> None:
        class M(BaseModel):
            color: str = AirField(choices=[("r", "Red"), ("g", "Green")])

        meta = _get_meta(M, "color", Choices)
        assert meta is not None
        assert meta.options == (("r", "Red"), ("g", "Green"))

    def test_primary_key(self) -> None:
        class M(BaseModel):
            id: int = AirField(primary_key=True)

        meta = _get_meta(M, "id", PrimaryKey)
        assert meta is not None

    def test_autofocus(self) -> None:
        class M(BaseModel):
            name: str = AirField(autofocus=True)

        meta = _get_meta(M, "name", Autofocus)
        assert meta is not None

    def test_multiple_metadata(self) -> None:
        """A field with several kwargs gets multiple typed metadata objects."""

        class M(BaseModel):
            email: str = AirField(type="email", label="Email Address", placeholder="you@example.com")

        all_meta = _get_all_meta(M, "email")
        types = {type(m) for m in all_meta}
        assert types == {Widget, Label, Placeholder}

    def test_no_presentation_metadata_when_none_specified(self) -> None:
        class M(BaseModel):
            name: str = AirField()

        all_meta = _get_all_meta(M, "name")
        assert all_meta == []

    def test_all_kwargs_together(self) -> None:
        """Every AirField kwarg produces its typed metadata."""

        class M(BaseModel):
            email: str = AirField(
                primary_key=True,
                type="email",
                label="Email",
                placeholder="you@example.com",
                help_text="Your email address",
                autofocus=True,
            )

        all_meta = _get_all_meta(M, "email")
        types = {type(m) for m in all_meta}
        assert types == {PrimaryKey, Widget, Label, Placeholder, HelpText, Autofocus}


# ---------------------------------------------------------------------------
# AirField still passes through Pydantic parameters
# ---------------------------------------------------------------------------


class TestAirFieldPydanticPassthrough:
    """Pydantic Field parameters should still work."""

    def test_default_value(self) -> None:
        class M(BaseModel):
            name: str = AirField("default_name", label="Name")

        assert M().name == "default_name"
        assert _get_meta(M, "name", Label).text == "Name"

    def test_default_factory(self) -> None:
        class M(BaseModel):
            tags: list[str] = AirField(default_factory=list)

        assert M().tags == []

    def test_pydantic_constraints(self) -> None:
        class M(BaseModel):
            age: int = AirField(ge=0, le=150)

        with pytest.raises(ValueError, match="greater than or equal"):
            M(age=-1)
        assert M(age=25).age == 25

    def test_json_schema_extra_passthrough(self) -> None:
        """Explicit json_schema_extra passes through to Pydantic."""

        class M(BaseModel):
            name: str = AirField(json_schema_extra={"x-custom": True})

        field_info = M.model_fields["name"]
        extra = field_info.json_schema_extra
        assert extra is not None
        assert extra["x-custom"] is True

    def test_unknown_kwargs_warn(self) -> None:
        """Unknown kwargs trigger Pydantic's deprecation warning."""
        with pytest.warns(DeprecationWarning, match="extra keyword arguments"):
            AirField(custom_attr="custom_value")


# ---------------------------------------------------------------------------
# AirField does not write to json_schema_extra
# ---------------------------------------------------------------------------


class TestNoJsonSchemaExtra:
    """AirField should never write to json_schema_extra itself."""

    def test_primary_key_not_in_json_schema_extra(self) -> None:
        class M(BaseModel):
            id: int = AirField(primary_key=True)

        field_info = M.model_fields["id"]
        assert field_info.json_schema_extra is None

    def test_autofocus_not_in_json_schema_extra(self) -> None:
        class M(BaseModel):
            name: str = AirField(autofocus=True)

        field_info = M.model_fields["name"]
        assert field_info.json_schema_extra is None

    def test_label_not_in_json_schema_extra(self) -> None:
        class M(BaseModel):
            name: str = AirField(label="Name")

        field_info = M.model_fields["name"]
        assert field_info.json_schema_extra is None

    def test_explicit_json_schema_extra_still_works(self) -> None:
        """User-provided json_schema_extra passes through untouched."""

        class M(BaseModel):
            name: str = AirField(label="Name", json_schema_extra={"x-foo": 1})

        field_info = M.model_fields["name"]
        assert field_info.json_schema_extra == {"x-foo": 1}
        assert _get_meta(M, "name", Label).text == "Name"


# ---------------------------------------------------------------------------
# Annotated metadata path produces same result
# ---------------------------------------------------------------------------


class TestAnnotatedMetadata:
    """Annotated[str, Widget("email")] should be discoverable the same way."""

    def test_annotated_widget(self) -> None:
        class M(BaseModel):
            email: Annotated[str, Widget("email")]

        meta = _get_meta(M, "email", Widget)
        assert meta is not None
        assert meta.kind == "email"

    def test_annotated_label(self) -> None:
        class M(BaseModel):
            name: Annotated[str, Label("Full Name")]

        meta = _get_meta(M, "name", Label)
        assert meta is not None
        assert meta.text == "Full Name"

    def test_annotated_multiple(self) -> None:
        class M(BaseModel):
            email: Annotated[str, Widget("email"), Label("Email"), Placeholder("you@example.com")]

        assert _get_meta(M, "email", Widget).kind == "email"
        assert _get_meta(M, "email", Label).text == "Email"
        assert _get_meta(M, "email", Placeholder).text == "you@example.com"

    def test_annotated_hidden(self) -> None:
        class M(BaseModel):
            secret: Annotated[str, Hidden("form", "table")]

        meta = _get_meta(M, "secret", Hidden)
        assert meta.in_context("form") is True
        assert meta.in_context("api") is False

    def test_annotated_readonly(self) -> None:
        class M(BaseModel):
            created: Annotated[str, ReadOnly("form")]

        meta = _get_meta(M, "created", ReadOnly)
        assert meta.in_context("form") is True
        assert meta.in_context("table") is False

    def test_annotated_primary_key(self) -> None:
        class M(BaseModel):
            id: Annotated[int, PrimaryKey()]

        meta = _get_meta(M, "id", PrimaryKey)
        assert meta is not None

    def test_annotated_autofocus(self) -> None:
        class M(BaseModel):
            name: Annotated[str, Autofocus()]

        meta = _get_meta(M, "name", Autofocus)
        assert meta is not None


# ---------------------------------------------------------------------------
# Both paths produce equivalent metadata
# ---------------------------------------------------------------------------


class TestBothPathsEquivalent:
    """AirField() and Annotated[] should produce the same metadata."""

    def test_airfield_and_annotated_both_discoverable(self) -> None:
        class M(BaseModel):
            email_a: str = AirField(type="email", label="Email")
            email_b: Annotated[str, Widget("email"), Label("Email")]

        for field_name in ("email_a", "email_b"):
            w = _get_meta(M, field_name, Widget)
            label = _get_meta(M, field_name, Label)
            assert w is not None, f"{field_name} missing Widget"
            assert label is not None, f"{field_name} missing Label"
            assert w.kind == "email"
            assert label.text == "Email"

    def test_primary_key_both_paths(self) -> None:
        class M(BaseModel):
            id_a: int = AirField(primary_key=True)
            id_b: Annotated[int, PrimaryKey()]

        for field_name in ("id_a", "id_b"):
            pk = _get_meta(M, field_name, PrimaryKey)
            assert pk is not None, f"{field_name} missing PrimaryKey"

    def test_autofocus_both_paths(self) -> None:
        class M(BaseModel):
            name_a: str = AirField(autofocus=True)
            name_b: Annotated[str, Autofocus()]

        for field_name in ("name_a", "name_b"):
            af = _get_meta(M, field_name, Autofocus)
            assert af is not None, f"{field_name} missing Autofocus"
