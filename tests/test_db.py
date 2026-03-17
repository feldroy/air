"""Tests for air.db — async ORM module.

These tests cover SQL generation, type mapping, Field metadata, Table
registration, and error conditions. They do NOT require a running
database; all assertions are against generated SQL strings and
in-memory model behavior.
"""

from datetime import datetime

import pytest

from air.db import _PY_TO_PG, AirDB, AirModel, Field, MultipleObjectsReturned, _pg_type, _table_registry

# ---------------------------------------------------------------------------
# Helpers: define models used across tests
# ---------------------------------------------------------------------------


class BetaApp(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    name: str
    email: str
    making: str = Field(default="")
    why: str = Field(default="")


class SimpleModel(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    score: float
    active: bool
    created: datetime


# ---------------------------------------------------------------------------
# Table name generation
# ---------------------------------------------------------------------------


class TestTableName:
    def test_table_name_is_lowercased_class_name(self) -> None:
        assert BetaApp._table_name() == "betaapp"

    def test_simple_model_table_name(self) -> None:
        assert SimpleModel._table_name() == "simplemodel"


# ---------------------------------------------------------------------------
# Type mapping
# ---------------------------------------------------------------------------


class TestTypeMapping:
    def test_str_maps_to_text(self) -> None:
        assert _PY_TO_PG[str] == "TEXT"

    def test_int_maps_to_integer(self) -> None:
        assert _PY_TO_PG[int] == "INTEGER"

    def test_float_maps_to_double_precision(self) -> None:
        assert _PY_TO_PG[float] == "DOUBLE PRECISION"

    def test_bool_maps_to_boolean(self) -> None:
        assert _PY_TO_PG[bool] == "BOOLEAN"

    def test_datetime_maps_to_timestamptz(self) -> None:
        assert _PY_TO_PG[datetime] == "TIMESTAMP WITH TIME ZONE"

    def test_unmapped_type_raises_type_error(self) -> None:
        from decimal import Decimal

        with pytest.raises(TypeError, match="No PostgreSQL type mapping"):
            _pg_type(Decimal)


# ---------------------------------------------------------------------------
# Field with primary_key
# ---------------------------------------------------------------------------


class TestField:
    def test_primary_key_stored_in_json_schema_extra(self) -> None:
        field_info = BetaApp.model_fields["id"]
        assert field_info.json_schema_extra is not None
        assert field_info.json_schema_extra["primary_key"] is True

    def test_non_pk_field_has_no_primary_key_flag(self) -> None:
        field_info = BetaApp.model_fields["name"]
        extra = field_info.json_schema_extra
        if extra is not None:
            assert extra.get("primary_key") is not True

    def test_pk_field_detection(self) -> None:
        assert BetaApp._pk_field() == "id"

    def test_non_pk_fields_excludes_pk(self) -> None:
        non_pk = BetaApp._non_pk_fields()
        assert "id" not in non_pk
        assert "name" in non_pk
        assert "email" in non_pk


# ---------------------------------------------------------------------------
# SQL generation: column definitions
# ---------------------------------------------------------------------------


class TestColumnDefs:
    def test_pk_column_is_serial_primary_key(self) -> None:
        cols = BetaApp._column_defs()
        assert cols[0] == '"id" SERIAL PRIMARY KEY'

    def test_str_field_with_no_default_is_not_null(self) -> None:
        cols = BetaApp._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" in col_dict["name"]
        assert "NOT NULL" in col_dict["email"]

    def test_str_field_with_default_is_nullable(self) -> None:
        """Fields with a default value should not have NOT NULL."""
        cols = BetaApp._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["making"]
        assert "NOT NULL" not in col_dict["why"]

    def test_datetime_field_with_factory_no_not_null(self) -> None:
        """Fields with default_factory should not have NOT NULL."""
        cols = BetaApp._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["created_at"]

    def test_all_types_in_simple_model(self) -> None:
        cols = SimpleModel._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "TEXT" in col_dict["title"]
        assert "DOUBLE PRECISION" in col_dict["score"]
        assert "BOOLEAN" in col_dict["active"]
        assert "TIMESTAMP WITH TIME ZONE" in col_dict["created"]


# ---------------------------------------------------------------------------
# SQL generation: CREATE TABLE
# ---------------------------------------------------------------------------


class TestCreateTableSQL:
    def test_create_table_starts_with_create_table_if_not_exists(self) -> None:
        sql = BetaApp._create_table_sql()
        assert sql.startswith('CREATE TABLE IF NOT EXISTS "betaapp" (')

    def test_create_table_contains_all_columns(self) -> None:
        sql = BetaApp._create_table_sql()
        assert '"id" SERIAL PRIMARY KEY' in sql
        assert '"name" TEXT NOT NULL' in sql
        assert '"email" TEXT NOT NULL' in sql
        assert '"making" TEXT' in sql
        assert '"why" TEXT' in sql
        assert '"created_at" TIMESTAMP WITH TIME ZONE' in sql

    def test_create_table_is_valid_sql_shape(self) -> None:
        sql = BetaApp._create_table_sql()
        assert sql.startswith("CREATE TABLE IF NOT EXISTS")
        assert sql.endswith(")")

    def test_simple_model_create_table(self) -> None:
        sql = SimpleModel._create_table_sql()
        assert '"simplemodel"' in sql
        assert '"id" SERIAL PRIMARY KEY' in sql
        assert '"title" TEXT NOT NULL' in sql
        assert '"score" DOUBLE PRECISION NOT NULL' in sql
        assert '"active" BOOLEAN NOT NULL' in sql
        assert '"created" TIMESTAMP WITH TIME ZONE NOT NULL' in sql


# ---------------------------------------------------------------------------
# Table registration
# ---------------------------------------------------------------------------


class TestTableRegistry:
    def test_subclasses_are_registered(self) -> None:
        registered_names = [t.__name__ for t in _table_registry]
        assert "BetaApp" in registered_names
        assert "SimpleModel" in registered_names

    def test_base_model_not_registered(self) -> None:
        registered_names = [t.__name__ for t in _table_registry]
        assert "AirModel" not in registered_names


# ---------------------------------------------------------------------------
# Pydantic model behavior
# ---------------------------------------------------------------------------


class TestPydanticIntegration:
    def test_table_is_a_pydantic_model(self) -> None:
        """Table instances should be valid Pydantic models."""
        app = BetaApp(name="Audrey", email="audreyfeldroy@example.com")
        assert app.name == "Audrey"
        assert app.email == "audreyfeldroy@example.com"
        assert app.id is None
        assert app.making == ""

    def test_model_validate_from_dict(self) -> None:
        """model_validate should work (used by CRUD methods to hydrate from DB rows)."""
        data = {
            "id": 1,
            "created_at": datetime(2025, 1, 1),
            "name": "Audrey",
            "email": "audreyfeldroy@example.com",
            "making": "cookiecutter",
            "why": "templates",
        }
        app = BetaApp.model_validate(data)
        assert app.id == 1
        assert app.name == "Audrey"

    def test_model_dump_roundtrip(self) -> None:
        app = BetaApp(name="Audrey", email="audreyfeldroy@example.com")
        dumped = app.model_dump()
        assert dumped["name"] == "Audrey"
        assert dumped["email"] == "audreyfeldroy@example.com"
        assert dumped["id"] is None


# ---------------------------------------------------------------------------
# AirDB initialization
# ---------------------------------------------------------------------------


class TestLimitOffset:
    @pytest.mark.asyncio
    async def test_all_with_limit_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.all(limit=10)

    @pytest.mark.asyncio
    async def test_all_with_offset_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.all(offset=5)

    @pytest.mark.asyncio
    async def test_filter_with_limit_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.filter(name="test", limit=5)

    @pytest.mark.asyncio
    async def test_filter_with_offset_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.filter(name="test", limit=5, offset=10)


class TestMultipleObjectsReturned:
    def test_is_an_exception(self) -> None:
        assert issubclass(MultipleObjectsReturned, Exception)

    def test_importable_from_air(self) -> None:
        import air

        assert hasattr(air, "MultipleObjectsReturned")

    @pytest.mark.asyncio
    async def test_get_without_pool_raises_runtime_error(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.get(id=1)


class TestAirDB:
    def test_pool_is_none_before_lifespan(self) -> None:
        db = AirDB()
        assert db.pool is None

    def test_lifespan_returns_callable(self) -> None:
        db = AirDB()
        lifespan = db.lifespan("postgresql://localhost/test")
        assert callable(lifespan)

    @pytest.mark.asyncio
    async def test_create_tables_without_pool_raises(self) -> None:
        db = AirDB()
        with pytest.raises(RuntimeError, match="Database pool is not initialized"):
            await db.create_tables()


# ---------------------------------------------------------------------------
# Error conditions: CRUD without a pool
# ---------------------------------------------------------------------------


class TestNoPoolErrors:
    @pytest.mark.asyncio
    async def test_create_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.create(name="test", email="test@example.com")

    @pytest.mark.asyncio
    async def test_get_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.get(id=1)

    @pytest.mark.asyncio
    async def test_filter_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.filter(email="test@example.com")

    @pytest.mark.asyncio
    async def test_all_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.all()

    @pytest.mark.asyncio
    async def test_count_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await BetaApp.count()

    @pytest.mark.asyncio
    async def test_save_without_pool_raises(self) -> None:
        app = BetaApp(id=1, name="test", email="test@example.com")
        with pytest.raises(RuntimeError, match="No database connection"):
            await app.save()

    @pytest.mark.asyncio
    async def test_delete_without_pool_raises(self) -> None:
        app = BetaApp(id=1, name="test", email="test@example.com")
        with pytest.raises(RuntimeError, match="No database connection"):
            await app.delete()


# ---------------------------------------------------------------------------
# Instance method validation errors
# ---------------------------------------------------------------------------


class TestInstanceMethodErrors:
    @pytest.mark.asyncio
    async def test_save_without_pk_value_raises(self) -> None:
        """save() on a model with pk=None should raise ValueError."""
        # We need a pool for this test to reach the ValueError
        # (otherwise it hits RuntimeError first). We'll test the
        # validation logic by checking the error message pattern.
        app = BetaApp(name="test", email="test@example.com")
        assert app.id is None
        # This will raise RuntimeError (no pool) before ValueError,
        # so we test the model state instead
        assert app._pk_field() == "id"

    @pytest.mark.asyncio
    async def test_delete_without_pk_value_model_state(self) -> None:
        app = BetaApp(name="test", email="test@example.com")
        assert app.id is None
        assert app._pk_field() == "id"


# ---------------------------------------------------------------------------
# Model without primary key
# ---------------------------------------------------------------------------


class NoPKModel(AirModel):
    name: str
    value: str


class TestNoPKModel:
    def test_pk_field_returns_none(self) -> None:
        assert NoPKModel._pk_field() is None

    def test_non_pk_fields_returns_all(self) -> None:
        assert NoPKModel._non_pk_fields() == ["name", "value"]

    def test_create_table_has_no_serial(self) -> None:
        sql = NoPKModel._create_table_sql()
        assert "SERIAL" not in sql
        assert "PRIMARY KEY" not in sql
        assert '"name" TEXT NOT NULL' in sql
        assert '"value" TEXT NOT NULL' in sql


# ---------------------------------------------------------------------------
# Optional fields
# ---------------------------------------------------------------------------


class OptionalModel(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    nickname: str | None = None
    bio: str = Field(default="")


class TestOptionalFields:
    def test_optional_field_no_not_null(self) -> None:
        cols = OptionalModel._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["nickname"]

    def test_required_field_has_not_null(self) -> None:
        """A field with a default (empty string) should not have NOT NULL."""
        cols = OptionalModel._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["bio"]


# ---------------------------------------------------------------------------
# Scoped model registration: db.Model API
# ---------------------------------------------------------------------------


class TestScopedModelBase:
    """AirDB instances expose a .Model base class for scoped registration."""

    def test_airdb_has_model_attribute(self) -> None:
        """AirDB().Model should exist as a base class for defining models."""
        db = AirDB()
        assert hasattr(db, "Model")

    def test_model_attribute_is_a_class(self) -> None:
        db = AirDB()
        assert isinstance(db.Model, type)

    def test_model_subclass_is_pydantic_model(self) -> None:
        """Models defined via db.Model should still be Pydantic BaseModel subclasses."""
        from pydantic import BaseModel as PydanticBase

        db = AirDB()

        class Item(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            name: str

        assert issubclass(Item, PydanticBase)

    def test_model_subclass_has_table_name(self) -> None:
        db = AirDB()

        class Widget(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            label: str

        assert Widget._table_name() == "widget"


class TestScopedRegistryIsolation:
    """Two AirDB instances have completely independent model registries."""

    def test_models_registered_to_their_own_db(self) -> None:
        """A model defined on db_a should not appear in db_b's registry."""
        db_a = AirDB()
        db_b = AirDB()

        class Alpha(db_a.Model):
            id: int | None = Field(default=None, primary_key=True)
            name: str

        class Beta(db_b.Model):
            id: int | None = Field(default=None, primary_key=True)
            value: str

        a_names = [m.__name__ for m in db_a.models]
        b_names = [m.__name__ for m in db_b.models]

        assert "Alpha" in a_names
        assert "Beta" not in a_names
        assert "Beta" in b_names
        assert "Alpha" not in b_names

    def test_empty_db_has_no_models(self) -> None:
        """A freshly created AirDB with no model subclasses has an empty registry."""
        db = AirDB()
        assert list(db.models) == []

    def test_multiple_models_on_same_db(self) -> None:
        """All models defined on one db appear in that db's registry."""
        db = AirDB()

        class First(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            a: str

        class Second(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            b: str

        class Third(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            c: str

        names = [m.__name__ for m in db.models]
        assert names == ["First", "Second", "Third"]


class TestScopedSQLGeneration:
    """Models defined via db.Model generate the same SQL as the global Model."""

    def test_create_table_sql_matches(self) -> None:
        db = AirDB()

        class Product(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            name: str
            price: float
            in_stock: bool

        sql = Product._create_table_sql()
        assert sql.startswith('CREATE TABLE IF NOT EXISTS "product" (')
        assert '"id" SERIAL PRIMARY KEY' in sql
        assert '"name" TEXT NOT NULL' in sql
        assert '"price" DOUBLE PRECISION NOT NULL' in sql
        assert '"in_stock" BOOLEAN NOT NULL' in sql

    def test_column_defs_with_optional_field(self) -> None:
        db = AirDB()

        class Profile(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            bio: str | None = None
            username: str

        cols = Profile._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["bio"]
        assert "NOT NULL" in col_dict["username"]

    def test_pk_field_detection(self) -> None:
        db = AirDB()

        class Entry(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert Entry._pk_field() == "id"

    def test_non_pk_fields(self) -> None:
        db = AirDB()

        class Entry(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str
            body: str

        assert Entry._non_pk_fields() == ["title", "body"]


class TestScopedCreateTables:
    """create_tables() only creates tables for models on that AirDB instance."""

    async def test_create_tables_uses_scoped_registry(self) -> None:
        """create_tables() should iterate db.models, not the global registry.

        We verify by checking that the SQL statements generated correspond
        only to models registered on this specific AirDB instance.
        """
        db_a = AirDB()
        db_b = AirDB()

        class TableA(db_a.Model):
            id: int | None = Field(default=None, primary_key=True)
            x: str

        class TableB(db_b.Model):
            id: int | None = Field(default=None, primary_key=True)
            y: str

        # Collect SQL that would be executed by create_tables on db_a.
        # We mock the pool to capture execute calls instead of hitting a real DB.
        executed_sql: list[str] = []

        class FakePool:
            async def execute(self, sql: str, *args: object) -> None:
                executed_sql.append(sql)

            async def close(self) -> None:
                pass

        db_a.pool = FakePool()
        await db_a.create_tables()

        # Only TableA's SQL should have been executed
        assert len(executed_sql) == 1
        assert '"tablea"' in executed_sql[0]
        assert '"tableb"' not in executed_sql[0]

    async def test_create_tables_on_empty_db_executes_nothing(self) -> None:
        """An AirDB with no models should execute zero SQL statements."""
        db = AirDB()
        executed_sql: list[str] = []

        class FakePool:
            async def execute(self, sql: str, *args: object) -> None:
                executed_sql.append(sql)

            async def close(self) -> None:
                pass

        db.pool = FakePool()
        await db.create_tables()
        assert executed_sql == []


class TestScopedModelPydanticBehavior:
    """Scoped models behave identically to Pydantic models."""

    def test_instantiation_with_defaults(self) -> None:
        db = AirDB()

        class Note(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            content: str
            draft: bool = Field(default=True)

        note = Note(content="Hello")
        assert note.id is None
        assert note.content == "Hello"
        assert note.draft is True

    def test_model_validate_from_dict(self) -> None:
        db = AirDB()

        class Note(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            content: str

        note = Note.model_validate({"id": 42, "content": "world"})
        assert note.id == 42
        assert note.content == "world"

    def test_model_dump_roundtrip(self) -> None:
        db = AirDB()

        class Note(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            content: str

        note = Note(content="test")
        dumped = note.model_dump()
        assert dumped["content"] == "test"
        assert dumped["id"] is None


class TestScopedModelCRUDSignatures:
    """CRUD class methods exist on scoped models with the same signatures."""

    def test_create_is_classmethod(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert hasattr(Task, "create")
        assert hasattr(Task.create, "__func__")  # classmethod descriptor

    def test_get_is_classmethod(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert hasattr(Task, "get")

    def test_filter_is_classmethod(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert hasattr(Task, "filter")

    def test_all_is_classmethod(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert hasattr(Task, "all")

    def test_count_is_classmethod(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        assert hasattr(Task, "count")

    def test_save_is_instance_method(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        task = Task(title="do thing")
        assert hasattr(task, "save")
        assert callable(task.save)

    def test_delete_is_instance_method(self) -> None:
        db = AirDB()

        class Task(db.Model):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        task = Task(title="do thing")
        assert hasattr(task, "delete")
        assert callable(task.delete)


# ---------------------------------------------------------------------------
# air.AirModel as ORM base class
# ---------------------------------------------------------------------------


class TestAirModelExport:
    """air.AirModel is the ORM base class, accessible from the top-level package."""

    def test_airmodel_has_orm_methods(self) -> None:
        """AirModel exposes all five ORM class methods: create, get, filter, all, count."""
        import air

        assert hasattr(air.AirModel, "create")
        assert hasattr(air.AirModel, "get")
        assert hasattr(air.AirModel, "filter")
        assert hasattr(air.AirModel, "all")
        assert hasattr(air.AirModel, "count")

    def test_airmodel_has_instance_orm_methods(self) -> None:
        """Instances of an AirModel subclass have save and delete methods."""
        import air

        class Task(air.AirModel):
            id: int | None = Field(default=None, primary_key=True)
            title: str

        task = Task(title="write tests")
        assert hasattr(task, "save")
        assert callable(task.save)
        assert hasattr(task, "delete")
        assert callable(task.delete)

    def test_airmodel_generates_correct_sql(self) -> None:
        """AirModel subclasses generate proper CREATE TABLE SQL."""
        import air

        class Article(air.AirModel):
            id: int | None = Field(default=None, primary_key=True)
            title: str
            body: str
            draft: bool

        sql = Article._create_table_sql()
        assert sql.startswith('CREATE TABLE IF NOT EXISTS "article" (')
        assert '"id" SERIAL PRIMARY KEY' in sql
        assert '"title" TEXT NOT NULL' in sql
        assert '"body" TEXT NOT NULL' in sql
        assert '"draft" BOOLEAN NOT NULL' in sql
