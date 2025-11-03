"""Model utilities for Air.

Provides a thin wrapper around :class:`pydantic.BaseModel` that knows how to
generate matching :class:`air.forms.AirForm` subclasses on demand.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from pydantic import BaseModel

from .forms import AirForm, to_form


class AirModel(BaseModel):
    """Base class for models that integrate tightly with Air forms."""

    @classmethod
    def to_form(
        cls,
        *,
        name: str | None = None,
        includes: Sequence[str] | None = None,
        widget: Callable | None = None,
    ) -> AirForm:
        """Return an :class:`AirForm` instance bound to ``cls``.

        Args:
            name: Optional explicit class name for the generated form.
            includes: Optional iterable of field names to render (defaults to all fields).
            widget: Optional custom rendering callable.

        Returns:
            An instance of :class:`AirForm` that validates against ``cls``.
        """

        return to_form(cls, name=name, includes=includes, widget=widget)
