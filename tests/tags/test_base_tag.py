from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

import pytest
from examples.samples.air_tag_samples import (
    AIR_TAG_SAMPLE,
    FRAGMENT_AIR_TAG_SAMPLE,
    SMALL_AIR_TAG_SAMPLE,
    TINY_AIR_TAG_SAMPLE,
)
from examples.samples.air_tag_source_samples import (
    AIR_TAG_SOURCE_SAMPLE,
    FRAGMENT_AIR_TAG_SOURCE_SAMPLE,
    SMALL_AIR_TAG_SOURCE_SAMPLE,
    TINY_AIR_TAG_SOURCE_SAMPLE,
)
from examples.samples.html_samples import FRAGMENT_HTML_SAMPLE, HTML_SAMPLE, SMALL_HTML_SAMPLE, TINY_HTML_SAMPLE
from full_match import match as full_match

import air
import air.tags.models.base as base_module
from air.tags.models.base import BaseTag
from air.tags.utils import SafeStr
from tests.utils import clean_doc

if TYPE_CHECKING:
    from collections.abc import Iterator

    from air.tags.models.types import Renderable, TagDictType

HTML_SAMPLES_DIR: Final = Path("examples/samples")
FRAGMENT_HTML_SAMPLE_FILE_NAME: Final = "fragment_html_sample.html"
FRAGMENT_HTML_SAMPLE_FILE_PATH: Final = HTML_SAMPLES_DIR / FRAGMENT_HTML_SAMPLE_FILE_NAME
TINY_HTML_SAMPLE_FILE_NAME: Final = "tiny_html_sample.html"
TINY_HTML_SAMPLE_FILE_PATH: Final = HTML_SAMPLES_DIR / TINY_HTML_SAMPLE_FILE_NAME
SMALL_HTML_SAMPLE_FILE_NAME: Final = "small_html_sample.html"
SMALL_HTML_SAMPLE_FILE_PATH: Final = HTML_SAMPLES_DIR / SMALL_HTML_SAMPLE_FILE_NAME
HTML_SAMPLE_FILE_NAME: Final = "html_sample.html"
HTML_SAMPLE_FILE_PATH: Final = HTML_SAMPLES_DIR / HTML_SAMPLE_FILE_NAME


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
    tag = WrapperTag("body", id_="main")
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
        },
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
        },
    ]


def test_compact_format_html_minifies() -> None:
    assert len(SMALL_AIR_TAG_SAMPLE.compact_render()) == 760
    assert len(AIR_TAG_SAMPLE.compact_render()) == 7536
    assert len(air.Html(*([AIR_TAG_SAMPLE.children] * 100)).compact_render()) == 884015


def test_compact_render_passes_html_to_compact_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []

    def fake_compact_formatter(html: str) -> str:
        captured.append(html)
        return "minified"

    monkeypatch.setattr(base_module, "compact_format_html", fake_compact_formatter)

    result = SampleTag("body").compact_render()

    assert result == "minified"
    assert captured == ["<sampletag>body</sampletag>"]


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


def test_compact_html_matches_compact_render() -> None:
    tag = SampleTag("body")

    assert tag.compact_html == tag.compact_render()


def test_save_writes_rendered_html(tmp_path: Path) -> None:
    target = tmp_path / "tag.html"
    SampleTag("saved").save(file_path=target)

    assert target.read_text() == "<sampletag>saved</sampletag>"


def test_pretty_save_writes_pretty_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "pretty.html"

    monkeypatch.setattr(base_module, "pretty_format_html", lambda html, **_: "pretty")

    SampleTag("pretty").pretty_save(file_path=target)

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


def test_last_child_returns_last_child() -> None:
    tag = WrapperTag("first", SampleTag("inner"), "last")

    assert tag.last_child == "last"


def test_first_child_returns_first_child() -> None:
    tag = WrapperTag("alpha", "beta")

    assert tag.first_child == "alpha"


def test_first_and_last_attribute_preserve_order() -> None:
    tag = SampleTag("child", first="1", second="2")

    assert tag.first_attribute == ("first", "1")
    assert tag.last_attribute == ("second", "2")


def test_counts_return_lengths() -> None:
    tag = WrapperTag("one", "two")
    tag_with_attrs = SampleTag(label="x", title="y")

    assert tag.num_of_direct_children == 2
    assert tag_with_attrs.num_of_attributes == 2


def test_tag_id_returns_attribute() -> None:
    tag = SampleTag(id_="identifier")

    assert tag.tag_id == "identifier"


def test_boolean_flags_for_children_and_attributes() -> None:
    empty = SampleTag()
    with_child = WrapperTag("kid")
    with_attr = SampleTag(data_id="42")

    assert not empty.has_children
    assert not empty.has_attributes
    assert empty.is_attribute_free_void_element
    assert with_child.has_children
    assert not with_child.is_attribute_free_void_element
    assert with_attr.has_attributes
    assert not with_attr.is_attribute_free_void_element


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
    child_dict: tuple[TagDictType | Renderable, ...] = (
        "plain",
        {
            "name": "SampleTag",
            "attributes": {},
            "children": (),
        },
    )

    restored = WrapperTag._from_child_dict(child_dict)

    assert restored[0] == "plain"
    assert isinstance(restored[1], SampleTag)


def test_init_subclass_registers_new_tag() -> None:
    class EphemeralTag(BaseTag):
        """Temporary tag for registry tests."""

    assert BaseTag.registry[EphemeralTag.__name__.lower()] is EphemeralTag


def test_from_dict_and_from_json_roundtrip() -> None:
    """This test encodes the intended behavior for from_dict/from_json."""
    original = AIR_TAG_SAMPLE
    original_type = type(original)
    original_dict = original.to_dict()
    original_json = original.to_json()

    rebuilt_from_dict = original_type.from_dict(original_dict)
    assert isinstance(rebuilt_from_dict, original_type)
    assert rebuilt_from_dict.to_dict() == original_dict
    assert rebuilt_from_dict.render() == original.render()

    rebuilt_from_json = original_type.from_json(original_json)
    assert isinstance(rebuilt_from_json, original_type)
    assert rebuilt_from_json.to_dict() == original_dict
    assert rebuilt_from_json.render() == original.render()


def test_pretty_from_dict_and_from_json_roundtrip() -> None:
    original = AIR_TAG_SAMPLE
    original_type = type(original)
    original_dict: dict = ast.literal_eval(
        original.to_pretty_dict(max_length=None, max_depth=None, max_string=None, expand_all=True)
    )
    original_json = original.to_pretty_json()

    rebuilt_from_dict = original_type.from_dict(original_dict)
    assert isinstance(rebuilt_from_dict, original_type)
    assert rebuilt_from_dict.to_dict() == original_dict
    assert rebuilt_from_dict.render() == original.render()

    rebuilt_from_json = original_type.from_json(original_json)
    assert isinstance(rebuilt_from_json, original_type)
    assert rebuilt_from_json.to_dict() == original_dict
    assert rebuilt_from_json.render() == original.render()


def test_print_source_outputs_python(monkeypatch: pytest.MonkeyPatch) -> None:
    html = "<div><p>hey</p></div>"
    captured: list[str] = []

    monkeypatch.setattr(base_module, "pretty_print_python", lambda source, **_: captured.append(source))

    air.Tag.print_source(html)

    assert captured == ["air.Div(\n    air.P('hey'),\n)"]


def test_save_source_writes_python(tmp_path: Path) -> None:
    html = "<div data-id='3'>ok</div>"
    target = tmp_path / "tag_source.py"

    air.Tag.save_source(file_path=target, html_source=html)

    saved = target.read_text()

    assert saved == "air.Div('ok', data_id=3)"


def test_hash_depends_on_rendered_html() -> None:
    first = SampleTag("x")
    second = SampleTag("x")
    third = SampleTag("y")

    assert hash(first) == hash(second)
    assert len({first, second, third}) == 2


def test_eq_rejects_non_tag() -> None:
    with pytest.raises(TypeError):
        _ = SampleTag() == "not-a-tag"


def test_from_html() -> None:
    actual_fragment_air_tag = air.Tag.from_html(FRAGMENT_HTML_SAMPLE)
    expected_fragment_air_tag = FRAGMENT_AIR_TAG_SAMPLE
    assert actual_fragment_air_tag == expected_fragment_air_tag
    actual_tiny_air_tag = air.Tag.from_html(TINY_HTML_SAMPLE)
    expected_tiny_air_tag = TINY_AIR_TAG_SAMPLE
    assert actual_tiny_air_tag.pretty_html == expected_tiny_air_tag.pretty_html
    actual_small_air_tag = air.Tag.from_html(SMALL_HTML_SAMPLE)
    expected_small_air_tag = SMALL_AIR_TAG_SAMPLE
    assert actual_small_air_tag.pretty_html == expected_small_air_tag.pretty_html
    actual_air_tag = air.Tag.from_html(HTML_SAMPLE)
    expected_air_tag = AIR_TAG_SAMPLE
    assert actual_air_tag.pretty_html == expected_air_tag.pretty_html


def test_to_source() -> None:
    actual_fragment_air_tag_source = FRAGMENT_AIR_TAG_SAMPLE.to_source()
    expected_fragment_air_tag_source = FRAGMENT_AIR_TAG_SOURCE_SAMPLE
    assert actual_fragment_air_tag_source == expected_fragment_air_tag_source
    actual_tiny_air_tag_source = TINY_AIR_TAG_SAMPLE.to_source()
    expected_tiny_air_tag_source = TINY_AIR_TAG_SOURCE_SAMPLE
    assert actual_tiny_air_tag_source == expected_tiny_air_tag_source
    actual_small_air_tag_source = SMALL_AIR_TAG_SAMPLE.to_source()
    expected_small_air_tag_source = SMALL_AIR_TAG_SOURCE_SAMPLE
    assert actual_small_air_tag_source == expected_small_air_tag_source
    actual_air_tag_source = AIR_TAG_SAMPLE.to_source()
    expected_air_tag_source = AIR_TAG_SOURCE_SAMPLE
    assert actual_air_tag_source == expected_air_tag_source


def test_from_html_to_source() -> None:
    actual_fragment_air_tag_source = air.Tag.from_html_to_source(FRAGMENT_HTML_SAMPLE)
    expected_fragment_air_tag_source = FRAGMENT_AIR_TAG_SOURCE_SAMPLE
    assert actual_fragment_air_tag_source == expected_fragment_air_tag_source
    actual_tiny_air_tag_source = air.Tag.from_html_to_source(TINY_HTML_SAMPLE)
    expected_tiny_air_tag_source = TINY_AIR_TAG_SOURCE_SAMPLE
    assert actual_tiny_air_tag_source == expected_tiny_air_tag_source
    actual_small_air_tag_source = air.Tag.from_html_to_source(SMALL_HTML_SAMPLE)
    expected_small_air_tag_source = SMALL_AIR_TAG_SOURCE_SAMPLE
    assert actual_small_air_tag_source == expected_small_air_tag_source
    actual_air_tag_source = air.Tag.from_html_to_source(HTML_SAMPLE)
    expected_air_tag_source = AIR_TAG_SOURCE_SAMPLE
    assert actual_air_tag_source == expected_air_tag_source


def test_from_html_file() -> None:
    actual_fragment_air_tag = air.Tag.from_html_file(file_path=FRAGMENT_HTML_SAMPLE_FILE_PATH)
    expected_fragment_air_tag = FRAGMENT_AIR_TAG_SAMPLE
    assert actual_fragment_air_tag == expected_fragment_air_tag
    actual_tiny_air_tag = air.Tag.from_html_file(file_path=TINY_HTML_SAMPLE_FILE_PATH)
    expected_tiny_air_tag = TINY_AIR_TAG_SAMPLE
    assert actual_tiny_air_tag.pretty_html == expected_tiny_air_tag.pretty_html
    actual_small_air_tag = air.Tag.from_html_file(file_path=SMALL_HTML_SAMPLE_FILE_PATH)
    expected_small_air_tag = SMALL_AIR_TAG_SAMPLE
    assert actual_small_air_tag.pretty_html == expected_small_air_tag.pretty_html
    actual_air_tag = air.Tag.from_html_file(file_path=HTML_SAMPLE_FILE_PATH)
    expected_air_tag = AIR_TAG_SAMPLE
    assert actual_air_tag.pretty_html == expected_air_tag.pretty_html


def test_from_html_file_to_source() -> None:
    actual_fragment_air_tag_source = air.Tag.from_html_file_to_source(file_path=FRAGMENT_HTML_SAMPLE_FILE_PATH)
    expected_fragment_air_tag_source = FRAGMENT_AIR_TAG_SOURCE_SAMPLE
    assert actual_fragment_air_tag_source == expected_fragment_air_tag_source
    actual_tiny_air_tag_source = air.Tag.from_html_file_to_source(file_path=TINY_HTML_SAMPLE_FILE_PATH)
    expected_tiny_air_tag_source = TINY_AIR_TAG_SOURCE_SAMPLE
    assert actual_tiny_air_tag_source == expected_tiny_air_tag_source
    actual_small_air_tag_source = air.Tag.from_html_file_to_source(file_path=SMALL_HTML_SAMPLE_FILE_PATH)
    expected_small_air_tag_source = SMALL_AIR_TAG_SOURCE_SAMPLE
    assert actual_small_air_tag_source == expected_small_air_tag_source
    actual_air_tag_source = air.Tag.from_html_file_to_source(file_path=HTML_SAMPLE_FILE_PATH)
    expected_air_tag_source = AIR_TAG_SOURCE_SAMPLE
    assert actual_air_tag_source == expected_air_tag_source


def test_from_html_with_leading_whitespace() -> None:
    html_source = clean_doc(
        """
           <main class="column p-5" style="overflow-y: auto;">

           <div class="columns">
         </div>

        </main>
        """
    )
    actual_air_tag = air.Tag.from_html(html_source)
    expected_air_tag = air.Main(
        air.Div(class_="columns"),
        class_="column p-5",
        style="overflow-y: auto;",
    )
    assert actual_air_tag == expected_air_tag


def test_from_html_with_comment() -> None:
    html_source = "<!-- My crazy comment -->"
    actual_air_tag = air.Tag.from_html(html_source)
    expected_air_tag = air.Comment("My crazy comment")
    assert actual_air_tag == expected_air_tag


def test_from_html_with_malformed_html_document_raises_value_error() -> None:
    html_source = clean_doc(
        """
        <!doctype html>
        <html lang="en">
          <head>
          </head>
          <body>
          </body<
        </html<
        """
    )
    with pytest.raises(
        ValueError,
        match=full_match("Tag.from_html(html_source) expects a valid HTML string."),
    ):
        air.Tag.from_html(html_source)


def test_from_html_with_head_start_tag_only_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match=full_match("Tag.from_html(html_source) expects a valid HTML string."),
    ):
        air.Tag.from_html("<head>")


def test_from_html_with_head_element_only_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match=full_match("Tag.from_html(html_source) is unable to parse the HTML content."),
    ):
        air.Tag.from_html("<head></head>")
