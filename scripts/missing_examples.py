"""
A utility script to look for callables (functions, classes, and methods)
that don't have examples for them. It lists them for easy reference.

Run:
    `just run-py-module scripts.missing_examples`
"""

import ast
import pathlib
from collections import defaultdict

import typer
from rich import print


def check_docstring_for_example(docstring: str | None) -> bool:
    """Check if docstring contains an example."""
    if not docstring:
        return False
    return "Example:" in docstring


def extract_callables_from_file(file_path: pathlib.Path, missing_examples: dict):
    """Extract all callables from a Python file."""
    try:
        with pathlib.Path(file_path).open("r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (SyntaxError, UnicodeDecodeError):
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Function or method
            if not check_docstring_for_example(ast.get_docstring(node)):
                missing_examples[file_path.relative_to("src")].append(f"function: {node.name}")

        elif isinstance(node, ast.ClassDef):
            # Class
            if not check_docstring_for_example(ast.get_docstring(node)):
                missing_examples[file_path.relative_to("src")].append(f"class: {node.name}")

            # Check methods in class
            for item in node.body:
                if (
                    isinstance(item, ast.FunctionDef)
                    and not item.name.startswith("_")
                    and not check_docstring_for_example(ast.get_docstring(item))
                ):
                    # Skip private methods (start with _)
                    missing_examples[file_path.relative_to("src")].append(f"method: {node.name}.{item.name}")


def main():
    """This function looks for callables (functions, classes, and methods)
    and looks for those that don't have examples in them. It prints the results
    to the terminal using the `rich` library.
    """

    src_path = pathlib.Path("src/air")
    missing_examples = defaultdict(list)

    # Paths to exclude from analysis (relative to src/air/)
    excluded_paths = {
        "tags/models/stock.py",  # Auto-generated HTML tag classes
        "tags/models/svg.py",  # Auto-generated SVG tag classes
    }

    # Walk through all Python files in src/air
    excluded_files = []
    for file_path in src_path.rglob("*.py"):
        if file_path.name != "__init__.py":  # Skip __init__.py files
            # Check if this file should be excluded
            relative_path = str(file_path.relative_to("src/air"))
            if relative_path not in excluded_paths:
                extract_callables_from_file(file_path, missing_examples)
            else:
                excluded_files.append(relative_path)

    # Print results
    if missing_examples:
        print("[bold red]Callables missing examples:[/bold red]\n")
        for file_path, callables in sorted(missing_examples.items()):
            print(f"[bold blue]{file_path}[/bold blue]:")
            for callable_info in callables:
                print(f"  • {callable_info}")
            print()

        total_missing = sum(len(callables) for callables in missing_examples.values())
        print(f"[bold yellow]Total missing examples: {total_missing}[/bold yellow]")
    else:
        print("[bold green]All callables have examples! 🎉[/bold green]")

    # Show excluded files if any
    if excluded_files:
        print(f"\n[dim]Excluded files: {', '.join(excluded_files)}[/dim]")


if __name__ == "__main__":
    typer.run(main)
