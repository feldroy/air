# tests/test_tag.py
from __future__ import annotations

from examples.html_sample import HTML_SAMPLE

from air import SafeStr, Tag


class MyTag(Tag):
    """Simple concrete Tag subclass used in tests."""


def test_render_basic_text() -> None:
    tag = MyTag("Hello", " World")
    rendered = tag.render()
    assert rendered == "Hello World"


def test_render_escapes_plain_text_and_preserves_safestr_and_child_tag() -> None:
    child_plain = "<script>alert(1)</script>"
    child_safe = SafeStr("<b>bold</b>")
    child_tag = MyTag("X")

    tag = MyTag(child_plain, child_safe, child_tag)
    out = tag.render()

    # Plain string is escaped
    assert out == "&lt;script&gt;alert(1)&lt;/script&gt;<b>bold</b>X"


def test_str_calls_render() -> None:
    tag = MyTag("Hi")
    assert str(tag) == tag.render() == "Hi"


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
