"""Backend contract for :class:`air.model.AirModel` persistence."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence
    from contextlib import AbstractAsyncContextManager

    from air.model.main import AirModel, Query


class AirModelBackend(Protocol):
    """Storage primitives required by :class:`AirModel`.

    AirModel owns validation and public CRUD semantics. Backends translate a
    backend-neutral query into their driver or service API and return plain
    row mappings. This keeps PostgreSQL and D1 implementations consistent
    without making either one depend on Pydantic model construction.
    """

    async def create_tables(self, models: Iterable[type[AirModel]] | None = None) -> None: ...

    async def insert(self, model: type[AirModel], values: Mapping[str, Any]) -> Mapping[str, Any]: ...

    async def insert_many(
        self,
        model: type[AirModel],
        values: Sequence[Mapping[str, Any]],
    ) -> Sequence[Mapping[str, Any]]: ...

    async def select(self, query: Query) -> Sequence[Mapping[str, Any]]: ...

    async def count(self, query: Query) -> int: ...

    async def update(
        self,
        model: type[AirModel],
        primary_key: Any,
        values: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...

    async def update_many(self, query: Query, values: Mapping[str, Any]) -> int: ...

    async def delete_many(self, query: Query) -> int: ...


class AirModelTransactionBackend(AirModelBackend, Protocol):
    """Optional capability for backends with scoped transaction support."""

    def transaction(self) -> AbstractAsyncContextManager[None]: ...


_active_backend: AirModelBackend | None = None


def set_model_backend(backend: AirModelBackend | None) -> None:
    """Set the process-wide persistence backend used by all AirModel classes."""
    global _active_backend
    _active_backend = backend


def clear_model_backend(backend: AirModelBackend | None = None) -> None:
    """Clear the active backend.

    When *backend* is provided, it is only cleared if that exact object is
    active. This prevents one backend's shutdown from unregistering a backend
    that replaced it.
    """
    global _active_backend
    if backend is None or _active_backend is backend:
        _active_backend = None


def get_model_backend() -> AirModelBackend:
    """Return the configured persistence backend.

    Raises:
        RuntimeError: If no backend has been configured.
    """
    if _active_backend is None:
        msg = (
            "No AirModel backend is configured. "
            "Configure a persistence package such as AirPostgres or AirD1 before using model CRUD methods."
        )
        raise RuntimeError(msg)
    return _active_backend
