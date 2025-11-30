import pathlib
from collections import defaultdict

import pytest
from scripts.missing_examples import (
    check_docstring_for_example,
    extract_callables_from_file,
    main,
)


@pytest.fixture
def project_dirs(tmp_path):
    """Create the standard project directory structure for testing main()."""
    src_air = tmp_path / "src" / "air"
    src_air.mkdir(parents=True)
    return tmp_path, src_air


def test_check_docstring_for_example():
    assert check_docstring_for_example("Example: foo()") is True
    assert check_docstring_for_example("No example here") is False
    assert check_docstring_for_example(None) is False


def test_extract_callables_from_file(tmp_path):
    test_code = '''
def function_with_example():
    """Function with example.

    Example:
        function_with_example()
    """
    pass

def function_without_example():
    """Function without example."""
    pass

class ClassWithExample:
    """Class with example.

    Example:
        obj = ClassWithExample()
    """

    def method_with_example(self):
        """Method with example.

        Example:
            obj.method_with_example()
        """
        pass

    def method_without_example(self):
        """Method without example."""
        pass
'''

    test_file = tmp_path / "test_file.py"
    test_file.write_text(test_code)

    missing_examples = defaultdict(list)
    extract_callables_from_file(test_file, missing_examples, tmp_path)

    results = missing_examples[pathlib.Path("test_file.py")]

    assert "function: function_without_example" in results
    assert "method: ClassWithExample.method_without_example" in results
    assert "function: function_with_example" not in results
    assert "method: ClassWithExample.method_with_example" not in results


def test_extract_callables_from_file_handles_syntax_error(tmp_path):
    """Test that extract_callables_from_file handles syntax errors gracefully."""
    test_code = '''def bad_function(
    """Invalid syntax."""
    pass
'''
    test_file = tmp_path / "test_file.py"
    test_file.write_text(test_code)

    missing_examples = defaultdict(list)
    extract_callables_from_file(test_file, missing_examples, tmp_path)

    # Should not crash, and should not add any entries
    assert len(missing_examples) == 0


def test_extract_callables_from_file_handles_unicode_decode_error(tmp_path):
    """Test that extract_callables_from_file handles unicode decode errors gracefully."""
    # Create a file with invalid UTF-8
    temp_file = tmp_path / "test.py"
    temp_file.write_bytes(b"\x80\x81\x82")

    missing_examples = defaultdict(list)
    extract_callables_from_file(temp_file, missing_examples, tmp_path)

    # Should not crash, and should not add any entries
    assert len(missing_examples) == 0


def test_extract_callables_from_file_skips_private_methods(tmp_path):
    """Test that private methods (starting with _) are skipped."""
    test_code = '''
class MyClass:
    """Class without example."""

    def _private_method(self):
        """Private method without example."""
        pass

    def public_method(self):
        """Public method without example."""
        pass
'''
    test_file = tmp_path / "test_file.py"
    test_file.write_text(test_code)

    missing_examples = defaultdict(list)
    extract_callables_from_file(test_file, missing_examples, tmp_path)

    results = missing_examples[pathlib.Path("test_file.py")]

    # Private method should not be in results
    assert not any("_private_method" in item for item in results)
    # Public method should be in results
    assert "method: MyClass.public_method" in results
    # Class should be in results
    assert "class: MyClass" in results


def test_main_finds_missing_examples(project_dirs, capsys):
    """Test that main() finds callables without examples."""
    tmp_path, src_air = project_dirs

    # Create a test file with missing examples
    test_file = src_air / "test_module.py"
    test_file.write_text('''
def function_without_example():
    """Function without example."""
    pass

class ClassWithoutExample:
    """Class without example."""
    pass
''')

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    assert "Callables missing examples:" in captured.out
    assert "function: function_without_example" in captured.out
    assert "class: ClassWithoutExample" in captured.out
    assert "Total missing examples:" in captured.out


def test_main_all_callables_have_examples(project_dirs, capsys):
    """Test that main() reports success when all callables have examples."""
    tmp_path, src_air = project_dirs

    # Create a test file with all examples present
    test_file = src_air / "test_module.py"
    test_file.write_text('''
def function_with_example():
    """Function with example.

    Example:
        function_with_example()
    """
    pass
''')

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    assert "All callables have examples!" in captured.out


def test_main_excludes_excluded_paths(project_dirs, capsys):
    """Test that main() excludes files in excluded_paths."""
    tmp_path, src_air = project_dirs

    # Create the tags/models directory
    tags_models = src_air / "tags" / "models"
    tags_models.mkdir(parents=True)

    # Create stock.py which should be excluded
    stock_file = tags_models / "stock.py"
    stock_file.write_text('''
def function_without_example():
    """Function without example."""
    pass
''')

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    # Should not report missing examples from stock.py
    assert "function: function_without_example" not in captured.out
    # Should show it was excluded
    assert "Excluded files:" in captured.out
    assert "tags/models/stock.py" in captured.out


def test_main_excludes_svg_file(project_dirs, capsys):
    """Test that main() excludes tags/models/svg.py."""
    tmp_path, src_air = project_dirs

    # Create the tags/models directory
    tags_models = src_air / "tags" / "models"
    tags_models.mkdir(parents=True)

    # Create svg.py which should be excluded
    svg_file = tags_models / "svg.py"
    svg_file.write_text('''
def function_without_example():
    """Function without example."""
    pass
''')

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    # Should not report missing examples from svg.py
    assert "function: function_without_example" not in captured.out
    # Should show it was excluded
    assert "Excluded files:" in captured.out
    assert "tags/models/svg.py" in captured.out


def test_main_skips_init_files(project_dirs, capsys):
    """Test that main() skips __init__.py files."""
    tmp_path, src_air = project_dirs

    # Create __init__.py with missing examples
    init_file = src_air / "__init__.py"
    init_file.write_text('''
def function_without_example():
    """Function without example."""
    pass
''')

    main(project_root=tmp_path)

    captured = capsys.readouterr()
    # Should not report anything since __init__.py is skipped
    assert "All callables have examples!" in captured.out


def test_main_handles_empty_src_directory(project_dirs, capsys):
    """Test that main() handles an empty src/air directory."""
    tmp_path, _src_air = project_dirs

    # src_air exists but is empty
    main(project_root=tmp_path)

    captured = capsys.readouterr()
    assert "All callables have examples!" in captured.out


def test_extract_callables_from_file_handles_async_functions(tmp_path):
    """Test that async functions are properly detected."""
    test_code = '''
async def async_function_with_example():
    """Async function with example.

    Example:
        await async_function_with_example()
    """
    pass

async def async_function_without_example():
    """Async function without example."""
    pass

class MyClass:
    """Class with example.

    Example:
        obj = MyClass()
    """

    async def async_method_with_example(self):
        """Async method with example.

        Example:
            await obj.async_method_with_example()
        """
        pass

    async def async_method_without_example(self):
        """Async method without example."""
        pass
'''
    test_file = tmp_path / "test_file.py"
    test_file.write_text(test_code)

    missing_examples = defaultdict(list)
    extract_callables_from_file(test_file, missing_examples, tmp_path)

    results = missing_examples[pathlib.Path("test_file.py")]

    # Async function without example should be in results
    assert "function: async_function_without_example" in results
    # Async function with example should not be in results
    assert "function: async_function_with_example" not in results
    # Async method without example should be in results
    assert "method: MyClass.async_method_without_example" in results
    # Async method with example should not be in results
    assert "method: MyClass.async_method_with_example" not in results
    # Class should not be in results (it has an example)
    assert "class: MyClass" not in results
