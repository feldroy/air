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


@pytest.mark.current
@pytest.mark.parametrize(
    "filename",
    [
        "getCallable.js",
        "example.txt",
        "data.json",
        "script.sh",
        "README.md",
    ],
)
def test_parse_filename_class_returns_None_on_non_python_files(filename: str) -> None:
    """parse_filename_class() returns None when filename is not a python file name."""
    assert parse_filename_class(filename) is None
