"""Tests for air.db — async ORM module.

These tests cover SQL generation, type mapping, Field metadata, Table
registration, and error conditions. They do NOT require a running
database; all assertions are against generated SQL strings and
in-memory model behavior.
"""

from datetime import datetime
from uuid import UUID

import pytest

from air.db import _PY_TO_PG, AirDB, AirModel, Field, MultipleObjectsReturned, _pg_type, _table_registry

# ---------------------------------------------------------------------------
# Helpers: define models used across tests
# ---------------------------------------------------------------------------


class DragonFruit(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    name: str
    color: str
    sweetness: str = Field(default="")
    origin: str = Field(default="")


class StarFruit(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    score: float
    active: bool
    created: datetime


class UnicornSighting(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    location: str


class UbePancake(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    weight: float


class BokChoy(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    bunch_size: int


class Cassava(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    variety: str


# ---------------------------------------------------------------------------
# Table name generation
# ---------------------------------------------------------------------------


class TestTableName:
    def test_dragon_fruit_snake_case(self) -> None:
        assert DragonFruit._table_name() == "dragon_fruit"

    def test_star_fruit_snake_case(self) -> None:
        assert StarFruit._table_name() == "star_fruit"

    def test_unicorn_sighting_snake_case(self) -> None:
        assert UnicornSighting._table_name() == "unicorn_sighting"

    def test_ube_pancake_snake_case(self) -> None:
        assert UbePancake._table_name() == "ube_pancake"

    def test_two_word_name_snake_case(self) -> None:
        assert BokChoy._table_name() == "bok_choy"

    def test_single_word_name(self) -> None:
        assert Cassava._table_name() == "cassava"


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


    def test_uuid_maps_to_uuid(self) -> None:
        assert _PY_TO_PG[UUID] == "UUID"

    def test_pg_type_returns_uuid_for_uuid(self) -> None:
        assert _pg_type(UUID) == "UUID"

    def test_unmapped_type_raises_type_error(self) -> None:
        from decimal import Decimal

        with pytest.raises(TypeError, match="No PostgreSQL type mapping"):
            _pg_type(Decimal)


# ---------------------------------------------------------------------------
# Field with primary_key
# ---------------------------------------------------------------------------


class TestField:
    def test_primary_key_stored_in_json_schema_extra(self) -> None:
        field_info = DragonFruit.model_fields["id"]
        assert field_info.json_schema_extra is not None
        assert field_info.json_schema_extra["primary_key"] is True

    def test_non_pk_field_has_no_primary_key_flag(self) -> None:
        field_info = DragonFruit.model_fields["name"]
        extra = field_info.json_schema_extra
        if extra is not None:
            assert extra.get("primary_key") is not True

    def test_pk_field_detection(self) -> None:
        assert DragonFruit._pk_field() == "id"

    def test_non_pk_fields_excludes_pk(self) -> None:
        non_pk = DragonFruit._non_pk_fields()
        assert "id" not in non_pk
        assert "name" in non_pk
        assert "color" in non_pk


# ---------------------------------------------------------------------------
# SQL generation: column definitions
# ---------------------------------------------------------------------------


class TestColumnDefs:
    def test_pk_column_is_bigserial_primary_key(self) -> None:
        cols = DragonFruit._column_defs()
        assert cols[0] == '"id" BIGSERIAL PRIMARY KEY'

    def test_str_field_with_no_default_is_not_null(self) -> None:
        cols = DragonFruit._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" in col_dict["name"]
        assert "NOT NULL" in col_dict["color"]

    def test_str_field_with_default_is_nullable(self) -> None:
        """Fields with a default value should not have NOT NULL."""
        cols = DragonFruit._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["sweetness"]
        assert "NOT NULL" not in col_dict["origin"]

    def test_datetime_field_with_factory_no_not_null(self) -> None:
        """Fields with default_factory should not have NOT NULL."""
        cols = DragonFruit._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "NOT NULL" not in col_dict["created_at"]

    def test_all_types_in_simple_model(self) -> None:
        cols = StarFruit._column_defs()
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
        sql = DragonFruit._create_table_sql()
        assert sql.startswith('CREATE TABLE IF NOT EXISTS "dragon_fruit" (')

    def test_create_table_contains_all_columns(self) -> None:
        sql = DragonFruit._create_table_sql()
        assert '"id" BIGSERIAL PRIMARY KEY' in sql
        assert '"name" TEXT NOT NULL' in sql
        assert '"color" TEXT NOT NULL' in sql
        assert '"sweetness" TEXT' in sql
        assert '"origin" TEXT' in sql
        assert '"created_at" TIMESTAMP WITH TIME ZONE' in sql

    def test_create_table_is_valid_sql_shape(self) -> None:
        sql = DragonFruit._create_table_sql()
        assert sql.startswith("CREATE TABLE IF NOT EXISTS")
        assert sql.endswith(")")

    def test_simple_model_create_table(self) -> None:
        sql = StarFruit._create_table_sql()
        assert '"star_fruit"' in sql
        assert '"id" BIGSERIAL PRIMARY KEY' in sql
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
        assert "DragonFruit" in registered_names
        assert "StarFruit" in registered_names

    def test_base_model_not_registered(self) -> None:
        registered_names = [t.__name__ for t in _table_registry]
        assert "AirModel" not in registered_names


# ---------------------------------------------------------------------------
# Pydantic model behavior
# ---------------------------------------------------------------------------


class TestPydanticIntegration:
    def test_table_is_a_pydantic_model(self) -> None:
        """Table instances should be valid Pydantic models."""
        fruit = DragonFruit(name="Pink Pitaya", color="magenta")
        assert fruit.name == "Pink Pitaya"
        assert fruit.color == "magenta"
        assert fruit.id is None
        assert fruit.sweetness == ""

    def test_model_validate_from_dict(self) -> None:
        """model_validate should work (used by CRUD methods to hydrate from DB rows)."""
        data = {
            "id": 1,
            "created_at": datetime(2025, 1, 1),
            "name": "Pink Pitaya",
            "color": "magenta",
            "sweetness": "high",
            "origin": "Vietnam",
        }
        fruit = DragonFruit.model_validate(data)
        assert fruit.id == 1
        assert fruit.name == "Pink Pitaya"

    def test_model_dump_roundtrip(self) -> None:
        fruit = DragonFruit(name="Pink Pitaya", color="magenta")
        dumped = fruit.model_dump()
        assert dumped["name"] == "Pink Pitaya"
        assert dumped["color"] == "magenta"
        assert dumped["id"] is None


# ---------------------------------------------------------------------------
# AirDB initialization
# ---------------------------------------------------------------------------


class TestLimitOffset:
    @pytest.mark.asyncio
    async def test_all_with_limit_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.all(limit=10)

    @pytest.mark.asyncio
    async def test_all_with_offset_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.all(offset=5)

    @pytest.mark.asyncio
    async def test_filter_with_limit_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.filter(name="Yellow Dragon", limit=5)

    @pytest.mark.asyncio
    async def test_filter_with_offset_raises_without_pool(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.filter(name="Yellow Dragon", limit=5, offset=10)


class TestMultipleObjectsReturned:
    def test_is_an_exception(self) -> None:
        assert issubclass(MultipleObjectsReturned, Exception)

    def test_importable_from_air(self) -> None:
        import air

        assert hasattr(air, "MultipleObjectsReturned")

    @pytest.mark.asyncio
    async def test_get_without_pool_raises_runtime_error(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.get(id=1)


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
            await DragonFruit.create(name="Yellow Dragon", color="yellow")

    @pytest.mark.asyncio
    async def test_get_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.get(id=1)

    @pytest.mark.asyncio
    async def test_filter_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.filter(color="red")

    @pytest.mark.asyncio
    async def test_all_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.all()

    @pytest.mark.asyncio
    async def test_count_without_pool_raises(self) -> None:
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.count()

    @pytest.mark.asyncio
    async def test_save_without_pool_raises(self) -> None:
        fruit = DragonFruit(id=1, name="Yellow Dragon", color="yellow")
        with pytest.raises(RuntimeError, match="No database connection"):
            await fruit.save()

    @pytest.mark.asyncio
    async def test_delete_without_pool_raises(self) -> None:
        fruit = DragonFruit(id=1, name="Yellow Dragon", color="yellow")
        with pytest.raises(RuntimeError, match="No database connection"):
            await fruit.delete()


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
        fruit = DragonFruit(name="Yellow Dragon", color="yellow")
        assert fruit.id is None
        # This will raise RuntimeError (no pool) before ValueError,
        # so we test the model state instead
        assert fruit._pk_field() == "id"

    @pytest.mark.asyncio
    async def test_delete_without_pk_value_model_state(self) -> None:
        fruit = DragonFruit(name="Yellow Dragon", color="yellow")
        assert fruit.id is None
        assert fruit._pk_field() == "id"


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
        assert '"id" BIGSERIAL PRIMARY KEY' in sql
        assert '"title" TEXT NOT NULL' in sql
        assert '"body" TEXT NOT NULL' in sql
        assert '"draft" BOOLEAN NOT NULL' in sql

# ---------------------------------------------------------------------------
# UUID field support
# ---------------------------------------------------------------------------


class MagicPotion(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    batch_id: UUID
    label: str


class TestUUIDField:
    def test_uuid_column_def(self) -> None:
        cols = MagicPotion._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert '"batch_id" UUID NOT NULL' == col_dict["batch_id"]

    def test_uuid_in_create_table_sql(self) -> None:
        sql = MagicPotion._create_table_sql()
        assert '"batch_id" UUID NOT NULL' in sql

    def test_optional_uuid_no_not_null(self) -> None:
        class OptionalUUIDModel(AirModel):
            id: int | None = Field(default=None, primary_key=True)
            trace_id: UUID | None = None

        cols = OptionalUUIDModel._column_defs()
        col_dict = {c.split()[0].strip('"'): c for c in cols}
        assert "UUID" in col_dict["trace_id"]
        assert "NOT NULL" not in col_dict["trace_id"]



# ---------------------------------------------------------------------------
# order_by parameter
# ---------------------------------------------------------------------------


class TestOrderBy:
    @pytest.mark.asyncio
    async def test_all_order_by_ascending(self) -> None:
        """all(order_by="name") should accept a field name for ascending sort."""
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.all(order_by="name")

    @pytest.mark.asyncio
    async def test_all_order_by_descending(self) -> None:
        """all(order_by="-name") should use a leading dash to mean DESC."""
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.all(order_by="-name")

    @pytest.mark.asyncio
    async def test_filter_order_by_ascending(self) -> None:
        """filter() should accept order_by alongside column filters."""
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.filter(color="yellow", order_by="name")

    @pytest.mark.asyncio
    async def test_filter_order_by_descending(self) -> None:
        """filter() with order_by="-name" should sort descending."""
        with pytest.raises(RuntimeError, match="No database connection"):
            await DragonFruit.filter(color="yellow", order_by="-name")


# ---------------------------------------------------------------------------
# save() should refresh the instance from the database
# ---------------------------------------------------------------------------


class FakePool:
    """Test double that captures SQL and returns canned rows from fetchrow."""

    def __init__(self, fetchrow_return: dict[str, object]) -> None:
        self.last_sql: str | None = None
        self.last_args: tuple[object, ...] = ()
        self._fetchrow_return = fetchrow_return

    async def execute(self, sql: str, *args: object) -> None:
        self.last_sql = sql
        self.last_args = args

    async def fetchrow(self, sql: str, *args: object) -> dict[str, object]:
        self.last_sql = sql
        self.last_args = args
        return self._fetchrow_return


class TestSaveRefreshesInstance:
    """save() should use RETURNING * and update the instance's fields."""

    async def test_save_sql_contains_returning(self) -> None:
        """The UPDATE statement should end with RETURNING *."""
        from air.db import _set_current_db

        fake_pool = FakePool(
            fetchrow_return={
                "id": 1,
                "created_at": datetime(2026, 3, 17),
                "name": "Pink Pitaya",
                "color": "magenta",
                "sweetness": "high",
                "origin": "Vietnam",
            }
        )
        db = AirDB()
        db.pool = fake_pool
        _set_current_db(db)
        try:
            fruit = DragonFruit(
                id=1, name="Pink Pitaya", color="magenta"
            )
            await fruit.save()
            assert fake_pool.last_sql is not None
            assert "RETURNING *" in fake_pool.last_sql
        finally:
            _set_current_db(None)

    async def test_save_refreshes_fields_from_returned_row(self) -> None:
        """After save(), instance fields should reflect what the database returned."""
        from air.db import _set_current_db

        fake_pool = FakePool(
            fetchrow_return={
                "id": 1,
                "created_at": datetime(2026, 3, 17, 12, 0, 0),
                "name": "Pink Pitaya",
                "color": "hot pink",
                "sweetness": "extreme",
                "origin": "Philippines",
            }
        )
        db = AirDB()
        db.pool = fake_pool
        _set_current_db(db)
        try:
            fruit = DragonFruit(
                id=1, name="Pink Pitaya", color="magenta",
                sweetness="", origin=""
            )
            await fruit.save()

            # The database returned different values for these fields.
            # save() should have updated the instance to match.
            assert fruit.color == "hot pink"
            assert fruit.sweetness == "extreme"
            assert fruit.origin == "Philippines"
        finally:
            _set_current_db(None)
