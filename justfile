# =============================================================================
# justfile: A makefile like build script -- Command Runner
# =============================================================================
# USAGE:
#   just --list
#   just <RECIPE>
#   just <RECIPE> <PARAM_VALUE1> ...
#
# Docs:
#   * https://just.systems/man/en/
# =============================================================================
# -- Load environment-variables from "$HERE/.env" file (if exists)

set dotenv-load := true
set dotenv-filename := ".env"
set export := true

# -----------------------------------------------------------------------------
# CONFIG:
# -----------------------------------------------------------------------------

HERE := justfile_directory()
MARKER_DIR := HERE
PYTHON_VERSION := trim(read(".python-version"))
# From pyproject.toml -> classifiers
PYTHON_VERSIONS := `awk -F'"| :: ' '/Python :: 3\.1/{print $4}' pyproject.toml`
# From pyproject.toml -> requires-python
PYTHON_VERSIONS_2 := `awk -F'[^0-9]+' '/requires-python/{for(i=$3;i<$5;)printf(i-$3?" ":"")$2"."i++}' pyproject.toml`
# From pyproject.toml -> version
VERSION := `awk -F\" '/^version/{print $2}' pyproject.toml`

# -----------------------------------------------------------------------------
# RECIPES:
# -----------------------------------------------------------------------------
# region ----> Just CLI helpers (meta) <----

# List all the justfile recipes
[group('meta')]
@list:
    just --list

# Show the development Python version and the package's supported versions
[group('meta')]
@python-versions:
    echo "Development Python version: {{ PYTHON_VERSION }}"
    echo "Supported Python versions: {{ PYTHON_VERSIONS }}"

# List recipe groups
[group('meta')]
@groups:
    just --groups

# List variable names
[group('meta')]
@variables:
    just --variables

# just evaluate VARIABLE_NAME # show one
[group('meta')]
@evaluate *ARGS:
    just --evaluate {{ ARGS }}

# endregion Just CLI helpers (meta)
# region ----> QA <----

# Format code and auto-fix simple issues with Ruff
[group('qa')]
format:
    # Format Python files using Ruff's formatter (writes changes to disk).
    uv run -- ruff format .
    # Check for lint violations, apply fixes to resolve lint violations(only for fixable rules),
    # show an enumeration of all fixed lint violations.
    uv run -- ruff check --fix --show-fixes .
    # Format justfile (uses Just's formatter).
    just --fmt --unstable

# Run Ruff checks without fixing to report issues
[group('qa')]
lint:
    # Avoid writing any formatted files back; instead, exit with a non-zero
    # status code if any files would have been modified, and zero otherwise,
    # and the difference between the current file and how the formatted file would look like.
    uv run -- ruff format --diff .
    # Check for lint violations
    uv run -- ruff check .

# Type check the project with Ty and pyrefly
[group('qa')]
type-check:
    uv run -- ty check .
    uv run -- pyrefly check .

# Annotate types using pyrefly infer
[group('qa')]
type-annotate TARGET="src":
    uv run -- pyrefly infer "{{ TARGET }}"

# Run all the formatting, linting, and type checking, for local development.
[group('qa')]
qa: format type-check

# Visualize Ruff analyze graph as JSON (uses rich for display)
[group('qa')]
@ruff-graph: (title "Ruff - Graph")
    ruff analyze graph -q | rich - --force-terminal --json

# endregion QA
# region ----> Test <----

# Run all the tests for all the supported Python versions
[group('test')]
test-on-supported-py-versions: (test-on "3.10") (test-on "3.11") \
    (test-on "3.12") (test-on "3.13") (test-on "3.13t")

@test-on-loop +PY_VERSIONS:
    for PY_VERSION in {{ PY_VERSIONS }}; do echo $PY_VERSION; done

@test-on-loop-1 : (test-on-2 "3.10, 3.11 3.12 3.13 3.13t")

@test-on-loop-2 PY_VERSION:
    echo {{PY_VERSION}}

# Run all the tests for all the supported Python versions
@test-on-all: && (run-each "test-on-2" "$PYTHON_VERSIONS")

# Run a 1-arg recipe for each arg (private)
[group('meta')]
[private]
@run-each RECIPE *ARGS:
    for ARG in {{ARGS}}; do just "{{RECIPE}}" "$ARG"; done

#    for ARG in {{ARGS}}; do
#        just "{{RECIPE}}" "$ARG"
#    done

# Run all the tests
[group('test')]
test:
    uv run -- pytest

test-1:
    @echo "Python: {{ env_var_or_default("UV_PYTHON", PYTHON_VERSION) }}"
    uv run --isolated -- pytest

# Run all the tests on a specified Python version
[group('test')]
test-on PY_VERSION:
    uv run --python={{ PY_VERSION }} --isolated -- pytest

# Run all the tests on a specified Python version
test-on-2  $UV_PYTHON $UV_ISOLATED="1":
    @echo "Python: $UV_PYTHON"
    uv run --isolated -- pytest

# Run all the tests on a specified Python version
test-on-4  $UV_PYTHON $UV_ISOLATED="1": test-1

test-on-3 PY_VERSION:
    UV_PYTHON := "$PY_VERSION"
    @echo "Python: $PY_VERSION"
    uv run --isolated -- pytest

# Run all the tests, but on failure, drop into the debugger
[group('test')]
pdb MAXFAIL="10" *ARGS:
    @echo "Running with arg: {{ ARGS }}"
    uv run -- pytest --pdb --maxfail={{ MAXFAIL }} {{ ARGS }}

# TDD mode: stop at the first test failure
[group('test')]
tdd: && (pdb "1")

# Show the 10 slowest tests (timings)
[group('test')]
test-durations:
    uv run -- pytest --durations=10 -vvv --no-header

# endregion Test
# region ----> Coverage <----

# Run Test Coverage
[group('coverage')]
test-coverage:
    uv run -- pytest --cov -q

# Build, store and open the HTML coverage report
[group('coverage')]
coverage-html:
    uv run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=html
    open ./htmlcov/index.html

# Build and store the XML coverage report
[group('coverage')]
coverage-xml:
    uv run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=xml

# Build and store the MD coverage report - Automatically find diff lines that need test coverage.
[group('coverage')]
coverage-md: coverage-xml
    diff-cover coverage.xml --format markdown:report.md
    open report.md

# endregion Coverage
# region ----> Rich <----

# Print a centered title with a magenta rule
[group('rich')]
@title TEXT="":
    rich "{{ TEXT }}" --rule --rule-style "red" --rule-char "=" --style "bold white on magenta"

# Print text inside a double-line panel with optional title and caption
[group('rich')]
@panel TEXT="" TITLE="" CAPTION="":
    rich "{{ TEXT }}" --title "{{ TITLE }}" --caption "{{ CAPTION }}" \
     --print --panel double --center --panel-style "magenta"

# View a Python file with syntax highlight, line numbers, and guides
[group('rich')]
@readpy FILE_PATH: (title FILE_PATH)
    rich "{{ FILE_PATH }}" --syntax --line-numbers --guides --theme dracula --pager

# endregion Rich
# region ----> Docs <----

# View a Markdown file with rich using the Dracula theme
[group('docs')]
@readmd FILE_NAME: (title FILE_NAME)
    rich "{{ FILE_NAME }}" --markdown --theme dracula --emoji --hyperlinks --pager

# Open README.md with rich
[group('docs')]
@readme: (readmd "README.md")

# Open CONTRIBUTING.md with rich
[group('docs')]
@contributing: (readmd "CONTRIBUTING.md")

# Open CHANGELOG.md with rich
[group('docs')]
@changelog: (readmd "CHANGELOG.md")

# Serve docs locally
[group('docs')]
doc:
    uv run -- mkdocs serve -a localhost:3000

# Build and deploy docs
[group('docs')]
doc-build:
    uv run -- mkdocs gh-deploy --force

# endregion Docs

# Build the project, useful for checking that packaging is correct
[group('build')]
build:
    rm -rf build
    rm -rf dist
    uv build

# Print the current version of the project
[group('release')]
version:
    @echo "Current version is {{ VERSION }}"

# Tag the current version in git and push to GitHub
[group('release')]
tag:
    echo "Tagging version v{{ VERSION }}"
    git tag -a v{{ VERSION }} -m "Creating version v{{ VERSION }}"
    git push origin v{{ VERSION }}
