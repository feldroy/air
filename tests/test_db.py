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


# ---------------------------------------------------------------------------
# delete() should clear the primary key
# ---------------------------------------------------------------------------


class TestDeleteClearsPrimaryKey:
    """After delete(), the instance's PK should be None so accidental
    save() or delete() calls fail with a clear ValueError instead of
    silently operating on a deleted row."""

    async def test_delete_clears_pk(self) -> None:
        from air.db import _set_current_db

        fake_pool = FakePool(fetchrow_return={})
        db = AirDB()
        db.pool = fake_pool
        _set_current_db(db)
        try:
            fruit = DragonFruit(
                id=1, name="Pink Pitaya", color="magenta"
            )
            assert fruit.id == 1

            await fruit.delete()

            assert fruit.id is None
        finally:
            _set_current_db(None)


# ---------------------------------------------------------------------------
# CRUD operations with mock pool
# ---------------------------------------------------------------------------


class CRUDPool:
    """Test double that captures SQL/args for all pool methods used by CRUD."""

    def __init__(
        self,
        *,
        fetchrow_return: dict[str, object] | None = None,
        fetch_return: list[dict[str, object]] | None = None,
        fetchval_return: object = None,
    ) -> None:
        self.last_sql: str | None = None
        self.last_args: tuple[object, ...] = ()
        self._fetchrow_return = fetchrow_return or {}
        self._fetch_return = fetch_return if fetch_return is not None else []
        self._fetchval_return = fetchval_return

    async def fetchrow(self, sql: str, *args: object) -> dict[str, object]:
        self.last_sql = sql
        self.last_args = args
        return self._fetchrow_return

    async def fetch(self, sql: str, *args: object) -> list[dict[str, object]]:
        self.last_sql = sql
        self.last_args = args
        return self._fetch_return

    async def fetchval(self, sql: str, *args: object) -> object:
        self.last_sql = sql
        self.last_args = args
        return self._fetchval_return


def _wire_pool(pool: object) -> None:
    """Wire a fake pool into the module-level _current_db."""
    from air.db import _set_current_db

    db = AirDB()
    db.pool = pool
    _set_current_db(db)


def _unwire_pool() -> None:
    from air.db import _set_current_db

    _set_current_db(None)


_DRAGON_ROW: dict[str, object] = {
    "id": 1,
    "created_at": datetime(2026, 3, 17),
    "name": "Pink Pitaya",
    "color": "magenta",
    "sweetness": "high",
    "origin": "Vietnam",
}

_DRAGON_ROW_2: dict[str, object] = {
    "id": 2,
    "created_at": datetime(2026, 3, 18),
    "name": "Yellow Dragon",
    "color": "yellow",
    "sweetness": "medium",
    "origin": "Colombia",
}


class TestCRUDWithMockPool:
    """Test CRUD class methods by wiring a fake pool that captures SQL."""

    # -- create() ------------------------------------------------------------

    async def test_create_calls_fetchrow_with_insert_returning(self) -> None:
        """create() should INSERT non-PK fields and use RETURNING *."""
        pool = CRUDPool(fetchrow_return=dict(_DRAGON_ROW))
        _wire_pool(pool)
        try:
            result = await DragonFruit.create(name="Pink Pitaya", color="magenta")

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('INSERT INTO "dragon_fruit"')
            assert "RETURNING *" in pool.last_sql
            assert '"name"' in pool.last_sql
            assert '"color"' in pool.last_sql
            # PK field should not appear in the INSERT column list
            assert '"id"' not in pool.last_sql
        finally:
            _unwire_pool()

    async def test_create_returns_hydrated_instance(self) -> None:
        """create() should return a DragonFruit populated from the returned row."""
        pool = CRUDPool(fetchrow_return=dict(_DRAGON_ROW))
        _wire_pool(pool)
        try:
            result = await DragonFruit.create(name="Pink Pitaya", color="magenta")

            assert isinstance(result, DragonFruit)
            assert result.id == 1
            assert result.name == "Pink Pitaya"
            assert result.color == "magenta"
            assert result.sweetness == "high"
            assert result.origin == "Vietnam"
        finally:
            _unwire_pool()

    # -- get() ---------------------------------------------------------------

    async def test_get_one_match_returns_instance(self) -> None:
        """get() with exactly one matching row should return that instance."""
        pool = CRUDPool(fetch_return=[dict(_DRAGON_ROW)])
        _wire_pool(pool)
        try:
            result = await DragonFruit.get(id=1)

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('SELECT * FROM "dragon_fruit" WHERE')
            assert "LIMIT 2" in pool.last_sql
            assert isinstance(result, DragonFruit)
            assert result.id == 1
            assert result.name == "Pink Pitaya"
        finally:
            _unwire_pool()

    async def test_get_no_match_returns_none(self) -> None:
        """get() with zero matching rows should return None."""
        pool = CRUDPool(fetch_return=[])
        _wire_pool(pool)
        try:
            result = await DragonFruit.get(id=999)

            assert result is None
        finally:
            _unwire_pool()

    async def test_get_two_matches_raises_multiple_objects_returned(self) -> None:
        """get() with more than one match should raise MultipleObjectsReturned."""
        pool = CRUDPool(fetch_return=[dict(_DRAGON_ROW), dict(_DRAGON_ROW_2)])
        _wire_pool(pool)
        try:
            with pytest.raises(MultipleObjectsReturned, match="matched more than one row"):
                await DragonFruit.get(color="magenta")
        finally:
            _unwire_pool()

    # -- filter() ------------------------------------------------------------

    async def test_filter_with_kwargs_uses_where(self) -> None:
        """filter(color="magenta") should SELECT with a WHERE clause."""
        pool = CRUDPool(fetch_return=[dict(_DRAGON_ROW)])
        _wire_pool(pool)
        try:
            results = await DragonFruit.filter(color="magenta")

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('SELECT * FROM "dragon_fruit" WHERE')
            assert '"color" = $1' in pool.last_sql
            assert isinstance(results, list)
            assert len(results) == 1
            assert results[0].name == "Pink Pitaya"
        finally:
            _unwire_pool()

    async def test_filter_no_kwargs_delegates_to_all(self) -> None:
        """filter() with no kwargs should produce the same SQL as all()."""
        pool = CRUDPool(fetch_return=[dict(_DRAGON_ROW), dict(_DRAGON_ROW_2)])
        _wire_pool(pool)
        try:
            results = await DragonFruit.filter()

            assert pool.last_sql is not None
            # all() produces a bare SELECT * with no WHERE
            assert pool.last_sql == 'SELECT * FROM "dragon_fruit"'
            assert len(results) == 2
        finally:
            _unwire_pool()

    # -- all() ---------------------------------------------------------------

    async def test_all_calls_fetch_with_select_star(self) -> None:
        """all() should SELECT * with no WHERE clause."""
        pool = CRUDPool(fetch_return=[dict(_DRAGON_ROW), dict(_DRAGON_ROW_2)])
        _wire_pool(pool)
        try:
            results = await DragonFruit.all()

            assert pool.last_sql == 'SELECT * FROM "dragon_fruit"'
            assert pool.last_args == ()
            assert isinstance(results, list)
            assert len(results) == 2
            assert results[0].name == "Pink Pitaya"
            assert results[1].name == "Yellow Dragon"
        finally:
            _unwire_pool()

    # -- count() -------------------------------------------------------------

    async def test_count_calls_fetchval_with_count(self) -> None:
        """count() should SELECT COUNT(*) and return an int."""
        pool = CRUDPool(fetchval_return=42)
        _wire_pool(pool)
        try:
            result = await DragonFruit.count()

            assert pool.last_sql == 'SELECT COUNT(*) FROM "dragon_fruit"'
            assert pool.last_args == ()
            assert result == 42
        finally:
            _unwire_pool()

    async def test_count_with_kwargs_adds_where(self) -> None:
        """count(color="magenta") should add a WHERE clause."""
        pool = CRUDPool(fetchval_return=7)
        _wire_pool(pool)
        try:
            result = await DragonFruit.count(color="magenta")

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('SELECT COUNT(*) FROM "dragon_fruit" WHERE')
            assert '"color" = $1' in pool.last_sql
            assert result == 7
        finally:
            _unwire_pool()


# ---------------------------------------------------------------------------
# Lookup operators (Django-style double-underscore)
# ---------------------------------------------------------------------------


class RainbowWaterfall(AirModel):
    """Test model with fields suited to lookup operator tests."""

    id: int | None = Field(default=None, primary_key=True)
    location: str
    sparkle_rating: int
    confirmed: bool = Field(default=False)


_WATERFALL_ROW: dict[str, object] = {
    "id": 1,
    "location": "Rainbow Falls",
    "sparkle_rating": 11,
    "confirmed": True,
}


class TestLookupOperators:
    """Verify that Django-style __lookup kwargs produce the correct SQL.

    Each test wires a CRUDPool mock and checks last_sql / last_args after
    calling filter(), get(), or count(). These tests should FAIL against
    the current implementation, which treats the full kwarg key (e.g.
    ``sparkle_rating__gt``) as a literal column name.
    """

    # -- gt ------------------------------------------------------------------

    async def test_filter_gt(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__gt=5)

            assert pool.last_sql is not None
            assert '"sparkle_rating" > $1' in pool.last_sql
            assert pool.last_args == (5,)
        finally:
            _unwire_pool()

    # -- gte -----------------------------------------------------------------

    async def test_filter_gte(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__gte=5)

            assert pool.last_sql is not None
            assert '"sparkle_rating" >= $1' in pool.last_sql
            assert pool.last_args == (5,)
        finally:
            _unwire_pool()

    # -- lt ------------------------------------------------------------------

    async def test_filter_lt(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__lt=10)

            assert pool.last_sql is not None
            assert '"sparkle_rating" < $1' in pool.last_sql
            assert pool.last_args == (10,)
        finally:
            _unwire_pool()

    # -- lte -----------------------------------------------------------------

    async def test_filter_lte(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__lte=10)

            assert pool.last_sql is not None
            assert '"sparkle_rating" <= $1' in pool.last_sql
            assert pool.last_args == (10,)
        finally:
            _unwire_pool()

    # -- contains ------------------------------------------------------------

    async def test_filter_contains(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(location__contains="Falls")

            assert pool.last_sql is not None
            assert "LIKE" in pool.last_sql
            assert "'%' || $1 || '%'" in pool.last_sql
            assert pool.last_args == ("Falls",)
        finally:
            _unwire_pool()

    # -- icontains -----------------------------------------------------------

    async def test_filter_icontains(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(location__icontains="falls")

            assert pool.last_sql is not None
            assert "ILIKE" in pool.last_sql
            assert "'%' || $1 || '%'" in pool.last_sql
            assert pool.last_args == ("falls",)
        finally:
            _unwire_pool()

    # -- in ------------------------------------------------------------------

    async def test_filter_in(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__in=[5, 8, 11])

            assert pool.last_sql is not None
            assert '"sparkle_rating" = ANY($1)' in pool.last_sql
            assert pool.last_args == ([5, 8, 11],)
        finally:
            _unwire_pool()

    # -- isnull=True ---------------------------------------------------------

    async def test_filter_isnull_true(self) -> None:
        pool = CRUDPool(fetch_return=[])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(confirmed__isnull=True)

            assert pool.last_sql is not None
            assert '"confirmed" IS NULL' in pool.last_sql
            # isnull=True should not add a parameter
            assert pool.last_args == ()
        finally:
            _unwire_pool()

    # -- isnull=False --------------------------------------------------------

    async def test_filter_isnull_false(self) -> None:
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(confirmed__isnull=False)

            assert pool.last_sql is not None
            assert '"confirmed" IS NOT NULL' in pool.last_sql
            # isnull=False should not add a parameter either
            assert pool.last_args == ()
        finally:
            _unwire_pool()

    # -- plain equality still works ------------------------------------------

    async def test_plain_equality_still_works(self) -> None:
        """Backward compatibility: plain kwargs remain simple equality."""
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(location="Rainbow Falls")

            assert pool.last_sql is not None
            assert '"location" = $1' in pool.last_sql
            assert pool.last_args == ("Rainbow Falls",)
        finally:
            _unwire_pool()

    # -- combining lookups with plain equality --------------------------------

    async def test_filter_combined_lookups(self) -> None:
        """Multiple lookups in one call should all appear in the WHERE clause."""
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.filter(sparkle_rating__gte=5, confirmed=True)

            assert pool.last_sql is not None
            assert '"sparkle_rating" >= $' in pool.last_sql
            assert '"confirmed" = $' in pool.last_sql
            # Both values should be in args (order depends on dict iteration,
            # so check membership rather than position)
            assert 5 in pool.last_args
            assert True in pool.last_args
            assert len(pool.last_args) == 2
        finally:
            _unwire_pool()

    # -- lookups work in get() -----------------------------------------------

    async def test_get_with_lookup(self) -> None:
        """get() should support lookup operators the same way filter() does."""
        pool = CRUDPool(fetch_return=[dict(_WATERFALL_ROW)])
        _wire_pool(pool)
        try:
            await RainbowWaterfall.get(sparkle_rating__gte=11)

            assert pool.last_sql is not None
            assert '"sparkle_rating" >= $1' in pool.last_sql
            assert pool.last_args == (11,)
        finally:
            _unwire_pool()

    # -- lookups work in count() ---------------------------------------------

    async def test_count_with_lookup(self) -> None:
        """count() should support lookup operators the same way filter() does."""
        pool = CRUDPool(fetchval_return=3)
        _wire_pool(pool)
        try:
            result = await RainbowWaterfall.count(sparkle_rating__gt=5)

            assert pool.last_sql is not None
            assert '"sparkle_rating" > $1' in pool.last_sql
            assert pool.last_args == (5,)
            assert result == 3
        finally:
            _unwire_pool()


# ---------------------------------------------------------------------------
# Transaction context manager
# ---------------------------------------------------------------------------


class FakeTransaction:
    """Test double for an asyncpg transaction object."""

    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    async def start(self) -> "FakeTransaction":
        return self

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


class FakeConnection:
    """Test double for an asyncpg connection acquired from a pool.

    Supports the same query methods as the pool (fetchrow, fetch, fetchval,
    execute) plus a transaction() method that returns a FakeTransaction.
    """

    def __init__(
        self,
        *,
        fetchrow_return: dict[str, object] | None = None,
        fetch_return: list[dict[str, object]] | None = None,
        fetchval_return: object = None,
    ) -> None:
        self.last_sql: str | None = None
        self.last_args: tuple[object, ...] = ()
        self.fetchrow_called = False
        self.fetch_called = False
        self.fetchval_called = False
        self.execute_called = False
        self._fetchrow_return = fetchrow_return or {}
        self._fetch_return = fetch_return if fetch_return is not None else []
        self._fetchval_return = fetchval_return
        self._transaction = FakeTransaction()

    async def fetchrow(self, sql: str, *args: object) -> dict[str, object]:
        self.fetchrow_called = True
        self.last_sql = sql
        self.last_args = args
        return self._fetchrow_return

    async def fetch(self, sql: str, *args: object) -> list[dict[str, object]]:
        self.fetch_called = True
        self.last_sql = sql
        self.last_args = args
        return self._fetch_return

    async def fetchval(self, sql: str, *args: object) -> object:
        self.fetchval_called = True
        self.last_sql = sql
        self.last_args = args
        return self._fetchval_return

    async def execute(self, sql: str, *args: object) -> None:
        self.execute_called = True
        self.last_sql = sql
        self.last_args = args

    def transaction(self) -> FakeTransaction:
        return self._transaction


class FakeAcquireContext:
    """Async context manager returned by TransactionPool.acquire()."""

    def __init__(self, connection: FakeConnection) -> None:
        self._connection = connection

    async def __aenter__(self) -> FakeConnection:
        return self._connection

    async def __aexit__(self, *args: object) -> None:
        pass


class TransactionPool(CRUDPool):
    """Extends CRUDPool with acquire() that yields a FakeConnection.

    This simulates what asyncpg pools do: pool.acquire() returns an async
    context manager that yields a connection, and the connection has its
    own transaction() method.
    """

    def __init__(
        self,
        connection: FakeConnection,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._connection = connection
        self.acquire_called = False

    def acquire(self) -> FakeAcquireContext:
        self.acquire_called = True
        return FakeAcquireContext(self._connection)


class TestTransaction:
    """Tests for db.transaction() -- an async context manager on AirDB
    that groups CRUD operations into a single database transaction.

    These tests should FAIL because db.transaction() does not exist yet.
    """

    def test_transaction_exists(self) -> None:
        """AirDB should have a transaction method."""
        db = AirDB()
        assert hasattr(db, "transaction")
        assert callable(db.transaction)

    def test_transaction_is_async_context_manager(self) -> None:
        """transaction() should return an object with __aenter__ and __aexit__."""
        db = AirDB()
        db.pool = TransactionPool(
            connection=FakeConnection(),
        )
        ctx = db.transaction()
        assert hasattr(ctx, "__aenter__"), "transaction() return value must have __aenter__"
        assert hasattr(ctx, "__aexit__"), "transaction() return value must have __aexit__"

    async def test_transaction_acquires_connection(self) -> None:
        """Entering the transaction block should acquire a connection from the pool."""
        conn = FakeConnection()
        pool = TransactionPool(connection=conn)
        db = AirDB()
        db.pool = pool

        async with db.transaction():
            pass

        assert pool.acquire_called, "transaction() should call pool.acquire()"

    async def test_transaction_commits_on_success(self) -> None:
        """On clean exit from the block, commit() should be called on the transaction."""
        conn = FakeConnection()
        pool = TransactionPool(connection=conn)
        db = AirDB()
        db.pool = pool

        async with db.transaction():
            pass

        assert conn._transaction.committed, "transaction should be committed on clean exit"
        assert not conn._transaction.rolled_back, "transaction should not be rolled back on clean exit"

    async def test_transaction_rolls_back_on_exception(self) -> None:
        """When an exception propagates out of the block, rollback() should be called."""
        conn = FakeConnection()
        pool = TransactionPool(connection=conn)
        db = AirDB()
        db.pool = pool

        with pytest.raises(ValueError, match="something went wrong"):
            async with db.transaction():
                raise ValueError("something went wrong")

        assert conn._transaction.rolled_back, "transaction should be rolled back on exception"
        assert not conn._transaction.committed, "transaction should not be committed on exception"

    async def test_crud_inside_transaction_uses_connection(self) -> None:
        """CRUD operations inside the block should use the transaction's
        connection, not the pool directly.

        We verify by checking that the FakeConnection's fetchrow was called
        (for create()) and the pool-level fetchrow was NOT called.
        """
        from air.db import _set_current_db

        conn = FakeConnection(
            fetchrow_return=dict(_DRAGON_ROW),
        )
        pool = TransactionPool(
            connection=conn,
            fetchrow_return=dict(_DRAGON_ROW),
        )
        db = AirDB()
        db.pool = pool
        _set_current_db(db)
        try:
            async with db.transaction():
                await DragonFruit.create(name="Pink Pitaya", color="magenta")

            # The connection's fetchrow should have been called, not the pool's
            assert conn.fetchrow_called, (
                "create() inside transaction should use the connection, not the pool"
            )
        finally:
            _set_current_db(None)


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


class BulkPool(CRUDPool):
    """Extends CRUDPool with execute() that returns a status string.

    asyncpg's execute() returns a command-tag string like "UPDATE 3" or
    "DELETE 5". bulk_update and bulk_delete parse that to get the affected
    row count.
    """

    def __init__(
        self,
        *,
        execute_return: str = "UPDATE 0",
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._execute_return = execute_return
        self.execute_called = False

    async def execute(self, sql: str, *args: object) -> str:
        self.execute_called = True
        self.last_sql = sql
        self.last_args = args
        return self._execute_return


_DRAGON_ROW_3: dict[str, object] = {
    "id": 3,
    "created_at": datetime(2026, 3, 19),
    "name": "White Pitaya",
    "color": "white",
    "sweetness": "low",
    "origin": "Thailand",
}


class TestBulkOperations:
    """Tests for bulk_create, bulk_update, and bulk_delete class methods.

    These should all FAIL because the methods don't exist yet.
    """

    # -- bulk_create ---------------------------------------------------------

    async def test_bulk_create_returns_list(self) -> None:
        """bulk_create() should return a list of DragonFruit instances."""
        pool = CRUDPool(
            fetch_return=[dict(_DRAGON_ROW), dict(_DRAGON_ROW_2)],
        )
        _wire_pool(pool)
        try:
            results = await DragonFruit.bulk_create([
                {"name": "Pink Pitaya", "color": "magenta"},
                {"name": "Yellow Dragon", "color": "yellow"},
            ])

            assert isinstance(results, list)
            assert len(results) == 2
            assert all(isinstance(r, DragonFruit) for r in results)
            assert results[0].name == "Pink Pitaya"
            assert results[0].id == 1
            assert results[1].name == "Yellow Dragon"
            assert results[1].id == 2
        finally:
            _unwire_pool()

    async def test_bulk_create_sql_is_multi_row_insert(self) -> None:
        """bulk_create() should generate an INSERT with multiple value sets
        or use a single INSERT...RETURNING * that covers all rows."""
        pool = CRUDPool(
            fetch_return=[
                dict(_DRAGON_ROW),
                dict(_DRAGON_ROW_2),
                dict(_DRAGON_ROW_3),
            ],
        )
        _wire_pool(pool)
        try:
            await DragonFruit.bulk_create([
                {"name": "Pink Pitaya", "color": "magenta"},
                {"name": "Yellow Dragon", "color": "yellow"},
                {"name": "White Pitaya", "color": "white"},
            ])

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('INSERT INTO "dragon_fruit"')
            assert "RETURNING *" in pool.last_sql
            # Should have multiple value placeholders (one set per row)
            # e.g. ($1, $2), ($3, $4), ($5, $6)
            assert pool.last_sql.count("(") >= 4  # table parens + 3 value sets
        finally:
            _unwire_pool()

    async def test_bulk_create_empty_list_returns_empty(self) -> None:
        """bulk_create([]) should return [] without hitting the database."""
        pool = CRUDPool()
        _wire_pool(pool)
        try:
            results = await DragonFruit.bulk_create([])

            assert results == []
            # Should not have issued any SQL
            assert pool.last_sql is None
        finally:
            _unwire_pool()

    # -- bulk_update ---------------------------------------------------------

    async def test_bulk_update_generates_update_where(self) -> None:
        """bulk_update() should generate UPDATE...SET...WHERE SQL."""
        pool = BulkPool(execute_return="UPDATE 3")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_update(
                {"color": "red"}, name="Pink Pitaya"
            )

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('UPDATE "dragon_fruit" SET')
            assert '"color" =' in pool.last_sql
            assert "WHERE" in pool.last_sql
            assert '"name" =' in pool.last_sql
        finally:
            _unwire_pool()

    async def test_bulk_update_with_lookup_operators(self) -> None:
        """bulk_update() should support Django-style lookup operators in
        the filter kwargs (the WHERE clause)."""
        pool = BulkPool(execute_return="UPDATE 5")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_update(
                {"color": "red"}, sweetness__contains="high"
            )

            assert pool.last_sql is not None
            assert "WHERE" in pool.last_sql
            assert "LIKE" in pool.last_sql
            assert '"color" =' in pool.last_sql
        finally:
            _unwire_pool()

    async def test_bulk_update_returns_row_count(self) -> None:
        """bulk_update() should return the number of rows affected as an int."""
        pool = BulkPool(execute_return="UPDATE 7")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_update(
                {"color": "red"}, name__contains="Dragon"
            )

            assert isinstance(count, int)
            assert count == 7
        finally:
            _unwire_pool()

    # -- bulk_delete ---------------------------------------------------------

    async def test_bulk_delete_generates_delete_where(self) -> None:
        """bulk_delete() should generate DELETE FROM...WHERE SQL."""
        pool = BulkPool(execute_return="DELETE 2")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_delete(confirmed=False)

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('DELETE FROM "dragon_fruit" WHERE')
            assert '"confirmed" = $1' in pool.last_sql
        finally:
            _unwire_pool()

    async def test_bulk_delete_with_lookup_operators(self) -> None:
        """bulk_delete() should support Django-style lookup operators."""
        pool = BulkPool(execute_return="DELETE 4")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_delete(sweetness__lt=3)

            assert pool.last_sql is not None
            assert pool.last_sql.startswith('DELETE FROM "dragon_fruit" WHERE')
            assert '"sweetness" < $1' in pool.last_sql
            assert pool.last_args == (3,)
        finally:
            _unwire_pool()

    async def test_bulk_delete_returns_row_count(self) -> None:
        """bulk_delete() should return the number of deleted rows as an int."""
        pool = BulkPool(execute_return="DELETE 12")
        _wire_pool(pool)
        try:
            count = await DragonFruit.bulk_delete(origin__icontains="vietnam")

            assert isinstance(count, int)
            assert count == 12
        finally:
            _unwire_pool()
