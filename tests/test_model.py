"""Tests for AirModel's backend-neutral model and query contract."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

import air
from air import AirField, AirModel
from air.model import (
    MultipleObjectsReturned,
    Predicate,
    Query,
    clear_model_backend,
    get_model_backend,
    registered_models,
    set_model_backend,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping, Sequence


class Note(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    title: str
    body: str = ""


class RecordingBackend:
    def __init__(self) -> None:
        self.calls: list[tuple[Any, ...]] = []
        self.rows: list[dict[str, Any]] = [{"id": 1, "title": "Selected", "body": ""}]

    async def create_tables(self, models: Iterable[type[AirModel]] | None = None) -> None:
        self.calls.append(("create_tables", tuple(models or ())))

    async def insert(self, model: type[AirModel], values: Mapping[str, Any]) -> Mapping[str, Any]:
        self.calls.append(("insert", model, dict(values)))
        return {"id": 1, **values}

    async def insert_many(
        self,
        model: type[AirModel],
        values: Sequence[Mapping[str, Any]],
    ) -> Sequence[Mapping[str, Any]]:
        rows = [{"id": index, **item} for index, item in enumerate(values, start=1)]
        self.calls.append(("insert_many", model, [dict(item) for item in values]))
        return rows

    async def select(self, query: Query) -> Sequence[Mapping[str, Any]]:
        self.calls.append(("select", query))
        return self.rows

    async def count(self, query: Query) -> int:
        self.calls.append(("count", query))
        return 3

    async def update(
        self,
        model: type[AirModel],
        primary_key: Any,
        values: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        self.calls.append(("update", model, primary_key, dict(values)))
        return {"id": primary_key, **values}

    async def update_many(self, query: Query, values: Mapping[str, Any]) -> int:
        self.calls.append(("update_many", query, dict(values)))
        return 2

    async def delete_many(self, query: Query) -> int:
        self.calls.append(("delete_many", query))
        return 4


@pytest.fixture
def backend() -> Iterator[RecordingBackend]:
    persistence = RecordingBackend()
    set_model_backend(persistence)
    yield persistence
    clear_model_backend(persistence)


class TestModelDefinition:
    def test_airmodel_is_exported_from_root(self) -> None:
        assert air.AirModel is AirModel

    def test_model_is_a_pydantic_model(self) -> None:
        note = Note(title="Hello")
        assert note.model_dump() == {"id": None, "title": "Hello", "body": ""}

    def test_database_table_is_stable_snake_case(self) -> None:
        class APIClientToken(AirModel):
            value: str

        assert APIClientToken.database_table() == "tests_api_client_token"
        assert APIClientToken._table_name() == APIClientToken.database_table()

    def test_explicit_table_name_is_honored(self) -> None:
        class LegacyNote(AirModel):
            table_name = "legacy_notes"

            id: int | None = AirField(default=None, primary_key=True)
            title: str

        assert LegacyNote.database_table() == "legacy_notes"

    def test_primary_key_helpers(self) -> None:
        assert Note.primary_key_field() == "id"
        assert Note._pk_field() == "id"
        assert Note.database_fields() == ["title", "body"]
        assert Note._non_pk_fields() == ["title", "body"]

    def test_model_without_primary_key(self) -> None:
        class Label(AirModel):
            name: str

        assert Label.primary_key_field() is None
        assert Label.database_fields() == ["name"]

    def test_subclasses_are_registered(self) -> None:
        assert Note in registered_models()
        assert AirModel not in registered_models()


class TestBackendConfiguration:
    def test_get_without_backend_has_actionable_error(self) -> None:
        clear_model_backend()
        with pytest.raises(RuntimeError, match="Configure a persistence package such as AirPostgres or AirD1"):
            get_model_backend()

    def test_set_and_clear_backend(self) -> None:
        persistence = RecordingBackend()
        set_model_backend(persistence)
        assert get_model_backend() is persistence
        clear_model_backend(persistence)
        with pytest.raises(RuntimeError, match="No AirModel backend"):
            get_model_backend()

    def test_old_backend_cannot_clear_replacement(self) -> None:
        old = RecordingBackend()
        replacement = RecordingBackend()
        set_model_backend(old)
        set_model_backend(replacement)
        clear_model_backend(old)
        assert get_model_backend() is replacement
        clear_model_backend()


class TestModelAndQuerySemantics:
    @pytest.mark.asyncio
    async def test_create_validates_then_inserts_plain_values(self, backend: RecordingBackend) -> None:
        note = await Note.create(title="Created", body="Text")
        assert note == Note(id=1, title="Created", body="Text")
        assert backend.calls == [("insert", Note, {"title": "Created", "body": "Text"})]

    @pytest.mark.asyncio
    async def test_get_owns_cardinality_semantics(self, backend: RecordingBackend) -> None:
        backend.rows = [{"id": 4, "title": "Found", "body": ""}]
        assert await Note.get(id=4) == Note(id=4, title="Found")
        assert backend.calls == [("select", Query(Note, (Predicate("id", "exact", 4),), limit=2))]

        backend.calls.clear()
        backend.rows = []
        assert await Note.get(id=404) is None

        backend.rows = [
            {"id": 1, "title": "One", "body": ""},
            {"id": 2, "title": "Two", "body": ""},
        ]
        with pytest.raises(MultipleObjectsReturned, match="Use filter"):
            await Note.get(title__contains="o")

    @pytest.mark.asyncio
    async def test_filter_builds_backend_neutral_query(self, backend: RecordingBackend) -> None:
        backend.rows = [{"id": 1, "title": "Filtered", "body": ""}]
        result = await Note.filter(title__contains="Air", order_by="-title", limit=5, offset=10)
        assert result == [Note(id=1, title="Filtered")]
        assert backend.calls == [
            (
                "select",
                Query(Note, (Predicate("title", "contains", "Air"),), "-title", 5, 10),
            )
        ]

    @pytest.mark.asyncio
    async def test_all_and_count_use_queries(self, backend: RecordingBackend) -> None:
        await Note.all(order_by="title", limit=2, offset=1)
        assert await Note.count(title="One") == 3
        assert backend.calls == [
            ("select", Query(Note, (), "title", 2, 1)),
            ("count", Query(Note, (Predicate("title", "exact", "One"),))),
        ]

    @pytest.mark.asyncio
    async def test_bulk_create_validates_items_before_inserting(self, backend: RecordingBackend) -> None:
        result = await Note.bulk_create([{"title": "One"}, {"title": "Two", "body": "Body"}])
        assert result == [Note(id=1, title="One"), Note(id=2, title="Two", body="Body")]
        assert backend.calls == [
            ("insert_many", Note, [{"title": "One", "body": ""}, {"title": "Two", "body": "Body"}])
        ]

    @pytest.mark.asyncio
    async def test_bulk_updates_and_deletes_require_filters(self, backend: RecordingBackend) -> None:
        with pytest.raises(ValueError, match="requires at least one filter"):
            await Note.bulk_update({"body": "Updated"})
        with pytest.raises(ValueError, match="requires at least one filter"):
            await Note.bulk_delete()

        assert await Note.bulk_update({"body": "Updated"}, title__contains="Air") == 2
        assert await Note.bulk_delete(title__contains="Old") == 4
        assert backend.calls == [
            (
                "update_many",
                Query(Note, (Predicate("title", "contains", "Air"),)),
                {"body": "Updated"},
            ),
            ("delete_many", Query(Note, (Predicate("title", "contains", "Old"),))),
        ]

    @pytest.mark.asyncio
    async def test_save_and_delete_keep_instance_semantics_in_core(self, backend: RecordingBackend) -> None:
        note = Note(id=1, title="Changed", body="Old")
        await note.save(update_fields=["title"])
        assert note == Note(id=1, title="Changed", body="Old")
        await note.delete()
        assert note.id is None
        assert backend.calls == [
            ("update", Note, 1, {"title": "Changed"}),
            ("delete_many", Query(Note, (Predicate("id", "exact", 1),))),
        ]

    @pytest.mark.asyncio
    async def test_core_rejects_invalid_fields_consistently(self, backend: RecordingBackend) -> None:
        with pytest.raises(ValueError, match="not a field"):
            await Note.filter(missing="value")
        with pytest.raises(ValueError, match="not a field"):
            await Note.all(order_by="missing")
        with pytest.raises(ValueError, match="Unknown or primary-key"):
            await Note.bulk_update({"id": 2}, title="One")
        with pytest.raises(ValueError, match="Unknown or primary-key"):
            await Note.bulk_update({"missing": "value"}, title="One")
