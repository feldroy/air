import pytest

from scripts.copy_src_example_to_callable import parse_filename_class


@pytest.mark.current
def test_parse_filename_class_returns_None_on_filename_ends_with___test_py() -> None:
    """parse_filename_class() returns None on filename ends with '__test.py'."""

    assert parse_filename_class("applications__Air__page__test.py") is None


@pytest.mark.current
def test_parse_filename_class_returns_None_on_filename_ends_with___init_py() -> None:
    """parse_filename_class() returns None on filename is '__init__.py'."""

    assert parse_filename_class("__init__.py") is None




