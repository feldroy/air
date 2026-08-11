"""AirField: UI presentation vocabulary for Pydantic models.

annotated-types is for validation. airfield is for presentation.
Define once on the model, render anywhere.
"""

from air.field.main import AirField as AirField
from air.field.types import (
    Autofocus as Autofocus,
    BasePresentation as BasePresentation,
    Choices as Choices,
    ColumnAlign as ColumnAlign,
    ColumnWidth as ColumnWidth,
    Compact as Compact,
    CsrfToken as CsrfToken,
    DisplayFormat as DisplayFormat,
    Filterable as Filterable,
    ForeignKey as ForeignKey,
    Grouped as Grouped,
    HelpText as HelpText,
    Hidden as Hidden,
    Label as Label,
    Placeholder as Placeholder,
    PrimaryKey as PrimaryKey,
    Priority as Priority,
    ReadOnly as ReadOnly,
    Sortable as Sortable,
    Widget as Widget,
)

__all__ = [
    "AirField",
    "Autofocus",
    "BasePresentation",
    "Choices",
    "ColumnAlign",
    "ColumnWidth",
    "Compact",
    "CsrfToken",
    "DisplayFormat",
    "Filterable",
    "ForeignKey",
    "Grouped",
    "HelpText",
    "Hidden",
    "Label",
    "Placeholder",
    "PrimaryKey",
    "Priority",
    "ReadOnly",
    "Sortable",
    "Widget",
]
