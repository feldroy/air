"""Backend-neutral Pydantic models with async persistence methods.

``AirModel`` owns model definition, validation, and public CRUD semantics.
Persistence is supplied separately by an :class:`AirModelBackend`, such as
AirPostgres or AirD1.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict

from air.field import PrimaryKey
from air.model.backend import get_model_backend

if TYPE_CHECKING:
    from collections.abc import Mapping

    from pydantic.fields import FieldInfo


_GENERIC_MODULES = frozenset({"main", "app", "models", "__main__", "server"})
_model_registry: list[type[AirModel]] = []
_LOOKUPS = frozenset({"gt", "gte", "lt", "lte", "contains", "icontains", "in", "isnull"})


class MultipleObjectsReturned(Exception):  # noqa: N818
    """Raised by ``AirModel.get`` when a query matches multiple rows."""


@dataclass(frozen=True)
class Predicate:
    """A backend-neutral comparison for one model field."""

    field: str
    lookup: str
    value: Any


@dataclass(frozen=True)
class Query:
    """A backend-neutral query over one AirModel class."""

    model: type[AirModel]
    predicates: tuple[Predicate, ...] = ()
    order_by: str | None = None
    limit: int | None = None
    offset: int | None = None


def _normalize_project_name(name: str) -> str:
    """Normalize a project name for use as a model table prefix."""
    for tld in (".com", ".org", ".io", ".net", ".dev", ".app"):
        if name.endswith(tld):
            name = name[: -len(tld)]
            break
    return name.replace("-", "_").replace(".", "_").lower()


@lru_cache(maxsize=1)
def _read_project_name() -> str | None:
    for parent in [Path.cwd(), *Path.cwd().parents]:
        toml_path = parent / "pyproject.toml"
        if toml_path.is_file():
            try:
                with toml_path.open("rb") as file:
                    return tomllib.load(file).get("project", {}).get("name")
            except (OSError, tomllib.TOMLDecodeError, KeyError):
                return None
    return None


def _table_prefix(module_name: str) -> str:
    """Derive a table prefix from a model's defining module."""
    top_module = module_name.split(".", maxsplit=1)[0]
    if top_module not in _GENERIC_MODULES:
        return top_module
    project_name = _read_project_name()
    return _normalize_project_name(project_name) if project_name else top_module


def _is_primary_key(field_info: FieldInfo) -> bool:
    return any(isinstance(metadata, PrimaryKey) for metadata in field_info.metadata)


def _parse_predicates(model: type[AirModel], values: Mapping[str, Any]) -> tuple[Predicate, ...]:
    """Turn public filter kwargs into validated backend-neutral predicates.

    Raises:
        ValueError: If a filter does not name a model field.
    """
    predicates: list[Predicate] = []
    for key, value in values.items():
        field, separator, lookup = key.rpartition("__")
        if not separator or lookup not in _LOOKUPS:
            field, lookup = key, "exact"
        if field not in model.model_fields:
            msg = f"{field!r} is not a field on {model.__name__}."
            raise ValueError(msg)
        predicates.append(Predicate(field, lookup, value))
    return tuple(predicates)


def registered_models() -> tuple[type[AirModel], ...]:
    """Return the AirModel subclasses registered in this process."""
    return tuple(_model_registry)


class AirModel(BaseModel):
    """A validated model with pluggable async persistence.

    Subclass this with ordinary Pydantic field annotations. CRUD methods use
    the active ``AirModelBackend`` while keeping validation and result
    semantics identical for every backend.
    """

    model_config = ConfigDict(from_attributes=True)
    table_name: ClassVar[str | None] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _model_registry.append(cls)

    def __getitem__(self, key: str) -> Any:
        """Allow row-style access in templates as well as attribute access."""
        return getattr(self, key)

    @classmethod
    def database_table(cls) -> str:
        """Return the storage name, honoring an explicit ``table_name``."""
        if cls.table_name is not None:
            return cls.table_name
        snake_case = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", cls.__name__).lower()
        return f"{_table_prefix(cls.__module__)}_{snake_case}"

    @classmethod
    def _table_name(cls) -> str:
        """Compatibility alias for backend implementations."""
        return cls.database_table()

    @classmethod
    def primary_key_field(cls) -> str | None:
        """Return the primary-key field name, if one is declared."""
        for name, field_info in cls.model_fields.items():
            if _is_primary_key(field_info):
                return name
        return None

    @classmethod
    def _pk_field(cls) -> str | None:
        """Compatibility alias for backend implementations."""
        return cls.primary_key_field()

    @classmethod
    def database_fields(cls) -> list[str]:
        """Return model field names excluding the primary key."""
        primary_key = cls.primary_key_field()
        return [name for name in cls.model_fields if name != primary_key]

    @classmethod
    def _non_pk_fields(cls) -> list[str]:
        """Compatibility alias for backend implementations."""
        return cls.database_fields()

    @classmethod
    def _non_primary_values(cls, values: Mapping[str, Any]) -> dict[str, Any]:
        primary_key = cls.primary_key_field()
        return {name: value for name, value in values.items() if name != primary_key}

    @classmethod
    def _query(
        cls,
        filters: Mapping[str, Any] | None = None,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Query:
        if order_by is not None:
            field = order_by.removeprefix("-")
            if field not in cls.model_fields:
                msg = f"{field!r} is not a field on {cls.__name__}."
                raise ValueError(msg)
        return Query(cls, _parse_predicates(cls, filters or {}), order_by, limit, offset)

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        """Validate, persist, and return a new model instance."""
        candidate = cls.model_validate(kwargs)
        row = await get_model_backend().insert(cls, cls._non_primary_values(candidate.model_dump()))
        return cls.model_validate(row)

    @classmethod
    async def bulk_create(cls, items: list[dict[str, Any]]) -> list[Self]:
        """Validate and persist multiple models in one backend operation."""
        if not items:
            return []
        candidates = [cls.model_validate(item) for item in items]
        rows = await get_model_backend().insert_many(
            cls,
            [cls._non_primary_values(candidate.model_dump()) for candidate in candidates],
        )
        return [cls.model_validate(row) for row in rows]

    @classmethod
    async def get(cls, **kwargs: Any) -> Self | None:
        """Return one matching model, ``None``, or raise on multiple matches.

        Raises:
            MultipleObjectsReturned: If the query matches more than one row.
        """
        rows = await get_model_backend().select(cls._query(kwargs, limit=2))
        if not rows:
            return None
        if len(rows) > 1:
            msg = f"{cls.__name__}.get() matched more than one row. Use filter() to retrieve multiple results."
            raise MultipleObjectsReturned(msg)
        return cls.model_validate(rows[0])

    @classmethod
    async def filter(
        cls,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        **kwargs: Any,
    ) -> list[Self]:
        """Return models matching the shared AirModel lookup syntax."""
        rows = await get_model_backend().select(cls._query(kwargs, order_by=order_by, limit=limit, offset=offset))
        return [cls.model_validate(row) for row in rows]

    @classmethod
    async def all(
        cls,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Self]:
        """Return every persisted model."""
        rows = await get_model_backend().select(cls._query(order_by=order_by, limit=limit, offset=offset))
        return [cls.model_validate(row) for row in rows]

    @classmethod
    async def count(cls, **kwargs: Any) -> int:
        """Return the number of models matching optional filters."""
        return await get_model_backend().count(cls._query(kwargs))

    @classmethod
    async def bulk_update(cls, set_values: dict[str, Any], **filter_kwargs: Any) -> int:
        """Update matching models and return the affected count.

        Raises:
            ValueError: If no filter or invalid update field is provided.
        """
        if not filter_kwargs:
            msg = "bulk_update() requires at least one filter."
            raise ValueError(msg)
        cls._validate_update_fields(set_values)
        return await get_model_backend().update_many(cls._query(filter_kwargs), set_values)

    @classmethod
    async def bulk_delete(cls, **filter_kwargs: Any) -> int:
        """Delete matching models and return the affected count.

        Raises:
            ValueError: If no filter is provided.
        """
        if not filter_kwargs:
            msg = "bulk_delete() requires at least one filter."
            raise ValueError(msg)
        return await get_model_backend().delete_many(cls._query(filter_kwargs))

    @classmethod
    def _validate_update_fields(cls, values: Mapping[str, Any]) -> None:
        primary_key = cls.primary_key_field()
        invalid = set(values) - set(cls.model_fields)
        if primary_key is not None and primary_key in values:
            invalid.add(primary_key)
        if invalid:
            msg = f"Unknown or primary-key update fields: {sorted(invalid)}"
            raise ValueError(msg)

    async def save(self, *, update_fields: list[str] | None = None) -> None:
        """Persist changes to this model instance.

        Raises:
            ValueError: If this model cannot be safely updated.
        """
        primary_key = self.primary_key_field()
        if primary_key is None:
            msg = f"{type(self).__name__} has no primary_key field"
            raise ValueError(msg)
        primary_value = getattr(self, primary_key)
        if primary_value is None:
            msg = "Cannot save a row without a primary key value. Use create() for new rows."
            raise ValueError(msg)
        if update_fields == []:
            msg = "update_fields cannot be empty. Omit the argument to update all fields."
            raise ValueError(msg)
        values = type(self)._non_primary_values(self.model_dump())
        if update_fields is not None:
            type(self)._validate_update_fields(dict.fromkeys(update_fields))
            values = {name: values[name] for name in update_fields}
        row = await get_model_backend().update(type(self), primary_value, values)
        for name, value in row.items():
            if name in type(self).model_fields:
                setattr(self, name, value)

    async def delete(self) -> None:
        """Delete this model instance from the active backend.

        Raises:
            ValueError: If this model cannot be safely deleted.
        """
        primary_key = self.primary_key_field()
        if primary_key is None:
            msg = f"{type(self).__name__} has no primary_key field"
            raise ValueError(msg)
        primary_value = getattr(self, primary_key)
        if primary_value is None:
            msg = "Cannot delete a row without a primary key value."
            raise ValueError(msg)
        await get_model_backend().delete_many(type(self)._query({primary_key: primary_value}))
        setattr(self, primary_key, None)
