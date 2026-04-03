"""AirField: unified field descriptor for Pydantic models.

Wraps pydantic.Field so users can describe everything about a field
in one place. All AirField parameters become typed metadata objects
in field_info.metadata. Pydantic parameters (ge, le, min_length,
json_schema_extra, etc.) pass straight through to Field().
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field as PydanticField

from air.field.types import (
    Autofocus,
    Choices,
    HelpText,
    Label,
    Placeholder,
    PrimaryKey,
    Widget,
)

if TYPE_CHECKING:
    from pydantic.fields import FieldInfo


def AirField(  # noqa: C901, N802
    default: Any = ...,
    *,
    # Presentation
    primary_key: bool = False,
    type: str | None = None,  # noqa: A002
    label: str | None = None,
    widget: str | None = None,
    choices: list[tuple[Any, str]] | None = None,
    autofocus: bool = False,
    placeholder: str | None = None,
    help_text: str | None = None,
    # Pydantic pass-through
    default_factory: Any = None,
    **kwargs: Any,
) -> Any:
    """Unified field descriptor for Pydantic models.

    Accepts presentation metadata (``primary_key``, ``type``, ``label``,
    ``widget``, ``choices``, ``placeholder``, ``help_text``,
    ``autofocus``) and all standard ``pydantic.Field`` parameters.

    All AirField-specific parameters become typed metadata objects in
    ``field_info.metadata``. Remaining ``**kwargs`` pass through to
    ``pydantic.Field()``; Pydantic raises on unrecognized parameters.

    Returns:
        A Pydantic FieldInfo configured with all specified parameters.
    """
    if default is not ...:
        kwargs["default"] = default
    if default_factory is not None:
        kwargs["default_factory"] = default_factory

    field_info: FieldInfo = PydanticField(**kwargs)

    # Typed presentation metadata
    if primary_key:
        field_info.metadata.append(PrimaryKey())
    if type:
        field_info.metadata.append(Widget(kind=type))
    if widget:
        field_info.metadata.append(Widget(kind=widget))
    if label:
        field_info.metadata.append(Label(text=label))
    if placeholder:
        field_info.metadata.append(Placeholder(text=placeholder))
    if help_text:
        field_info.metadata.append(HelpText(text=help_text))
    if choices:
        field_info.metadata.append(Choices(*choices))
        # Choices implies a select widget unless explicitly overridden
        if not type and not widget:
            field_info.metadata.append(Widget(kind="select"))
    if autofocus:
        field_info.metadata.append(Autofocus())

    return field_info
