"""
A utility script to look for callables (functions, classes, and methods)
that don't have examples for them. It lists them for easy reference.

Run:
    `uv run python scripts/missing_examples.py` - Show all missing examples
    `uv run python scripts/missing_examples.py --mode baseline` - Generate baseline
    `uv run python scripts/missing_examples.py --mode check` - Check against baseline
"""

import ast
import json
import pathlib
import sys
from collections import defaultdict

import typer
from rich import print

BASELINE_FILE = ".missing_examples_baseline.json"
SRC_PATH = "src/air"

# Paths to exclude from analysis (relative to SRC_PATH)
EXCLUDED_PATHS = {
    "tags/models/stock.py",  # Auto-generated HTML tag classes
    "tags/models/svg.py",  # Auto-generated SVG tag classes
}


def check_docstring_for_example(docstring: str | None) -> bool:
    """Check if docstring contains an example.

    Returns:
        True if the docstring contains an example, False otherwise.
    """
    if not docstring:
        return False
    return "Example:" in docstring


def collect_missing_examples(project_root: pathlib.Path) -> tuple[dict[pathlib.Path, list[str]], list[str]]:
    """Collect all missing examples from the codebase.

    Returns:
        Tuple of (missing_examples dict, list of excluded files).
    """
    src_path = project_root / SRC_PATH
    missing_examples = defaultdict(list)
    excluded_files = []

    # Walk through all Python files in SRC_PATH
    for file_path in src_path.rglob("*.py"):
        if file_path.name != "__init__.py":  # Skip __init__.py files
            # Check if this file should be excluded
            relative_path = file_path.relative_to(src_path).as_posix()
            if relative_path not in EXCLUDED_PATHS:
                extract_callables_from_file(file_path, missing_examples, src_path)
            else:
                excluded_files.append(relative_path)

    return dict(missing_examples), excluded_files


def load_baseline(project_root: pathlib.Path) -> dict[str, list[str]]:
    """Load baseline from JSON file.

    Returns:
        Dictionary containing the baseline missing examples data.
    """
    baseline_path = project_root / BASELINE_FILE
    if not baseline_path.exists():
        return {}

    with baseline_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_baseline(project_root: pathlib.Path, missing_examples: dict) -> None:
    """Save baseline to JSON file."""
    baseline_path = project_root / BASELINE_FILE

    # Convert Path keys to strings for JSON serialization
    serializable = {str(k): v for k, v in missing_examples.items()}

    with baseline_path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, sort_keys=True)
        f.write("\n")


def find_new_missing(current: dict, baseline: dict) -> dict[str, list[str]]:
    """Find missing examples that are new (not in baseline).

    Returns:
        Dictionary of files and callables with new missing examples.
    """
    new_missing = {}

    for file_path, callables in current.items():
        file_path_str = str(file_path)
        baseline_callables = set(baseline.get(file_path_str, []))
        current_callables = set(callables)

        # Find callables that are in current but not in baseline
        new_callables = current_callables - baseline_callables

        if new_callables:
            new_missing[file_path_str] = sorted(new_callables)

    return new_missing


def extract_callables_from_file(file_path: pathlib.Path, missing_examples: dict, src_path: pathlib.Path) -> None:
    """Extract all callables from a Python file."""
    try:
        tree = ast.parse(file_path.read_text())
    except (SyntaxError, UnicodeDecodeError):
        return

    # Process top-level items only
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Top-level function (sync or async)
            if not check_docstring_for_example(ast.get_docstring(node)):
                missing_examples[file_path.relative_to(src_path)].append(f"function: {node.name}")

        elif isinstance(node, ast.ClassDef):
            # Class
            if not check_docstring_for_example(ast.get_docstring(node)):
                missing_examples[file_path.relative_to(src_path)].append(f"class: {node.name}")

            # Check methods in class
            for item in node.body:
                if (
                    isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and not item.name.startswith("_")
                    and not check_docstring_for_example(ast.get_docstring(item))
                ):
                    # Skip private methods (start with _)
                    missing_examples[file_path.relative_to(src_path)].append(f"method: {node.name}.{item.name}")


def _print_missing_examples(missing_examples: dict) -> None:
    """Print missing examples in a formatted way."""
    for file_path, callables in sorted(missing_examples.items()):
        print(f"[bold blue]{file_path}[/bold blue]:")
        for callable_info in callables:
            print(f"  • {callable_info}")
        print()


def main(project_root: pathlib.Path | None = None, mode: str = "report") -> None:
    """This function walks through all Python files in SRC_PATH, identifies callables
    without example sections in their docstrings, and prints the results to the
    terminal using the `rich` library.

    Args:
        project_root: Root directory of the project (defaults to current directory)
        mode: Operation mode:
            - "report" (default): Display all missing examples
            - "baseline": Generate a baseline file of current missing examples
            - "check": Check against baseline and fail if new missing examples found
    """
    if project_root is None:
        project_root = pathlib.Path.cwd()  # pragma: no cover

    # Collect all missing examples
    missing_examples, excluded_files = collect_missing_examples(project_root)

    if mode == "baseline":
        # Generate baseline file
        save_baseline(project_root, missing_examples)
        baseline_path = project_root / BASELINE_FILE
        total = sum(len(v) for v in missing_examples.values())
        print(f"[bold green]✓[/bold green] Baseline saved to {baseline_path}")
        print(f"[dim]  {total} missing examples recorded[/dim]")
        if excluded_files:
            print(f"[dim]  Excluded files: {', '.join(excluded_files)}[/dim]")
        return

    if mode == "check":
        # Check against baseline
        baseline = load_baseline(project_root)

        if not baseline:
            print("[bold red]✗[/bold red] No baseline file found. Generate one with --mode baseline")
            sys.exit(1)

        new_missing = find_new_missing(missing_examples, baseline)

        if new_missing:
            print("[bold red]✗ New missing examples found:[/bold red]\n")
            _print_missing_examples(new_missing)
            total = sum(len(v) for v in new_missing.values())
            print(f"[bold red]Found {total} new missing example(s)[/bold red]")
            print("[dim]Add examples or update baseline with --mode baseline[/dim]")
            sys.exit(1)

        print("[bold green]✓ No new missing examples![/bold green]")
        if excluded_files:
            print(f"[dim]Excluded files: {', '.join(excluded_files)}[/dim]")
        return

    # report mode
    if missing_examples:
        print("[bold red]Callables missing examples:[/bold red]\n")
        _print_missing_examples(missing_examples)
        total_missing = sum(len(callables) for callables in missing_examples.values())
        print(f"[bold yellow]Total missing examples: {total_missing}[/bold yellow]")
    else:
        print("[bold green]All callables have examples! 🎉[/bold green]")

    # Show excluded files if any
    if excluded_files:
        print(f"\n[dim]Excluded files: {', '.join(excluded_files)}[/dim]")


if __name__ == "__main__":
    typer.run(main)
