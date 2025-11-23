import pytest
from scripts.copy_src_example_to_callable import (
    main,
    parse_filename_class,
    update_example_section,
)


@pytest.fixture
def project_dirs(tmp_path):
    """Create the standard project directory structure for testing main()."""
    examples_src = tmp_path / "examples" / "src"
    examples_src.mkdir(parents=True)
    src_air = tmp_path / "src" / "air"
    src_air.mkdir(parents=True)
    return tmp_path, examples_src, src_air


# Tests for parse_filename_class


def test_parse_filename_class_with_class_method() -> None:
    result = parse_filename_class("applications__Air__page.py")
    assert result == ("applications", "Air", "page")


def test_parse_filename_class_with_class_only() -> None:
    result = parse_filename_class("forms__AirForm.py")
    assert result == ("forms", "AirForm", None)


def test_parse_filename_class_with_function() -> None:
    result = parse_filename_class("utils__compute_page_path.py")
    assert result == ("utils", None, "compute_page_path")


def test_parse_filename_class_returns_none_for_test_files() -> None:
    result = parse_filename_class("module__Class__test.py")
    assert result is None


def test_parse_filename_class_returns_none_for_init() -> None:
    result = parse_filename_class("__init__.py")
    assert result is None


def test_parse_filename_class_returns_none_for_non_python_files() -> None:
    result = parse_filename_class("readme.md")
    assert result is None


def test_parse_filename_class_returns_none_for_single_part() -> None:
    result = parse_filename_class("simple.py")
    assert result is None


# Tests for update_example_section


def test_update_example_section_updates_function_docstring(tmp_path) -> None:
    test_code = '''def my_function():
    """Function with example.

    Example:
        old_example()
    """
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "new_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_example()" in updated_content
    assert "old_example()" not in updated_content


def test_update_example_section_updates_class_docstring(tmp_path) -> None:
    test_code = '''class MyClass:
    """Class with example.

    Example:
        old_example()
    """
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, "MyClass", None, "new_class_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_class_example()" in updated_content
    assert "old_example()" not in updated_content


def test_update_example_section_updates_class_method_docstring(tmp_path) -> None:
    test_code = '''class MyClass:
    """Class docstring."""

    def my_method(self):
        """Method with example.

        Example:
            old_method_example()
        """
        pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, "MyClass", "my_method", "new_method_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_method_example()" in updated_content
    assert "old_method_example()" not in updated_content


def test_update_example_section_returns_false_for_missing_example_section(tmp_path, capsys) -> None:
    test_code = '''def my_function():
    """Function without example section."""
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "No Example section found in my_function" in captured.out


def test_update_example_section_returns_false_for_missing_docstring(tmp_path, capsys) -> None:
    test_code = """def my_function():
    pass
"""
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "No Example section found in my_function" in captured.out


def test_update_example_section_returns_false_for_missing_class_when_looking_for_method(tmp_path, capsys) -> None:
    test_code = '''class OtherClass:
    """Other class."""
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, "MyClass", "my_method", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "Class MyClass not found" in captured.out


def test_update_example_section_returns_false_for_missing_method(tmp_path, capsys) -> None:
    test_code = '''class MyClass:
    """Class docstring."""

    def other_method(self):
        """Other method."""
        pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, "MyClass", "my_method", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "Method my_method not found in class MyClass" in captured.out


def test_update_example_section_returns_false_for_missing_function(tmp_path, capsys) -> None:
    test_code = '''def other_function():
    """Other function."""
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "Function my_function not found" in captured.out


def test_update_example_section_returns_false_for_syntax_error(tmp_path, capsys) -> None:
    test_code = '''def my_function(
    """Invalid syntax."""
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "example()")
    assert result is False

    captured = capsys.readouterr()
    assert "Error parsing" in captured.out


def test_update_example_section_handles_async_function(tmp_path) -> None:
    test_code = '''async def my_async_function():
    """Async function with example.

    Example:
        old_example()
    """
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_async_function", "await new_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "await new_example()" in updated_content
    assert "old_example()" not in updated_content


def test_update_example_section_with_multiline_example(tmp_path) -> None:
    test_code = '''def my_function():
    """Function with example.

    Example:
        old_example()
    """
    pass
'''
    expected_example = """result = my_function()
print(result)
for item in result:
    print(item)"""

    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", expected_example)
    assert result is True

    updated_content = temp_file.read_text()
    assert "result = my_function()" in updated_content
    assert "print(result)" in updated_content
    assert "for item in result:" in updated_content
    assert "print(item)" in updated_content


def test_update_example_section_fallback_to_function_when_class_not_found(tmp_path) -> None:
    # When class_name is capitalized but it's actually a function
    test_code = '''def MyFunction():
    """Function with capital name.

    Example:
        old_example()
    """
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    # Pass as if it were a class (method_name=None), but it's actually a function
    result = update_example_section(temp_file, "MyFunction", None, "new_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_example()" in updated_content


def test_update_example_section_handles_decorated_method(tmp_path) -> None:
    test_code = '''class MyClass:
    """Class docstring."""

    @property
    def my_property(self):
        """Property with example.

        Example:
            old_example()
        """
        return self._value
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, "MyClass", "my_property", "new_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_example()" in updated_content
    assert "old_example()" not in updated_content
    # Verify decorator is preserved
    assert "@property" in updated_content


def test_update_example_section_replaces_everything_after_example_marker(tmp_path) -> None:
    # Everything after "Example:" is replaced, so place Example: last in docstrings
    test_code = '''def my_function():
    """Function with content after example.

    Example:
        first_example()

    Note:
        This note comes after the example section.
    """
    pass
'''
    temp_file = tmp_path / "test.py"
    temp_file.write_text(test_code)

    result = update_example_section(temp_file, None, "my_function", "new_example()")
    assert result is True

    updated_content = temp_file.read_text()
    assert "new_example()" in updated_content
    assert "first_example()" not in updated_content
    # Everything after Example: is replaced
    assert "Note:" not in updated_content


# Tests for main function


def test_main_processes_example_files(project_dirs) -> None:
    tmp_path, examples_src, src_air = project_dirs

    # Create an example file
    example_file = examples_src / "utils__my_function.py"
    example_file.write_text("new_example()")

    # Create corresponding source file
    source_file = src_air / "utils.py"
    source_file.write_text('''def my_function():
    """Function with example.

    Example:
        old_example()
    """
    pass
''')

    main(project_root=tmp_path)

    # Verify the source file was updated
    updated_content = source_file.read_text()
    assert "new_example()" in updated_content
    assert "old_example()" not in updated_content


def test_main_handles_missing_examples_directory(tmp_path, capsys) -> None:
    # Don't create examples/src directory, it should not exist
    main(project_root=tmp_path)

    captured = capsys.readouterr()
    assert "src_examples directory not found" in captured.out


def test_main_skips_unparsable_files(project_dirs, capsys) -> None:
    tmp_path, examples_src, _ = project_dirs

    # Create a file that parse_filename_class will return None for
    unparsable_file = examples_src / "simple.py"
    unparsable_file.write_text("# just a comment")

    main(project_root=tmp_path)

    # Should skip the file without any output
    captured = capsys.readouterr()
    assert not captured.out


def test_main_handles_missing_source_file(project_dirs, capsys) -> None:
    tmp_path, examples_src, _ = project_dirs

    # Create an example file that references a non-existent source
    example_file = examples_src / "utils__my_function.py"
    example_file.write_text("new_example()")

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    assert "Source file not found" in captured.out
