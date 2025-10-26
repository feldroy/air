from __future__ import annotations

import builtins
import json
import sys
import types
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast

import pytest

import air.tags.models.base as base_module
from air.tags.models.base import BaseTag, TagDictType
from air.tags.utils import SafeStr


class SampleTag(BaseTag):
    """Sample tag used in unit tests."""


class WrapperTag(BaseTag):
    """Container tag used to test nested structures."""


@pytest.fixture(autouse=True)
def restore_registry() -> Iterator[None]:
    original_registry = BaseTag._registry.copy()
    yield
    BaseTag._registry.clear()
    BaseTag._registry.update(original_registry)


def test_basetag_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        BaseTag()


def test_name_and_attrs_formatting() -> None:
    tag = SampleTag("content", class_="btn", data_id="42", disabled=True, hidden=False)

    assert tag.name == "sampletag"
    assert tag.attrs == ' class="btn" data-id="42" disabled'


def test_children_escape_plain_strings_and_preserve_safe_and_nested_tags() -> None:
    nested = SampleTag("inner")
    tag = WrapperTag("<script>", SafeStr("<em>safe</em>"), nested)

    assert tag.children == "&lt;script&gt;<em>safe</em><sampletag>inner</sampletag>"


def test_escape_text_escapes_html_entities() -> None:
    assert SampleTag()._escape_text("<b>bold</b>") == "&lt;b&gt;bold&lt;/b&gt;"


def test_render_and_str_return_paired_markup() -> None:
    tag = WrapperTag("body", id="main")
    expected = '<wrappertag id="main">body</wrappertag>'

    assert tag.render() == expected
    assert str(tag) == expected


def test_render_in_the_browser_uses_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []

    def fake_open(html: str) -> None:
        captured.append(html)

    monkeypatch.setattr(base_module, "open_html_in_the_browser", fake_open)

    SampleTag("browser").render_in_the_browser()

    assert captured == ["<sampletag>browser</sampletag>"]


def test_pretty_render_in_the_browser_uses_pretty_render(monkeypatch: pytest.MonkeyPatch) -> None:
    pretty_calls: list[dict[str, Any]] = []
    browser_calls: list[str] = []

    def fake_pretty_format(html: str, **kwargs: bool) -> str:
        pretty_calls.append({"html": html, "kwargs": kwargs})
        return "formatted"

    def fake_open(html: str) -> None:
        browser_calls.append(html)

    monkeypatch.setattr(base_module, "pretty_format_html", fake_pretty_format)
    monkeypatch.setattr(base_module, "open_html_in_the_browser", fake_open)

    SampleTag("content").pretty_render_in_the_browser()

    assert pretty_calls == [
        {
            "html": "<sampletag>content</sampletag>",
            "kwargs": {"with_body": True, "with_head": False, "with_doctype": True},
        }
    ]
    assert browser_calls == ["formatted"]


def test_pretty_render_passes_flags_to_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []

    def fake_formatter(html: str, **kwargs: bool) -> str:
        calls.append({"html": html, "kwargs": kwargs})
        return "pretty"

    monkeypatch.setattr(base_module, "pretty_format_html", fake_formatter)

    result = SampleTag("body").pretty_render(with_body=True, with_head=True, with_doctype=True)

    assert result == "pretty"
    assert calls == [
        {
            "html": "<sampletag>body</sampletag>",
            "kwargs": {"with_body": True, "with_head": True, "with_doctype": True},
        }
    ]


def test_pretty_print_delegates_to_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[str] = []

    def fake_pretty_print(html: str) -> None:
        printed.append(html)

    def fake_formatter(html: str, **kwargs: bool) -> str:
        return "formatted"

    monkeypatch.setattr(base_module, "pretty_print_html", fake_pretty_print)
    monkeypatch.setattr(base_module, "pretty_format_html", fake_formatter)

    SampleTag("text").pretty_print()

    assert printed == ["formatted"]


def test_save_writes_rendered_html(tmp_path: Path) -> None:
    target = tmp_path / "tag.html"
    SampleTag("saved").save(target)

    assert target.read_text() == "<sampletag>saved</sampletag>"


def test_pretty_save_writes_pretty_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "pretty.html"

    monkeypatch.setattr(base_module, "pretty_format_html", lambda html, **_: "pretty")

    SampleTag("pretty").pretty_save(target)

    assert target.read_text() == "pretty"


def test_pretty_display_in_the_browser_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_formatter(html: str, **kwargs: bool) -> str:
        return "pretty"

    def fake_display(html: str) -> None:
        calls.append(html)

    monkeypatch.setattr(base_module, "pretty_format_html", fake_formatter)
    monkeypatch.setattr(base_module, "display_pretty_html_in_the_browser", fake_display)

    SampleTag("x").pretty_display_in_the_browser()

    assert calls == ["pretty"]


def test_render_helpers_cover_void_and_paired_output() -> None:
    tag = SampleTag("void-test")

    assert tag._render_void() == "<sampletag>"
    assert tag._render_paired() == "<sampletag>void-test</sampletag>"


def test_doc_summary_and_repr_include_class_doc() -> None:
    summary = SampleTag()._doc_summary
    representation = repr(SampleTag())

    assert summary == "Sample tag used in unit tests."
    assert representation.startswith('<air.SampleTag("Sample tag used in unit tests.")>')


def test_full_repr_includes_attributes_and_children() -> None:
    nested = SampleTag("inner")
    tag = WrapperTag(nested, "plain", title="example")

    result = tag.full_repr()

    assert result.startswith("WrapperTag(")
    assert "children=SampleTag" in result
    assert "plain" in result


def test_to_dict_and_to_child_dict_structure() -> None:
    nested = SampleTag("inner")
    tag = WrapperTag(nested, "plain", title="example")

    tag_dict = tag.to_dict()
    child_list = tag._to_child_dict()

    assert tag_dict["name"] == "WrapperTag"
    assert tag_dict["attributes"] == {"title": "example"}
    assert isinstance(child_list[0], dict)
    assert child_list[1] == "plain"


def test_to_json_and_to_pretty_json_round_trip() -> None:
    tag = SampleTag("json", data_id="7")

    loaded = json.loads(tag.to_json())
    pretty_loaded = json.loads(tag.to_pretty_json())

    assert loaded["name"] == "SampleTag"
    assert pretty_loaded == loaded


def test_to_pretty_dict_uses_rich_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    rich_module = types.ModuleType("rich")
    rich_pretty_module = types.ModuleType("rich.pretty")

    def fake_pretty_repr(data: TagDictType, **kwargs: Any) -> str:
        captured["data"] = data
        captured["kwargs"] = kwargs
        return "pretty"

    rich_pretty_module.pretty_repr = fake_pretty_repr
    rich_module.pretty = rich_pretty_module

    monkeypatch.setitem(sys.modules, "rich", rich_module)
    monkeypatch.setitem(sys.modules, "rich.pretty", rich_pretty_module)

    result = SampleTag("rich").to_pretty_dict()

    assert result == "pretty"
    assert captured["data"]["name"] == "SampleTag"


def test_to_pretty_dict_falls_back_when_rich_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def fake_import(
        name: str,
        globals_: dict[str, Any] | None = None,
        locals_: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name == "rich.pretty":
            raise ModuleNotFoundError
        return original_import(name, globals_, locals_, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    tag = SampleTag("fallback")
    result = tag.to_pretty_dict()

    assert result == str(tag.to_dict())


def test_from_dict_and_from_json_restore_instances() -> None:
    original = WrapperTag(SampleTag("child"), "plain", title="demo")
    as_dict = original.to_dict()
    as_json = original.to_json()

    from_dict = WrapperTag.from_dict(as_dict)
    from_json = WrapperTag.from_json(as_json)

    assert isinstance(from_dict, WrapperTag)
    assert isinstance(from_json, WrapperTag)
    assert from_dict.render() == original.render()
    assert from_json.render() == original.render()


def test_from_child_dict_handles_nested_and_plain_values() -> None:
    child_dict: tuple[Any, ...] = (
        "plain",
        {
            "name": "SampleTag",
            "attributes": {},
            "children": (),
        },
    )

    restored = WrapperTag._from_child_dict(cast(Any, child_dict))

    assert restored[0] == "plain"
    assert isinstance(restored[1], SampleTag)


def test_init_subclass_registers_new_tag() -> None:
    class EphemeralTag(BaseTag):
        """Temporary tag for registry tests."""

    assert BaseTag.registry["EphemeralTag"] is EphemeralTag
