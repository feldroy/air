"""Async ORM module for Air.

Provides a minimal async ORM built on asyncpg and Pydantic v2, with a
Django-inspired API for defining tables and performing CRUD operations
against PostgreSQL.

Example::

    from air.db import AirDB, Model, Field
    from datetime import datetime

    db = AirDB()

    class BetaApplication(Model):
        id: int | None = Field(default=None, primary_key=True)
        created_at: datetime = Field(default_factory=datetime.now)
        name: str
        email: str
        making: str = Field(default="")
        why: str = Field(default="")

    app = air.Air(lifespan=db.lifespan("postgresql://..."))

    # Then in async handlers:
    await BetaApplication.create(name="Alice", email="alice@example.com")
    apps = await BetaApplication.filter(email="alice@example.com")
    app_row = await BetaApplication.get(id=1)
    all_rows = await BetaApplication.all()
    count = await BetaApplication.count()
    await db.create_tables()
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from types import UnionType
from typing import Any, ClassVar, Self, get_args, get_origin

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic.fields import FieldInfo

# ---------------------------------------------------------------------------
# Type mapping: Python types -> PostgreSQL column types
# ---------------------------------------------------------------------------

_PY_TO_PG: dict[type, str] = {
    str: "TEXT",
    int: "INTEGER",
    float: "DOUBLE PRECISION",
    bool: "BOOLEAN",
    datetime: "TIMESTAMP WITH TIME ZONE",
}


def _pg_type(python_type: type) -> str:
    """Return the PostgreSQL column type string for a Python type."""
    return _PY_TO_PG.get(python_type, "TEXT")


# ---------------------------------------------------------------------------
# Field helper
# ---------------------------------------------------------------------------


def Field(
    default: Any = ...,
    *,
    primary_key: bool = False,
    default_factory: Any = None,
    **kwargs: Any,
) -> Any:
    """Thin wrapper around :func:`pydantic.Field` that accepts a ``primary_key`` flag.

    The flag is stored in ``json_schema_extra`` so :class:`Table` can read it
    when generating SQL.

    Returns:
        A Pydantic FieldInfo with optional ``primary_key`` metadata.
    """
    schema_extra: dict[str, Any] = kwargs.pop("json_schema_extra", None) or {}
    if primary_key:
        schema_extra["primary_key"] = True

    pydantic_kwargs: dict[str, Any] = {**kwargs, "json_schema_extra": schema_extra}
    if default is not ...:
        pydantic_kwargs["default"] = default
    if default_factory is not None:
        pydantic_kwargs["default_factory"] = default_factory

    return PydanticField(**pydantic_kwargs)


# ---------------------------------------------------------------------------
# Helpers for introspecting Pydantic field types
# ---------------------------------------------------------------------------


def _is_optional(annotation: Any) -> bool:
    """Return True if *annotation* is ``X | None`` or ``Optional[X]``."""
    origin = get_origin(annotation)
    if origin is UnionType:
        return type(None) in get_args(annotation)
    import typing  # noqa: PLC0415

    if origin is typing.Union:
        return type(None) in get_args(annotation)
    return False


def _unwrap_optional(annotation: Any) -> Any:
    """Strip ``None`` from a union, returning the inner type."""
    args = [a for a in get_args(annotation) if a is not type(None)]
    return args[0] if len(args) == 1 else annotation


def _is_primary_key(field_info: FieldInfo) -> bool:
    extra = field_info.json_schema_extra
    if isinstance(extra, dict):
        return bool(extra.get("primary_key"))
    return False


# ---------------------------------------------------------------------------
# AirDB: connection pool + table registry
# ---------------------------------------------------------------------------


class AirDB:
    """Manages an asyncpg connection pool and the registry of :class:`Model` subclasses.

    Example::

        db = AirDB()
        app = air.Air(lifespan=db.lifespan("postgresql://user:pass@host/dbname"))
    """

    def __init__(self) -> None:
        self.pool: Any | None = None  # asyncpg.Pool once connected

    # -- connection lifecycle ------------------------------------------------

    def lifespan(self, url: str, **pool_kwargs: Any) -> Any:
        """Return an async context manager suitable for Air/FastAPI lifespan.

        Args:
            url: PostgreSQL connection string (supports ``postgresql://`` and
                ``postgres://`` schemes, including ``?sslmode=require`` for
                TLS connections like NeonDB).
            **pool_kwargs: Extra keyword arguments forwarded to
                :func:`asyncpg.create_pool`.

        Returns:
            An async context manager that opens the pool on entry and closes
            it on exit.
        """
        db = self

        @asynccontextmanager
        async def _lifespan(app: Any) -> AsyncIterator[None]:
            import asyncpg  # noqa: PLC0415

            db.pool = await asyncpg.create_pool(url, **pool_kwargs)
            _set_current_db(db)
            try:
                yield
            finally:
                if db.pool is not None:
                    await db.pool.close()
                    db.pool = None
                _set_current_db(None)

        return _lifespan

    # -- table management ----------------------------------------------------

    async def create_tables(self) -> None:
        """Execute ``CREATE TABLE IF NOT EXISTS`` for every registered :class:`Model`.

        Tables are registered automatically when their class body is executed,
        so simply importing your models is enough.
        """
        if self.pool is None:
            msg = "Database pool is not initialized. Did you forget to use db.lifespan()?"
            raise RuntimeError(msg)
        for table_cls in _table_registry:
            sql = table_cls._create_table_sql()
            await self.pool.execute(sql)


# ---------------------------------------------------------------------------
# Module-level current-db reference (set during lifespan)
# ---------------------------------------------------------------------------

_current_db: AirDB | None = None
_table_registry: list[type[Model]] = []


def _set_current_db(db: AirDB | None) -> None:
    global _current_db  # noqa: PLW0603
    _current_db = db


def _get_pool() -> Any:
    """Return the current asyncpg pool, raising if unavailable."""
    if _current_db is None or _current_db.pool is None:
        msg = "No database connection. Ensure AirDB.lifespan() is active."
        raise RuntimeError(msg)
    return _current_db.pool


# ---------------------------------------------------------------------------
# Table base class
# ---------------------------------------------------------------------------


class _TableMeta(type(BaseModel)):
    """Metaclass that auto-registers Model subclasses in the global registry."""

    def __init__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(name, bases, namespace, **kwargs)
        # Skip the base Model class itself; register any concrete subclass
        for base in bases:
            if getattr(base, "__name__", "") == "Model":
                _table_registry.append(cls)  # type: ignore[arg-type]
                break


class Model(BaseModel, metaclass=_TableMeta):
    """Base class for database-backed Pydantic models.

    Subclass this and declare fields using standard Pydantic annotations.
    Use :func:`Field` with ``primary_key=True`` for auto-incrementing
    primary keys.

    The table name is derived from the class name (lowercased). All query
    methods are async class methods.

    Example::

        class User(Model):
            id: int | None = Field(default=None, primary_key=True)
            name: str
            email: str
    """

    model_config: ClassVar[dict[str, Any]] = {"from_attributes": True}

    # -- SQL generation helpers ----------------------------------------------

    @classmethod
    def _table_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def _pk_field(cls) -> str | None:
        """Return the name of the primary-key field, or None."""
        for name, info in cls.model_fields.items():
            if _is_primary_key(info):
                return name
        return None

    @classmethod
    def _column_defs(cls) -> list[str]:
        """Return a list of ``"column_name TYPE [constraints]"`` strings."""
        cols: list[str] = []
        for field_name, field_info in cls.model_fields.items():
            annotation = field_info.annotation
            is_pk = _is_primary_key(field_info)

            if is_pk:
                cols.append(f'"{field_name}" SERIAL PRIMARY KEY')
                continue

            # Determine the base Python type (unwrap Optional if needed)
            if _is_optional(annotation):
                base_type = _unwrap_optional(annotation)
            else:
                base_type = annotation

            pg_type = _pg_type(base_type)  # type: ignore[arg-type]

            # NOT NULL when the field is required and not Optional
            nullable = _is_optional(annotation) if annotation else False
            is_required = field_info.is_required()

            constraint = ""
            if is_required and not nullable:
                constraint = " NOT NULL"

            cols.append(f'"{field_name}" {pg_type}{constraint}')

        return cols

    @classmethod
    def _create_table_sql(cls) -> str:
        """Generate a ``CREATE TABLE IF NOT EXISTS`` statement."""
        cols = cls._column_defs()
        cols_sql = ", ".join(cols)
        return f'CREATE TABLE IF NOT EXISTS "{cls._table_name()}" ({cols_sql})'

    @classmethod
    def _non_pk_fields(cls) -> list[str]:
        """Return field names excluding the primary key."""
        pk = cls._pk_field()
        return [n for n in cls.model_fields if n != pk]

    # -- CRUD class methods --------------------------------------------------

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        """Insert a row and return the populated model instance.

        Keyword arguments correspond to column values. The primary-key field
        (if any) is excluded from the INSERT and populated from the
        ``RETURNING`` clause.

        Returns:
            A new instance of this Table subclass with all fields set.
        """
        pool = _get_pool()
        fields = cls._non_pk_fields()
        insert_fields = [f for f in fields if f in kwargs]
        columns = ", ".join(f'"{f}"' for f in insert_fields)
        placeholders = ", ".join(f"${i + 1}" for i in range(len(insert_fields)))
        values = [kwargs[f] for f in insert_fields]

        sql = f'INSERT INTO "{cls._table_name()}" ({columns}) VALUES ({placeholders}) RETURNING *'  # noqa: S608
        row = await pool.fetchrow(sql, *values)
        return cls.model_validate(dict(row))

    @classmethod
    async def get(cls, **kwargs: Any) -> Self | None:
        """Fetch a single row matching the given keyword filters.

        Returns:
            An instance of this Table subclass, or ``None`` if no row matches.
        """
        pool = _get_pool()
        conditions = [f'"{k}" = ${i + 1}' for i, k in enumerate(kwargs)]
        where = " AND ".join(conditions)
        sql = f'SELECT * FROM "{cls._table_name()}" WHERE {where}'  # noqa: S608
        row = await pool.fetchrow(sql, *kwargs.values())
        if row is None:
            return None
        return cls.model_validate(dict(row))

    @classmethod
    async def filter(cls, **kwargs: Any) -> list[Self]:
        """Fetch all rows matching the given keyword filters.

        Returns:
            A list of model instances (possibly empty).
        """
        pool = _get_pool()
        if not kwargs:
            return await cls.all()
        conditions = [f'"{k}" = ${i + 1}' for i, k in enumerate(kwargs)]
        where = " AND ".join(conditions)
        sql = f'SELECT * FROM "{cls._table_name()}" WHERE {where}'  # noqa: S608
        rows = await pool.fetch(sql, *kwargs.values())
        return [cls.model_validate(dict(r)) for r in rows]

    @classmethod
    async def all(cls) -> list[Self]:
        """Fetch every row from the table.

        Returns:
            A list of all model instances.
        """
        pool = _get_pool()
        sql = f'SELECT * FROM "{cls._table_name()}"'  # noqa: S608
        rows = await pool.fetch(sql)
        return [cls.model_validate(dict(r)) for r in rows]

    @classmethod
    async def count(cls, **kwargs: Any) -> int:
        """Return the number of rows, optionally filtered by keyword arguments.

        Returns:
            Integer row count.
        """
        pool = _get_pool()
        if kwargs:
            conditions = [f'"{k}" = ${i + 1}' for i, k in enumerate(kwargs)]
            where = " AND ".join(conditions)
            sql = f'SELECT COUNT(*) FROM "{cls._table_name()}" WHERE {where}'  # noqa: S608
            return await pool.fetchval(sql, *kwargs.values())
        sql = f'SELECT COUNT(*) FROM "{cls._table_name()}"'  # noqa: S608
        return await pool.fetchval(sql)

    # -- Instance methods ----------------------------------------------------

    async def save(self) -> None:
        """Update the row identified by this instance's primary key.

        All non-PK fields are written. Raises :class:`ValueError` if the
        model has no primary-key field or if the PK value is ``None``.
        """
        pool = _get_pool()
        pk = self._pk_field()
        if pk is None:
            msg = f"{type(self).__name__} has no primary_key field"
            raise ValueError(msg)
        pk_value = getattr(self, pk)
        if pk_value is None:
            msg = "Cannot save a row without a primary key value. Use create() for new rows."
            raise ValueError(msg)

        fields = self._non_pk_fields()
        set_clauses = [f'"{f}" = ${i + 1}' for i, f in enumerate(fields)]
        values = [getattr(self, f) for f in fields]
        pk_placeholder = f"${len(fields) + 1}"

        sql = f'UPDATE "{self._table_name()}" SET {", ".join(set_clauses)} WHERE "{pk}" = {pk_placeholder}'
        await pool.execute(sql, *values, pk_value)

    async def delete(self) -> None:
        """Delete the row identified by this instance's primary key.

        Raises :class:`ValueError` if the model has no primary-key field or
        if the PK value is ``None``.
        """
        pool = _get_pool()
        pk = self._pk_field()
        if pk is None:
            msg = f"{type(self).__name__} has no primary_key field"
            raise ValueError(msg)
        pk_value = getattr(self, pk)
        if pk_value is None:
            msg = "Cannot delete a row without a primary key value."
            raise ValueError(msg)

        sql = f'DELETE FROM "{self._table_name()}" WHERE "{pk}" = $1'
        await pool.execute(sql, pk_value)
