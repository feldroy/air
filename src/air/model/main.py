"""AirModel: async ORM for Pydantic models and PostgreSQL.

Provides an async ORM built on asyncpg and Pydantic v2, with a
Django-inspired API for defining tables and performing CRUD operations
against PostgreSQL.

Example::

    from air import AirDB, AirModel, AirField


    class UnicornSighting(AirModel):
        id: int | None = AirField(default=None, primary_key=True)
        location: str
        sparkle_rating: int
        confirmed: bool = AirField(default=False)


    db = AirDB()
    app = air.Air(lifespan=db.lifespan("postgresql://..."))

    # Then in async handlers:
    await UnicornSighting.create(location="Rainbow Falls", sparkle_rating=11)
    sightings = await UnicornSighting.filter(confirmed=True)
    one = await UnicornSighting.get(id=1)
    all_rows = await UnicornSighting.all()
    count = await UnicornSighting.count()
    await db.create_tables()
"""

from __future__ import annotations

import inspect
import re
import tomllib
from contextlib import asynccontextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from types import UnionType
from typing import TYPE_CHECKING, Any, Self, get_args, get_origin
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

from air.field import ForeignKey, PrimaryKey

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pydantic.fields import FieldInfo

# ---------------------------------------------------------------------------
# Table prefix: auto-derived from module name or pyproject.toml
# ---------------------------------------------------------------------------

_GENERIC_MODULES = frozenset({"main", "app", "models", "__main__", "server"})


def _normalize_project_name(name: str) -> str:
    """Normalize a pyproject.toml project name for use as a table prefix.

    Strips common TLDs (.com, .org, .io, .net, .dev, .app), replaces
    dots and hyphens with underscores, and lowercases.
    """
    for tld in (".com", ".org", ".io", ".net", ".dev", ".app"):
        if name.endswith(tld):
            name = name[: -len(tld)]
            break
    return name.replace("-", "_").replace(".", "_").lower()


@lru_cache(maxsize=1)
def _read_project_name() -> str | None:
    """Walk up from CWD looking for pyproject.toml and return [project].name."""
    path = Path.cwd()
    for parent in [path, *path.parents]:
        toml_path = parent / "pyproject.toml"
        if toml_path.is_file():
            try:
                with Path(toml_path).open("rb") as f:
                    data = tomllib.load(f)
                return data.get("project", {}).get("name")
            except (OSError, tomllib.TOMLDecodeError, KeyError):
                return None
    return None


def _table_prefix(module_name: str) -> str:
    """Derive a table prefix from the module where a model is defined.

    For package modules (``myapp.models``), uses the top-level package
    name. For standalone files with generic names (``main.py``,
    ``app.py``, ``models.py``), falls back to the normalized project
    name from ``pyproject.toml``.
    """
    top_module = module_name.split(".", maxsplit=1)[0]
    if top_module not in _GENERIC_MODULES:
        return top_module
    project_name = _read_project_name()
    if project_name:
        return _normalize_project_name(project_name)
    return top_module


# ---------------------------------------------------------------------------
# Type mapping: Python types -> PostgreSQL column types
# ---------------------------------------------------------------------------

_PY_TO_PG: dict[type, str] = {
    str: "TEXT",
    int: "INTEGER",
    float: "DOUBLE PRECISION",
    bool: "BOOLEAN",
    datetime: "TIMESTAMP WITH TIME ZONE",
    UUID: "UUID",
}


def _pg_type(python_type: type) -> str:
    """Return the PostgreSQL column type string for a Python type.

    Raises:
        TypeError: If *python_type* has no entry in :data:`_PY_TO_PG`.
    """
    if python_type not in _PY_TO_PG:
        supported = ", ".join(t.__name__ for t in _PY_TO_PG)
        msg = f"No PostgreSQL type mapping for {python_type!r}. Supported types: {supported}"
        raise TypeError(msg)
    return _PY_TO_PG[python_type]


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
    return any(isinstance(m, PrimaryKey) for m in field_info.metadata)


def _get_foreign_key(field_info: FieldInfo) -> ForeignKey | None:
    for metadata in field_info.metadata:
        if isinstance(metadata, ForeignKey):
            return metadata
    return None


# ---------------------------------------------------------------------------
# Lookup operators (Django-style double-underscore)
# ---------------------------------------------------------------------------

# Maps suffix -> SQL operator for simple binary comparisons.
_LOOKUP_OPS: dict[str, str] = {
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
}


def _parse_kwargs(kwargs: dict[str, Any], *, start_idx: int = 1) -> tuple[list[str], list[Any]]:
    """Parse keyword arguments into SQL WHERE conditions and parameter values.

    Supports Django-style ``__`` lookups (gt, gte, lt, lte, contains,
    icontains, in, isnull) alongside plain equality.

    Returns:
        A ``(conditions, values)`` tuple. *conditions* is a list of SQL
        fragments like ``"sparkle_rating" > $1`` and *values* is the
        corresponding list of bind parameters. The two lists may differ in
        length because ``isnull`` produces a condition with no parameter.
    """
    conditions: list[str] = []
    values: list[Any] = []
    param_idx = start_idx  # asyncpg uses $1, $2, ...

    for key, value in kwargs.items():
        # Split off a lookup suffix if present.
        if "__" in key:
            field, lookup = key.rsplit("__", 1)
        else:
            field, lookup = key, "exact"

        if lookup == "exact":
            conditions.append(f'"{field}" = ${param_idx}')
            values.append(value)
            param_idx += 1
        elif lookup in _LOOKUP_OPS:
            conditions.append(f'"{field}" {_LOOKUP_OPS[lookup]} ${param_idx}')
            values.append(value)
            param_idx += 1
        elif lookup == "contains":
            conditions.append(f"\"{field}\" LIKE '%' || ${param_idx} || '%'")
            values.append(value)
            param_idx += 1
        elif lookup == "icontains":
            conditions.append(f"\"{field}\" ILIKE '%' || ${param_idx} || '%'")
            values.append(value)
            param_idx += 1
        elif lookup == "in":
            conditions.append(f'"{field}" = ANY(${param_idx})')
            values.append(value)
            param_idx += 1
        elif lookup == "isnull":
            if value:
                conditions.append(f'"{field}" IS NULL')
            else:
                conditions.append(f'"{field}" IS NOT NULL')
            # No parameter consumed.
        else:
            # Unknown lookup -- treat the whole key as a column name for
            # backward compatibility (e.g. a column that contains "__").
            conditions.append(f'"{key}" = ${param_idx}')
            values.append(value)
            param_idx += 1

    return conditions, values


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class MultipleObjectsReturned(Exception):  # noqa: N818
    """Raised by :meth:`AirModel.get` when the query matches more than one row."""


# ---------------------------------------------------------------------------
# Module-level current-db reference (set during lifespan)
# ---------------------------------------------------------------------------

_current_db: AirDB | None = None
_table_registry: list[type[AirModel]] = []
_current_connection: ContextVar[Any | None] = ContextVar("_current_connection", default=None)


def _set_current_db(db: AirDB | None) -> None:
    global _current_db
    _current_db = db


def _get_pool() -> Any:
    """Return the active transaction connection or the asyncpg pool.

    Raises:
        RuntimeError: If no database connection is active.
    """
    conn = _current_connection.get()
    if conn is not None:
        return conn
    if _current_db is None or _current_db.pool is None:
        msg = "No database connection. Ensure AirDB.lifespan() is active."
        raise RuntimeError(msg)
    return _current_db.pool


# ---------------------------------------------------------------------------
# ORM base class
# ---------------------------------------------------------------------------


class AirModel(BaseModel):
    """Base class for database-backed Pydantic models.

    Subclass this and declare fields using standard Pydantic annotations.
    Use :func:`AirField` with ``primary_key=True`` for auto-incrementing
    primary keys.

    The table name is derived from the class name (converted to snake_case). All query
    methods are async class methods.

    Example::

        class User(AirModel):
            id: int | None = AirField(default=None, primary_key=True)
            name: str
            email: str
    """

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        cls._validate_fk_relation_names()
        _table_registry.append(cls)

    # -- SQL generation helpers ----------------------------------------------

    @classmethod
    def _table_name(cls) -> str:
        prefix = _table_prefix(cls.__module__)
        snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", cls.__name__).lower()
        return f"{prefix}_{snake}"

    @classmethod
    def _pk_field(cls) -> str | None:
        """Return the name of the primary-key field, or None."""
        for name, info in cls.model_fields.items():
            if _is_primary_key(info):
                return name
        return None

    @staticmethod
    def _relation_attr_name(field_name: str) -> str:
        """Derive the eager-loading relation attribute from an FK field name."""
        if field_name.endswith("_id"):
            return field_name.removesuffix("_id")
        return f"{field_name}_obj"

    @classmethod
    def _relation_field_map(cls) -> dict[str, str]:
        """Map derived relation attribute names to their FK field names.

        Raises:
            ValueError: If a derived relation attribute would shadow an existing field or attribute.
        """
        relation_fields: dict[str, str] = {}
        for field_name, field_info in cls.model_fields.items():
            if _get_foreign_key(field_info) is None:
                continue
            relation_name = cls._relation_attr_name(field_name)
            if relation_name in cls.model_fields:
                msg = (
                    f'Foreign key field "{field_name}" derives relation attribute '
                    f'"{relation_name}", which collides with existing field "{relation_name}".'
                )
                raise ValueError(msg)
            marker = object()
            existing = inspect.getattr_static(cls, relation_name, marker)
            if existing is not marker:
                msg = (
                    f'Foreign key field "{field_name}" derives relation attribute '
                    f'"{relation_name}", which collides with existing model attribute '
                    f'"{relation_name}".'
                )
                raise ValueError(msg)
            relation_fields[relation_name] = field_name
        return relation_fields

    @classmethod
    def _validate_fk_relation_names(cls) -> None:
        """Reject FK relation names that would shadow model attributes."""
        cls._relation_field_map()

    @classmethod
    def _column_defs(cls) -> list[str]:
        """Return a list of ``"column_name TYPE [constraints]"`` strings."""
        cols: list[str] = []
        for field_name, field_info in cls.model_fields.items():
            annotation = field_info.annotation
            is_pk = _is_primary_key(field_info)

            if is_pk:
                cols.append(f'"{field_name}" BIGSERIAL PRIMARY KEY')
                continue

            # Determine the base Python type (unwrap Optional if needed)
            base_type = _unwrap_optional(annotation) if _is_optional(annotation) else annotation

            pg_type = _pg_type(base_type)

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
    def _add_column_sql(cls, field_name: str) -> str:
        """Generate an ``ALTER TABLE ADD COLUMN`` statement for a single field.

        Never includes ``NOT NULL``, even for required fields, because
        existing rows have no value for the new column.
        """
        field_info = cls.model_fields[field_name]
        annotation = field_info.annotation
        base_type = _unwrap_optional(annotation) if _is_optional(annotation) else annotation
        pg_type = _pg_type(base_type)
        return f'ALTER TABLE "{cls._table_name()}" ADD COLUMN "{field_name}" {pg_type}'

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

        sql = f'INSERT INTO "{cls._table_name()}" ({columns}) VALUES ({placeholders}) RETURNING *'
        row = await pool.fetchrow(sql, *values)
        return cls.model_validate(dict(row))

    @classmethod
    async def get(cls, **kwargs: Any) -> Self | None:
        """Fetch exactly one row matching the given keyword filters.

        Supports Django-style ``__`` lookups (gt, gte, lt, lte, contains,
        icontains, in, isnull) in addition to plain equality.

        Returns:
            An instance of this Model subclass, or ``None`` if no row matches.

        Raises:
            MultipleObjectsReturned: If more than one row matches the filters.
        """
        pool = _get_pool()
        conditions, values = _parse_kwargs(kwargs)
        where = " AND ".join(conditions)
        sql = f'SELECT * FROM "{cls._table_name()}" WHERE {where} LIMIT 2'
        rows = await pool.fetch(sql, *values)
        if not rows:
            return None
        if len(rows) > 1:
            msg = f"{cls.__name__}.get() matched more than one row. Use filter() to retrieve multiple results."
            raise MultipleObjectsReturned(msg)
        return cls.model_validate(dict(rows[0]))

    @classmethod
    async def filter(
        cls,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        **kwargs: Any,
    ) -> list[Self]:
        """Fetch all rows matching the given keyword filters.

        Supports Django-style ``__`` lookups (gt, gte, lt, lte, contains,
        icontains, in, isnull) in addition to plain equality.

        Args:
            order_by: Optional field name to sort by. Prefix with ``-`` for
                descending order (e.g. ``"-name"``).
            limit: Maximum number of rows to return.
            offset: Number of rows to skip before returning results.
            **kwargs: Column name/value pairs to filter by, with optional
                ``__lookup`` suffixes.

        Returns:
            A list of model instances (possibly empty).
        """
        pool = _get_pool()
        if not kwargs:
            return await cls.all(order_by=order_by, limit=limit, offset=offset)
        conditions, values = _parse_kwargs(kwargs)
        where = " AND ".join(conditions)
        sql = f'SELECT * FROM "{cls._table_name()}" WHERE {where}'
        if order_by is not None:
            if order_by.startswith("-"):
                sql += f' ORDER BY "{order_by[1:]}" DESC'
            else:
                sql += f' ORDER BY "{order_by}" ASC'
        if limit is not None:
            sql += f" LIMIT {limit}"
        if offset is not None:
            sql += f" OFFSET {offset}"
        rows = await pool.fetch(sql, *values)
        return [cls.model_validate(dict(r)) for r in rows]

    @classmethod
    async def all(
        cls,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Self]:
        """Fetch every row from the table.

        Args:
            order_by: Optional field name to sort by. Prefix with ``-`` for
                descending order (e.g. ``"-name"``).
            limit: Maximum number of rows to return.
            offset: Number of rows to skip before returning results.

        Returns:
            A list of all model instances.
        """
        pool = _get_pool()
        sql = f'SELECT * FROM "{cls._table_name()}"'
        if order_by is not None:
            if order_by.startswith("-"):
                sql += f' ORDER BY "{order_by[1:]}" DESC'
            else:
                sql += f' ORDER BY "{order_by}" ASC'
        if limit is not None:
            sql += f" LIMIT {limit}"
        if offset is not None:
            sql += f" OFFSET {offset}"
        rows = await pool.fetch(sql)
        return [cls.model_validate(dict(r)) for r in rows]

    @classmethod
    async def count(cls, **kwargs: Any) -> int:
        """Return the number of rows, optionally filtered by keyword arguments.

        Supports Django-style ``__`` lookups (gt, gte, lt, lte, contains,
        icontains, in, isnull) in addition to plain equality.

        Returns:
            Integer row count.
        """
        pool = _get_pool()
        if kwargs:
            conditions, values = _parse_kwargs(kwargs)
            where = " AND ".join(conditions)
            sql = f'SELECT COUNT(*) FROM "{cls._table_name()}" WHERE {where}'
            return await pool.fetchval(sql, *values)
        sql = f'SELECT COUNT(*) FROM "{cls._table_name()}"'
        return await pool.fetchval(sql)

    # -- Bulk class methods ---------------------------------------------------

    @classmethod
    async def bulk_create(cls, items: list[dict[str, Any]]) -> list[Self]:
        """Insert multiple rows in a single query and return the new instances.

        Builds a multi-row INSERT with ``RETURNING *`` so only one round-trip
        is needed regardless of list length.

        Args:
            items: A list of dicts, each mapping column names to values.

        Returns:
            A list of model instances, one per inserted row.
        """
        if not items:
            return []

        pool = _get_pool()
        fields = cls._non_pk_fields()
        # Use the columns present in the first item (all items must have the same keys)
        insert_fields = [f for f in fields if f in items[0]]
        columns = ", ".join(f'"{f}"' for f in insert_fields)

        # Build ($1, $2), ($3, $4), ... with flattened parameter list
        value_groups: list[str] = []
        all_values: list[Any] = []
        for i, item in enumerate(items):
            offset = i * len(insert_fields)
            placeholders = ", ".join(f"${offset + j + 1}" for j in range(len(insert_fields)))
            value_groups.append(f"({placeholders})")
            all_values.extend(item[f] for f in insert_fields)

        values_sql = ", ".join(value_groups)
        sql = f'INSERT INTO "{cls._table_name()}" ({columns}) VALUES {values_sql} RETURNING *'
        rows = await pool.fetch(sql, *all_values)
        return [cls.model_validate(dict(r)) for r in rows]

    @classmethod
    async def bulk_update(cls, set_values: dict[str, Any], **filter_kwargs: Any) -> int:
        """Update multiple rows matching the filter and return the count affected.

        Args:
            set_values: A dict of column names to new values for the SET clause.
            **filter_kwargs: Column name/value pairs (with optional ``__lookup``
                suffixes) for the WHERE clause.

        Returns:
            The number of rows updated.
        """
        pool = _get_pool()
        set_clauses = [f'"{col}" = ${i + 1}' for i, col in enumerate(set_values)]
        set_sql = ", ".join(set_clauses)
        set_params = list(set_values.values())

        conditions, where_params = _parse_kwargs(filter_kwargs, start_idx=len(set_values) + 1)
        where_sql = " AND ".join(conditions)

        sql = f'UPDATE "{cls._table_name()}" SET {set_sql} WHERE {where_sql}'
        status = await pool.execute(sql, *set_params, *where_params)
        # asyncpg returns e.g. "UPDATE 3"
        return int(status.split()[-1])

    @classmethod
    async def bulk_delete(cls, **filter_kwargs: Any) -> int:
        """Delete all rows matching the filter and return the count deleted.

        Args:
            **filter_kwargs: Column name/value pairs (with optional ``__lookup``
                suffixes) for the WHERE clause.

        Returns:
            The number of rows deleted.
        """
        pool = _get_pool()
        conditions, values = _parse_kwargs(filter_kwargs)
        where_sql = " AND ".join(conditions)

        sql = f'DELETE FROM "{cls._table_name()}" WHERE {where_sql}'
        status = await pool.execute(sql, *values)
        # asyncpg returns e.g. "DELETE 5"
        return int(status.split()[-1])

    # -- Instance methods ----------------------------------------------------

    async def save(self, *, update_fields: list[str] | None = None) -> None:
        """Update the row identified by this instance's primary key.

        All non-PK fields are written.

        Raises:
            ValueError: If the model has no primary-key field, the PK
                value is ``None``, or *update_fields* is an empty list.
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

        if update_fields is not None and len(update_fields) == 0:
            msg = "update_fields cannot be empty. Omit the argument to update all fields."
            raise ValueError(msg)

        fields = update_fields if update_fields is not None else self._non_pk_fields()
        set_clauses = [f'"{f}" = ${i + 1}' for i, f in enumerate(fields)]
        values = [getattr(self, f) for f in fields]
        pk_placeholder = f"${len(fields) + 1}"

        sql = f'UPDATE "{self._table_name()}" SET {", ".join(set_clauses)} WHERE "{pk}" = {pk_placeholder} RETURNING *'
        row = await pool.fetchrow(sql, *values, pk_value)
        for field_name in type(self).model_fields:
            if field_name in row:
                object.__setattr__(self, field_name, row[field_name])  # noqa: PLC2801

    async def delete(self) -> None:
        """Delete the row identified by this instance's primary key.

        Raises:
            ValueError: If the model has no primary-key field or
                the PK value is ``None``.
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
        object.__setattr__(self, pk, None)  # noqa: PLC2801


# ---------------------------------------------------------------------------
# AirDB: connection pool + table management
# ---------------------------------------------------------------------------


async def _get_existing_columns(pool: Any, table_name: str) -> set[str]:
    """Query ``information_schema.columns`` for a table's current column names."""
    rows = await pool.fetch(
        "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = $1",
        table_name,
    )
    return {row["column_name"] for row in rows}


class AirDB:
    """Manages an asyncpg connection pool for :class:`AirModel` subclasses.

    Example::

        db = AirDB()
        app = air.Air(lifespan=db.lifespan("postgresql://user:pass@host/dbname"))
    """

    def __init__(self) -> None:
        self.pool: Any | None = None  # asyncpg.Pool once connected

    # -- connection lifecycle ------------------------------------------------

    def connect(self, pool: Any) -> None:
        """Set the connection pool and register this as the active database.

        In production, called automatically by :meth:`lifespan`. In tests,
        call directly with a mock pool::

            db = AirDB()
            db.connect(fake_pool)
        """
        self.pool = pool
        _set_current_db(self)

    def disconnect(self) -> None:
        """Unregister this database and clear the pool reference.

        In production, called automatically by :meth:`lifespan`. In tests,
        call in teardown::

            db.disconnect()
        """
        self.pool = None
        _set_current_db(None)

    def lifespan(self, url: str, **pool_kwargs: Any) -> Any:
        """Return an async context manager suitable for ASGI lifespan.

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

            pool = await asyncpg.create_pool(url, **pool_kwargs)
            db.connect(pool)
            try:
                yield
            finally:
                if db.pool is not None:
                    await db.pool.close()
                db.disconnect()

        return _lifespan

    # -- transactions --------------------------------------------------------

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """Async context manager that wraps a block in a database transaction.

        Acquires a connection from the pool, starts a transaction on it, and
        routes all CRUD operations inside the block through that connection
        instead of the pool.

        On clean exit the transaction is committed. If an exception propagates
        out of the block, the transaction is rolled back and the exception is
        re-raised.

        Raises:
            RuntimeError: If no database connection is active.

        Example::

            async with db.transaction():
                await Item.create(name="a")
                await Item.create(name="b")  # atomic with the first
        """
        pool = self.pool
        if pool is None:
            msg = "No database connection. Ensure AirDB.lifespan() is active."
            raise RuntimeError(msg)
        async with pool.acquire() as conn:
            txn = conn.transaction()
            await txn.start()
            token = _current_connection.set(conn)
            try:
                yield
                await txn.commit()
            except BaseException:
                await txn.rollback()
                raise
            finally:
                _current_connection.reset(token)

    # -- table management ----------------------------------------------------

    async def create_tables(self) -> None:
        """Create or migrate tables for every registered :class:`AirModel`.

        For each model, runs ``CREATE TABLE IF NOT EXISTS`` and then
        ``ALTER TABLE ADD COLUMN`` for any model fields not yet present
        in the database. Non-destructive: never drops columns, never
        changes types. New columns are added without ``NOT NULL`` so
        existing rows aren't broken.

        Raises:
            RuntimeError: If the database pool is not initialized.
        """
        if self.pool is None:
            msg = "Database pool is not initialized. Did you forget to use db.lifespan()?"
            raise RuntimeError(msg)
        for table_cls in _table_registry:
            sql = table_cls._create_table_sql()
            await self.pool.execute(sql)

            existing = await _get_existing_columns(self.pool, table_cls._table_name())
            if not existing:
                continue

            pk = table_cls._pk_field()
            for field_name in table_cls.model_fields:
                if field_name == pk:
                    continue
                if field_name not in existing:
                    await self.pool.execute(table_cls._add_column_sql(field_name))
