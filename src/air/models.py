"""Model utilities for Air.

Provides a thin wrapper around :class:`pydantic.BaseModel` that knows how to
generate matching :class:`air.forms.AirForm` subclasses on demand.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import ClassVar

from pydantic import BaseModel

from .forms import AirForm, model_form


class AirModel(BaseModel):
	"""Base class for models that should integrate tightly with Air forms."""

	_air_form_cache: ClassVar[dict[tuple[tuple[str, ...] | None, Callable | None, str | None], type[AirForm]]] = {}

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

		includes_key = tuple(includes) if includes is not None else None
		cache_key = (includes_key, widget, name)

		cache = cls.__dict__.get("_air_form_cache")
		if cache is None or cache is AirModel._air_form_cache:
			cache = {}
			setattr(cls, "_air_form_cache", cache)

		if cache_key not in cache:
			cache[cache_key] = model_form(cls, name=name, includes=includes, widget=widget)

		return cache[cache_key]

