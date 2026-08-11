"""UI presentation metadata for Pydantic fields.

Like annotated-types defines validation vocabulary (Gt, Lt, MinLen)
without performing validation, airfield defines presentation vocabulary
(Widget, Label, Choices) without performing rendering.

Consumers discover metadata via field_info.metadata, the same way
Pydantic discovers annotated-types constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from air.model import AirModel


class BasePresentation:
    """Base class for all presentation metadata.

    Consumers can do ``isinstance(m, BasePresentation)`` while
    traversing field annotations to find all airfield metadata.
    """

    __slots__ = ()


# ---------------------------------------------------------------------------
# Identity and structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PrimaryKey(BasePresentation):
    """Marks this field as the primary identity for the record.

    Affects presentation across contexts: typically hidden in create
    forms, read-only in edit forms, displayed as a link in tables,
    used as the record identifier in detail views and URLs.
    """


@dataclass(frozen=True, slots=True)
class ForeignKey(BasePresentation):
    """Marks this field as a foreign key to another AirModel.

    This metadata is structural rather than presentational. Consumers in
    ``air.model`` use it to derive relation attribute names, validate
    collisions, and eventually build relationship-aware query helpers.
    """

    to: type["AirModel"] | str
    on_delete: Literal["cascade", "set_null", "restrict"] = "restrict"


@dataclass(frozen=True, slots=True)
class CsrfToken(BasePresentation):
    """Marks this field as a CSRF protection token.

    Form renderers should render this as a hidden input with a
    signed value. Form validators should verify the signature
    before processing other fields. The field should not appear
    in user-facing form layouts.
    """


# ---------------------------------------------------------------------------
# Identity and labeling
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Label(BasePresentation):
    """Human-readable name for the field.

    Used everywhere a field needs a display name: form labels,
    table headers, CLI prompts, chart axis labels, API docs.

    Without this, consumers fall back to the field name with
    underscores replaced by spaces and title-cased.
    """

    text: str


@dataclass(frozen=True, slots=True)
class Placeholder(BasePresentation):
    """Example or hint text shown when the field is empty.

    In a form: the placeholder attribute.
    In a CLI: shown in parentheses after the prompt.
    In API docs: the example value.
    """

    text: str


@dataclass(frozen=True, slots=True)
class HelpText(BasePresentation):
    """Explanatory text that supplements the label.

    In a form: text below the input.
    In a CLI: shown when the user asks for help on a field.
    In API docs: the parameter description.
    In a table: tooltip on the column header.
    """

    text: str


# ---------------------------------------------------------------------------
# Input and display
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Widget(BasePresentation):
    """Preferred input/display mechanism for the field.

    The ``kind`` is a semantic name, not an HTML element.
    Consuming libraries map these to their own components.

    Standard kinds (consumers should recognize at minimum):
        text, textarea, date, datetime, time, color, email, url,
        password, file, hidden, toggle, slider, rating, rich_text,
        code, search, phone, currency, autocomplete

    Libraries are free to define additional kinds. Unknown kinds
    should fall back to ``"text"`` without raising errors.
    """

    kind: str


@dataclass(frozen=True, slots=True)
class DisplayFormat(BasePresentation):
    """How to format the field's value for display (not input).

    Common patterns:
        ``"percent"``       0.42 -> "42%"
        ``"currency"``      1234.5 -> "$1,234.50"
        ``"bytes"``         1048576 -> "1 MB"
        ``"relative_time"`` datetime -> "3 hours ago"
        ``"%Y-%m-%d"``      datetime -> "2026-03-18"
    """

    pattern: str
    locale: str | None = None


@dataclass(frozen=True, slots=True)
class Choices(BasePresentation):
    """Constrains the field to a set of labeled options.

    In a form: rendered as a ``<select>``, radio group, or combobox.
    In a CLI: a numbered menu or autocomplete.
    In API docs: an enumerated parameter.

    Each option is ``(value, display_label)``.
    """

    options: tuple[tuple[Any, str], ...]

    def __init__(self, *options: tuple[Any, str]) -> None:
        object.__setattr__(self, "options", options)


# ---------------------------------------------------------------------------
# Table and list context
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ColumnAlign(BasePresentation):
    """How to align the field's value in a table column."""

    align: Literal["left", "center", "right"]


@dataclass(frozen=True, slots=True)
class ColumnWidth(BasePresentation):
    """Preferred width for the field in a table column.

    Expressed as a relative weight. A field with weight=2 gets
    roughly twice the space of a field with weight=1.
    """

    weight: float = 1.0
    min_chars: int | None = None
    max_chars: int | None = None


# ---------------------------------------------------------------------------
# Focus and interaction
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Autofocus(BasePresentation):
    """This field should receive input focus when the UI context loads.

    In a form: sets the autofocus attribute on the input.
    In a CLI: this field is prompted first.
    In a TUI: this widget receives initial focus.

    Only one field per form/view should have this.
    """


# ---------------------------------------------------------------------------
# Behavior across contexts
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Filterable(BasePresentation):
    """Whether and how this field should appear in search/filter UI.

    In a table: adds a filter control to the column.
    In an admin panel: adds to the filter sidebar.
    In a CLI list command: adds a ``--field=value`` filter flag.
    """

    kind: Literal["exact", "contains", "range", "multi_select"] = "exact"


@dataclass(frozen=True, slots=True)
class Sortable(BasePresentation):
    """Whether this field should be sortable in list/table contexts.

    When ``default`` is True, this field is the initial sort key.
    """

    default: bool = False
    descending: bool = False


@dataclass(frozen=True, slots=True)
class Hidden(BasePresentation):
    """Field should not be shown in the specified contexts.

    With no arguments, hidden everywhere. Standard context names:
    ``"form"``, ``"table"``, ``"detail"``, ``"api"``, ``"cli"``, ``"export"``
    """

    contexts: tuple[str, ...] = ()

    def __init__(self, *contexts: str) -> None:
        object.__setattr__(self, "contexts", contexts)

    def in_context(self, context: str) -> bool:
        """True if the field is hidden in the given context."""
        return not self.contexts or context in self.contexts


@dataclass(frozen=True, slots=True)
class ReadOnly(BasePresentation):
    """Field should be displayed but not editable.

    With no arguments, read-only everywhere.
    """

    contexts: tuple[str, ...] = ()

    def __init__(self, *contexts: str) -> None:
        object.__setattr__(self, "contexts", contexts)

    def in_context(self, context: str) -> bool:
        """True if the field is read-only in the given context."""
        return not self.contexts or context in self.contexts


@dataclass(frozen=True, slots=True)
class Grouped(BasePresentation):
    """Assigns the field to a named group for layout purposes.

    In a form: fields in the same group appear in the same fieldset.
    In a table: groups can become column groups.
    In a detail view: groups become sections.
    """

    name: str
    order: int = 0


@dataclass(frozen=True, slots=True)
class Priority(BasePresentation):
    """How important this field is relative to siblings.

    Higher priority fields are shown first, or shown when space
    is limited while lower-priority fields are hidden.
    """

    level: int


@dataclass(frozen=True, slots=True)
class Compact(BasePresentation):
    """How to represent this field in space-constrained contexts."""

    format: str | None = None
    max_length: int | None = None
