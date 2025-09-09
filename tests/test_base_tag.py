# tests/test_tag.py
from __future__ import annotations

import json
from typing import Any

from examples.html_sample import HTML_SAMPLE

from air import SafeStr, Tag


class MyTag(Tag):
    """Simple concrete Tag subclass used in tests."""


def _strip_ws(s: str) -> str:
    """Helper to normalize insignificant whitespace (meaning: space that doesn't change HTML)."""
    return " ".join(s.split())


def test_render_basic_text() -> None:
    tag = MyTag("Hello")
    rendered = tag.render()
    assert rendered == "<mytag>Hello</mytag>"


def test_render_with_attributes_cleaning_and_boolean() -> None:
    tag = MyTag(class_="btn", data_test_id=3, disabled=True, hidden=False)
    rendered = tag.render()

    # Attributes appear on the opening tag
    assert rendered.startswith("<mytag")
    assert rendered.endswith("</mytag>")

    # Key cleaning
    assert ' class="btn"' in rendered
    assert ' data-test-id="3"' in rendered

    # Boolean handling
    assert " disabled" in rendered  # True -> present without value
    assert " hidden" not in rendered  # False -> omitted


def test_render_escapes_plain_text_and_preserves_safestr_and_child_tag() -> None:
    child_plain = "<script>alert(1)</script>"
    child_safe = SafeStr("<b>bold</b>")
    child_tag = MyTag("X")

    tag = MyTag(child_plain, child_safe, child_tag)
    out = tag.render()

    # Plain string is escaped
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in out
    # SafeStr is not escaped
    assert "<b>bold</b>" in out
    # Nested Tag renders as HTML
    assert "<mytag>X</mytag>" in out


def test_str_calls_render() -> None:
    tag = MyTag("Hi")
    assert str(tag) == tag.render() == "<mytag>Hi</mytag>"


def test_repr_no_attrs_no_children() -> None:
    tag = MyTag()
    # Format: MyTag()
    assert repr(tag) == "MyTag()"


def test_repr_with_attrs_and_children() -> None:
    tag = MyTag("A", id_=10)  # note: __repr__ shows original _attrs keys (id_), not cleaned keys
    r = repr(tag)
    assert r == "MyTag(attributes={'id_': 10}, children=('A',))"


def test_to_dict_and_to_json_roundtrip() -> None:
    children: tuple[Any, ...] = ("A", 7, SafeStr("<i>x</i>"))
    attrs: dict[str, Any] = {"data_test_id": 42, "checked": True, "hidden": False}

    tag = MyTag(*children, **attrs)

    as_dict = tag.to_dict()
    assert as_dict["name"] == "MyTag"
    assert as_dict["attributes"] == attrs  # raw attrs dict (unmodified keys/values)
    assert as_dict["children"] == children

    as_json = tag.to_json()
    # Ensure it's valid JSON and matches the dict produced
    parsed = json.loads(as_json)
    assert parsed == {
        "name": "MyTag",
        "attributes": attrs,
        "children": list(children),  # json converts tuple -> list
    }


def test_from_dict_and_from_json_roundtrip() -> None:
    """This test encodes the intended behavior for from_dict/from_json."""
    original = HTML_SAMPLE
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
