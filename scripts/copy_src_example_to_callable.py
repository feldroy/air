"""Script to copy examples/src content into corresponding docstring Example sections.

Run:
    uv run scripts/copy_src_example_to_callable.py
"""

import ast
import re
from pathlib import Path

import typer
from rich.console import Console

console = Console()

ERROR_STYLE = "red"
SUCCESS_STYLE = "green"


def parse_filename_class(filename: str) -> tuple[str, str | None, str | None] | None:
    """Parse filename like 'applications__Air__page.py' into (module, class, method).

    Also supports:
    - 'module__Class.py' format for class-level examples (capitalized second part)
    - 'module__function.py' format for module-level functions (lowercase second part)

    Returns:
        Tuple of (module, class_name, method_name), (module, class_name, None), or (module, None, function_name).
        Returns None if filename is a test file or doesn't match expected pattern.
    """
    if filename.endswith("__test.py") or filename == "__init__.py":
        return None

    if not filename.endswith(".py"):
        return None

    # Remove .py extension
    name = filename[:-3]

    # Split by double underscore
    parts = name.split("__")

    if len(parts) == 2:
        module = parts[0]
        second_part = parts[1]

        # If second part starts with uppercase, it's a class
        if second_part and second_part[0].isupper():
            return module, second_part, None
        # Module-level function
        return module, None, second_part
    if len(parts) >= 3:
        # Class method: module__class__method
        module = parts[0]
        class_name = parts[1]
        method_name = parts[2]
        return module, class_name, method_name

    return None


def update_example_section(
    file_path: Path, class_name: str | None, method_name: str | None, example_content: str
) -> bool:
    """Update the Example section in the specified class, method, or function's docstring.

    Returns:
        True if successful, False otherwise.
    """
    content = file_path.read_text()

    # Parse the AST to find the class and method or function
    try:
        tree = ast.parse(content)
    except SyntaxError:
        console.print(f"Error parsing {file_path}", style=ERROR_STYLE)
        return False

    target_node = None

    if class_name is None:
        # Module-level function
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name:
                target_node = node
                break

        if not target_node:
            console.print(f"Function {method_name} not found in {file_path}", style=ERROR_STYLE)
            return False
    elif method_name is None:
        # Class-level docstring
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                target_node = node
                break

        # Fallback: if class not found, try as module-level function
        if not target_node:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == class_name:
                    target_node = node
                    method_name = class_name
                    class_name = None
                    break

        if not target_node:
            console.print(f"Class or function {class_name} not found in {file_path}", style=ERROR_STYLE)
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
            console.print(f"Class {class_name} not found in {file_path}", style=ERROR_STYLE)
            return False

        # Find the method
        for node in target_class.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name:
                target_node = node
                break

        if not target_node:
            console.print(f"Method {method_name} not found in class {class_name} in {file_path}", style=ERROR_STYLE)
            return False

    # Build callable name for display
    if class_name and method_name:
        callable_name = f"{class_name}.{method_name}"
    elif class_name:
        callable_name = class_name
    else:
        callable_name = method_name

    # Get the docstring
    docstring = ast.get_docstring(target_node)
    if not docstring or "Example:" not in docstring:
        console.print(f"No Example section found in {callable_name}", style=ERROR_STYLE)
        return False

    # Find the actual position of the docstring in the source
    # The docstring is the first statement in the function/class
    if not target_node.body or not isinstance(target_node.body[0], ast.Expr):
        return False

    docstring_node = target_node.body[0].value
    if not isinstance(docstring_node, ast.Constant):
        return False

    # Find the docstring in the source code
    lines = content.split("\n")
    docstring_start_line = docstring_node.lineno - 1

    # Find the indentation by looking at the function/class definition line
    def_line = lines[target_node.lineno - 1]
    def_indent_match = re.match(r"^(\s*)", def_line)
    def_indent = def_indent_match.group(1) if def_indent_match else ""

    # Docstring content indent is definition indent + 4 spaces (standard Python)
    docstring_indent = def_indent + "    "

    # Code examples within docstring get an additional 4 spaces
    code_indent = docstring_indent + "    "

    # Build the new example section with proper indentation
    example_lines = example_content.strip().split("\n")
    indented_example_lines = [code_indent + line if line.strip() else "" for line in example_lines]
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

    new_docstring_content = "\n".join(indented_docstring_lines) + "\n\n" + docstring_indent + "Example:" + new_example

    # Reconstruct the file
    docstring_end_line = docstring_node.end_lineno - 1  # pyrefly: ignore
    before_docstring = "\n".join(lines[:docstring_start_line])
    after_docstring = "\n".join(lines[docstring_end_line + 1 :])

    triple_quote = '"""'
    new_docstring_full = f"{docstring_indent}{triple_quote}{new_docstring_content}{triple_quote}"

    new_content = before_docstring + "\n" + new_docstring_full + "\n" + after_docstring

    # Write back
    file_path.write_text(new_content)
    console.print(f"Updated {callable_name} in {file_path}", style=SUCCESS_STYLE)
    return True


def main(project_root: Path | None = None) -> None:
    """Main function to process all examples/src files."""
    if project_root is None:
        project_root = Path(__file__).parent.parent  # pragma: no cover
    src_examples_dir = project_root / "examples/src"
    src_dir = project_root / "src" / "air"

    if not src_examples_dir.exists():
        console.print(f"src_examples directory not found: {src_examples_dir}", style=ERROR_STYLE)
        return

    # Process each file in examples/src
    for example_file in src_examples_dir.glob("*.py"):
        parsed = parse_filename_class(example_file.name)
        if not parsed:
            continue

        module, class_name, method_name = parsed

        # Read the example content
        example_content = example_file.read_text()

        # Find the corresponding source file
        source_file = src_dir / f"{module}.py"

        if not source_file.exists():
            console.print(f"Source file not found: {source_file}", style=ERROR_STYLE)
            continue

        # Update the example section
        update_example_section(source_file, class_name, method_name, example_content)


if __name__ == "__main__":
    typer.run(main)
