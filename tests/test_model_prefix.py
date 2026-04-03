"""Tests for automatic table prefix derivation.

AirModel derives a table prefix from the module where the model is defined:
- Package module (myapp.models) → prefix is the top-level package name (myapp)
- Standalone file with a meaningful name (bakeshop.py) → prefix is the filename (bakeshop)
- Standalone file with a generic name (main.py, app.py) → prefix is the
  normalized project name from pyproject.toml
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from air.model.main import (
    _normalize_project_name,  # noqa: PLC2701
    _read_project_name,  # noqa: PLC2701
    _table_prefix,  # noqa: PLC2701
)

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

# ---------------------------------------------------------------------------
# _normalize_project_name
# ---------------------------------------------------------------------------


class TestNormalizeProjectName:
    def test_strips_dot_com(self) -> None:
        assert _normalize_project_name("example-bakery.com") == "example_bakery"

    def test_strips_dot_org(self) -> None:
        assert _normalize_project_name("myproject.org") == "myproject"

    def test_strips_dot_io(self) -> None:
        assert _normalize_project_name("coolapp.io") == "coolapp"

    def test_replaces_hyphens(self) -> None:
        assert _normalize_project_name("my-cool-project") == "my_cool_project"

    def test_replaces_dots(self) -> None:
        assert _normalize_project_name("my.cool.project") == "my_cool_project"

    def test_lowercases(self) -> None:
        assert _normalize_project_name("MyProject") == "myproject"

    def test_combined_normalization(self) -> None:
        assert _normalize_project_name("My-Cool-App.io") == "my_cool_app"

    def test_plain_name_unchanged(self) -> None:
        assert _normalize_project_name("bakeshop") == "bakeshop"


# ---------------------------------------------------------------------------
# _table_prefix
# ---------------------------------------------------------------------------


class TestTablePrefix:
    def test_package_module_uses_top_level(self) -> None:
        assert _table_prefix("myapp.models") == "myapp"

    def test_deep_package_uses_top_level(self) -> None:
        assert _table_prefix("myapp.sub.models") == "myapp"

    def test_meaningful_standalone_file(self) -> None:
        assert _table_prefix("bakeshop") == "bakeshop"

    def test_generic_main_falls_back_to_project(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """main.py should fall back to pyproject.toml project name."""
        toml = tmp_path / "pyproject.toml"
        toml.write_text('[project]\nname = "example-bakery.com"\n')
        monkeypatch.chdir(tmp_path)
        # Clear the cache so it re-reads
        _read_project_name.cache_clear()
        assert _table_prefix("main") == "example_bakery"

    def test_generic_app_falls_back_to_project(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        toml = tmp_path / "pyproject.toml"
        toml.write_text('[project]\nname = "my-cool-project"\n')
        monkeypatch.chdir(tmp_path)
        _read_project_name.cache_clear()
        assert _table_prefix("app") == "my_cool_project"

    def test_generic_models_falls_back_to_project(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        toml = tmp_path / "pyproject.toml"
        toml.write_text('[project]\nname = "shopsite.io"\n')
        monkeypatch.chdir(tmp_path)
        _read_project_name.cache_clear()
        assert _table_prefix("models") == "shopsite"

    def test_generic_dunder_main_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        toml = tmp_path / "pyproject.toml"
        toml.write_text('[project]\nname = "example-bakery.com"\n')
        monkeypatch.chdir(tmp_path)
        _read_project_name.cache_clear()
        assert _table_prefix("__main__") == "example_bakery"

    def test_no_pyproject_uses_generic_name(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """If no pyproject.toml exists, fall back to the generic module name."""
        monkeypatch.chdir(tmp_path)
        _read_project_name.cache_clear()
        assert _table_prefix("main") == "main"


# ---------------------------------------------------------------------------
# Integration: _table_name includes the prefix
# ---------------------------------------------------------------------------


class TestTableNameWithPrefix:
    def test_model_table_name_is_prefixed(self) -> None:
        """Models defined in this test file get the module name as prefix."""
        from air.field import AirField  # noqa: PLC0415
        from air.model import AirModel  # noqa: PLC0415

        class SampleWidget(AirModel):
            id: int | None = AirField(default=None, primary_key=True)
            name: str

        # Module is "tests.test_model_prefix" (package module), so prefix is "tests"
        assert SampleWidget._table_name() == "tests_sample_widget"

    def test_create_table_sql_uses_prefixed_name(self) -> None:
        from air.field import AirField  # noqa: PLC0415
        from air.model import AirModel  # noqa: PLC0415

        class GadgetItem(AirModel):
            id: int | None = AirField(default=None, primary_key=True)
            label: str

        sql = GadgetItem._create_table_sql()
        assert '"tests_gadget_item"' in sql
