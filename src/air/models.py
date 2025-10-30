"""Model utilities for Air.

Provides a thin wrapper around :class:`pydantic.BaseModel` that knows how to
generate matching :class:`air.forms.AirForm` subclasses on demand.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from pydantic import BaseModel

from .forms import AirForm, model_form


class AirModel(BaseModel):
    """Base class for models that should integrate tightly with Air forms."""

    @classmethod
    def form(
        cls,
        *,
        name: str | None = None,
        includes: Sequence[str] | None = None,
        widget: Callable | None = None,
    ) -> type[AirForm]:
        """Return an :class:`AirForm` subclass bound to ``cls``.

        Args:
            name: Optional explicit class name for the generated form.
            includes: Optional iterable of field names to render (defaults to all fields).
            widget: Optional custom rendering callable.

        Returns:
            A subclass of :class:`AirForm` that validates against ``cls``.
        """

        return model_form(cls, name=name, includes=includes, widget=widget)
