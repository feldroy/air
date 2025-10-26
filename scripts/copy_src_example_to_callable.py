"""Script to copy src_examples content into corresponding docstring Example sections.

Run:
    uv run scripts/copy_src_example_to_callable.py
"""

import ast
import re
from pathlib import Path

import typer


def is_filename_not_parseable(filename: str) -> bool:
    """Check if filename is not parseable for `parse_module_class_function_names_from_filename` function."""

    not_a_python_file = not filename.endswith(".py")
    is__init__py = filename == "__init__.py"
    ends_with__test_py = filename.endswith("__test.py")

    return not_a_python_file or is__init__py or ends_with__test_py


def remove_python_extension(filename: str) -> str:
    """Remove .py extension from filename."""
    if not filename.endswith(".py"):
        raise ValueError(f"Filename {filename} does not end with .py")

    return filename[:-3]


def split_name_by_double_underscore(name: str) -> list[str]:
    """Split name by double underscore."""
    return name.split("__")


def get_module_level_function_name_parts(
    name_parts: list[str, str],
) -> tuple[str, None, str]:
    """Get (module, None, function) tuple from module-level function name parts


    Example: ["requests", "get"] from requests__get.py filename.
    """

    assert len(name_parts) == 2

    module_name = name_parts[0]
    class_name = None
    function_name = name_parts[1]

    return (module_name, class_name, function_name)


def get_module_class_method_name_parts(
    name_parts: list[str, str, str],
) -> tuple[str, str, str]:
    """Get (module, class, method) tuple from name_parts list of strings.


    Example: ["applications", "Air", "page"] from applications__Air__page.py filename
    """

    assert len(name_parts) >= 3

    module_name = name_parts[0]
    class_name = name_parts[1]
    method_name = name_parts[2]

    return (module_name, class_name, method_name)


def is_name_a_module_level_function(name_parts: list[str]) -> bool:
    """Check if name_parts is a 2 itemed list representing a module-level function name split by double underscore.

    Example: ["request", "get"] from requests__get.py filename.
    """
    return len(name_parts) == 2


def is_name_a_module_class_method(name_parts: list[str]) -> bool:
    """Check if name_parts is a 3 itemed list representing a module-class-method name split by double underscore.

    Example: ["applications", "Air", "get"] from applications__Air__get.py filename.
    """
    return len(name_parts) >= 3


def parse_module_class_function_names_from_filename(
    filename: str,
) -> tuple[str, str | None, str] | None:
    """Parse filename like 'applications__Air__page.py' into (module, class, method).

    Also supports 'module__function.py' format for module-level functions.
    Returns (module, class_name, method_name) or (module, None, function_name).
    Returns None if filename is a test file or doesn't match expected pattern.
    """
    if is_filename_not_parseable(filename):
        return None

    name = remove_python_extension(filename)

    name_parts = split_name_by_double_underscore(name)

    if is_name_a_module_level_function(name_parts):
        return get_module_level_function_name_parts(name_parts)
    elif is_name_a_module_class_method(name_parts):
        return get_module_class_method_name_parts(name_parts)
    else:
        return None


def update_example_section(
    file_path: Path, class_name: str | None, method_name: str, example_content: str
) -> bool:
    """Update the Example section in the specified method or function's docstring.

    Returns True if successful, False otherwise.
    """
    content = file_path.read_text()

    # Parse the AST to find the class and method or function
    try:
        tree = ast.parse(content)
    except SyntaxError:
        typer.secho(f"Error parsing {file_path}")
        return False

    target_method = None

    if class_name is None:
        # Module-level function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                target_method = node
                break

        if not target_method:
            typer.secho(f"Function {method_name} not found in {file_path}")
            return False
    else:
        # Class method
        # Find the class
        target_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                target_class = node
                break

        if not target_class:
            typer.secho(f"Class {class_name} not found in {file_path}")
            return False

        # Find the method
        for node in target_class.body:
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                target_method = node
                break

        if not target_method:
            typer.secho(
                f"Method {method_name} not found in class {class_name} in {file_path}"
            )
            return False

    # Get the docstring
    docstring = ast.get_docstring(target_method)
    if not docstring or "Example:" not in docstring:
        callable_name = f"{class_name}.{method_name}" if class_name else method_name
        typer.secho(f"No Example section found in {callable_name}")
        return False

    # Find the actual position of the docstring in the source
    # The docstring is the first statement in the function
    if not target_method.body or not isinstance(target_method.body[0], ast.Expr):
        return False

    docstring_node = target_method.body[0].value
    if not isinstance(docstring_node, ast.Constant):
        return False

    # Find the docstring in the source code
    lines = content.split("\n")
    docstring_start_line = docstring_node.lineno - 1

    # Find the indentation by looking at the function definition line
    func_line = lines[target_method.lineno - 1]
    func_indent_match = re.match(r"^(\s*)", func_line)
    func_indent = func_indent_match.group(1) if func_indent_match else ""

    # Docstring content indent is function indent + 4 spaces (standard Python)
    docstring_indent = func_indent + "    "

    # Code examples within docstring get an additional 4 spaces
    code_indent = docstring_indent + "    "

    # Build the new example section with proper indentation
    example_lines = example_content.strip().split("\n")
    indented_example_lines = [
        code_indent + line if line.strip() else "" for line in example_lines
    ]
    new_example = "\n\n" + "\n".join(indented_example_lines) + "\n" + docstring_indent

    # Split the docstring at "Example:"
    parts = docstring.split("Example:", 1)
    before_example = parts[0]

    # Reconstruct the docstring with proper indentation
    # First line of docstring doesn't get extra indent
    docstring_lines = before_example.rstrip().split("\n")
    indented_docstring_lines = []
    for i, line in enumerate(docstring_lines):
        if i == 0:
            # First line - no indent
            indented_docstring_lines.append(line)
        elif line.strip():
            # Other lines with content - add docstring indent
            indented_docstring_lines.append(docstring_indent + line)
        else:
            # Empty lines - no indent
            indented_docstring_lines.append("")

    new_docstring_content = (
        "\n".join(indented_docstring_lines)
        + "\n\n"
        + docstring_indent
        + "Example:"
        + new_example
    )

    # Reconstruct the file
    docstring_end_line = docstring_node.end_lineno - 1  # pyrefly: ignore
    before_docstring = "\n".join(lines[:docstring_start_line])
    after_docstring = "\n".join(lines[docstring_end_line + 1 :])

    triple_quote = '"""'
    new_docstring_full = (
        f"{docstring_indent}{triple_quote}{new_docstring_content}{triple_quote}"
    )

    new_content = before_docstring + "\n" + new_docstring_full + "\n" + after_docstring

    # Write back
    file_path.write_text(new_content)
    callable_name = f"{class_name}.{method_name}" if class_name else method_name
    typer.secho(f"Updated {callable_name} in {file_path}")
    return True


def main():
    """Main function to process all src_examples files."""
    project_root = Path(__file__).parent.parent
    src_examples_dir = project_root / "src_examples"
    src_dir = project_root / "src" / "air"

    if not src_examples_dir.exists():
        typer.secho(f"src_examples directory not found: {src_examples_dir}")
        return

    # Process each file in src_examples
    for example_file in src_examples_dir.glob("*.py"):
        parsed = parse_module_class_function_names_from_filename(example_file.name)
        if not parsed:
            continue

        module, class_name, method_name = parsed

        # Read the example content
        example_content = example_file.read_text()

        # Find the corresponding source file
        source_file = src_dir / f"{module}.py"

        if not source_file.exists():
            typer.secho(f"Source file not found: {source_file}")
            continue

        # Update the example section
        update_example_section(source_file, class_name, method_name, example_content)


if __name__ == "__main__":
    typer.run(main)
