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
# From pyproject.toml -> version
VERSION := `awk -F\" '/^version/{print $2}' pyproject.toml`
# From pyproject.toml -> requires-python
PYTHON_VERSIONS := `awk -F'[^0-9]+' '/requires-python/{for(i=$3;i<$5;)printf(i-$3?" ":"")$2"."i++}' pyproject.toml`
# Alternative option: From pyproject.toml -> classifiers
# PYTHON_VERSIONS := `awk -F'"| :: ' '/Python :: 3\.1/{print $4}' pyproject.toml`

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

# just evaluate VARIABLE_NAME
[group('meta')]
@evaluate *ARGS:
    just --evaluate {{ ARGS }}

# Run a recipe for each argument value in ARGS (calls RECIPE once per ARG)
[doc]
[group('meta')]
[private]
@run-each RECIPE +ARGS:
    for ARG in {{ ARGS }}; do just "{{ RECIPE }}" "$ARG"; done

# Run a command and turn absolute paths into relative paths everywhere in its output
[doc]
[group('meta')]
[no-exit-message]
[private]
run-with-relative-paths +CMD:
    #!/usr/bin/env bash
    set -euo pipefail
    {{ CMD }} 2>&1 | sed "s|$HERE||g"

# Run a python module using uv
[group('uv')]
@run-py-module TARGET=".":
    just run --module "{{ TARGET }}"

# Run a python script using uv
[group('uv')]
@run-py-script TARGET=".":
    just run --script "{{ TARGET }}"

# uv run helper
[doc]
[group('uv')]
@run +ARGS:
    just run-with-relative-paths uv run -q --extra all --frozen {{ ARGS }}

# Upgrade all dependencies using uv (uv don't support pyproject.toml update yet)
[group('uv')]
upgrade-dependencies:
    uv sync --extra all -U

# endregion Just CLI helpers (meta)
# region ----> QA <----

# Format code and auto-fix simple issues with Ruff
[group('qa')]
format OUTPUT_FORMAT="full" UNSAFE="":
    # Format Python files using Ruff's formatter (writes changes to disk).
    just run -- ruff format .
    # Check for lint violations, apply fixes to resolve lint violations(only for fixable rules),
    # show an enumeration of all fixed lint violations.
    just run -- ruff check --fix --output-format={{OUTPUT_FORMAT}} {{UNSAFE}} .
    # Check for spelling and grammar violations and apply fixes
    just run -- typos --write-changes --format={{ if OUTPUT_FORMAT == "concise" { "brief" } else { "long" } }}
    just run -- codespell --write-changes

# [including *unsafe* fixes, NOTE: --unsafe-fixes may change code intent (be careful)]
[group('qa')]
format-unsafe: && (format "concise" "--unsafe-fixes")

# [print diagnostics concisely, one per line]
[group('qa')]
@format-concise: && (format "concise")

# [group messages by file]
[group('qa')]
@format-grouped: && (format "grouped")

# Check for formatting, lint violations
[group('qa')]
lint OUTPUT_FORMAT="full":
    # Avoid writing any formatted files back; instead, exit with a non-zero
    # status code if any files would have been modified, and zero otherwise,
    # and the difference between the current file and how the formatted file would look like.
    just run -- ruff format --check --output-format={{OUTPUT_FORMAT}} .
    # Check for lint violations
    just run -- ruff check --output-format={{OUTPUT_FORMAT}} .
    # Check for spelling and grammar violations
    just run -- typos --format={{ if OUTPUT_FORMAT == "concise" { "brief" } else { "long" } }}
    just run -- codespell

# [print diagnostics concisely, one per line]
[group('qa')]
@lint-concise: && (lint "concise")

# [group messages by file]
[group('qa')]
@lint-grouped: && (lint "grouped")

# Type check the project with Ty and pyrefly
[group('qa')]
type-check TARGET=".":
    just run -- ty check "{{TARGET}}"
    just run -- pyrefly check "{{TARGET}}"

# Type check the project with Ty and pyrefly - Print diagnostics concisely, one per line
[group('qa')]
type-check-concise TARGET=".":
    just run -- ty check --output-format=concise "{{TARGET}}"
    just run -- pyrefly check --output-format=min-text "{{TARGET}}"

# Annotate types using pyrefly infer
[group('qa')]
type-annotate TARGET="src":
    just run -- pyrefly infer "{{ TARGET }}"

# Run all the formatting, linting, and type checking, for local development.
[group('qa')]
qa: format type-check

# Visualize Ruff analyze graph as JSON (uses rich for display)
[group('qa')]
@ruff-graph: (title "Ruff - Graph")
    just run -- ruff analyze graph -q | rich - --force-terminal --json

# endregion QA
# region ----> Test <----

# Run all the tests
[group('test')]
test:
    just run -- pytest

# Run all the tests on a specified Python version
[group('test')]
test-on PY_VERSION:
    just run --python={{ PY_VERSION }} --isolated -- pytest

# Run all the tests for all the supported Python versions
[group('test')]
@test-on-supported-py-versions:
    just run-each test-on $PYTHON_VERSIONS

# Run all the tests, but on failure, drop into the debugger
[group('test')]
pdb MAXFAIL="10" *ARGS:
    @echo "Running with arg: {{ ARGS }}"
    just run -- pytest --pdb --maxfail={{ MAXFAIL }} {{ ARGS }}

# TDD mode: stop at the first test failure
[group('test')]
tdd: && (pdb "1")

# Show the 10 slowest tests (timings)
[group('test')]
test-durations:
    just run -- pytest --durations=10 -vvv --no-header

# endregion Test
# region ----> Coverage <----

# Run Test Coverage
[group('coverage')]
test-coverage:
    just run -- pytest --cov -q

# Build, store and open the HTML coverage report
[group('coverage')]
coverage-html:
    just run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=html
    open ./htmlcov/index.html

# Build and store the XML coverage report
[group('coverage')]
coverage-xml:
    just run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=xml

# Build and store the MD coverage report - Automatically find diff lines that need test coverage.
[group('coverage')]
coverage-md: coverage-xml
    diff-cover coverage.xml --format "markdown:report.md"
    just readmd "report.md"

# endregion Coverage
# region ----> Rich <----

# Print a centered title with a magenta rule
[doc]
[group('rich')]
@title TEXT="":
    rich "{{ TEXT }}" --rule --rule-style "red" --rule-char "=" --style "bold white on magenta"

# Print text inside a double-line panel with optional title and caption
[doc]
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
[doc]
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
    just run -- mkdocs serve -a localhost:3000

# Build docs
[group('docs')]
doc-build:
    just run -- mkdocs gh-deploy --force

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
