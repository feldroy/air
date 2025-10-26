import pathlib
import tempfile
from collections import defaultdict
from unittest.mock import patch

from scripts.missing_examples import (
    check_docstring_for_example,
    extract_callables_from_file,
)


def test_check_docstring_for_example():
    assert check_docstring_for_example("Example: foo()") is True
    assert check_docstring_for_example("No example here") is False
    assert check_docstring_for_example(None) is False


def test_extract_callables_from_file():
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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_code)
        temp_path = pathlib.Path(f.name)

    try:
        missing_examples = defaultdict(list)

        # Mock the relative_to call to return a simple path
        with patch.object(pathlib.Path, "relative_to", return_value=pathlib.Path("test_file.py")):
            extract_callables_from_file(temp_path, missing_examples)

        results = missing_examples[pathlib.Path("test_file.py")]

        assert "function: function_without_example" in results
        assert "method: ClassWithExample.method_without_example" in results
        assert "function: function_with_example" not in results
        assert "method: ClassWithExample.method_with_example" not in results

    finally:
        temp_path.unlink()
