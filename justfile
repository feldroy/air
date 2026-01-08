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
UV_CLI_FLAGS := "--all-extras --all-packages --refresh --reinstall-package air"
BRANCH_NAME := `git branch --show-current`
PREK_RUN_ARG := "--all-files"
# TODO -> Use the line bellow to run prek only on the files changes by the PR branch:
#PREK_RUN_ARG := if BRANCH_NAME == "main" { "--all-files" } else { "--from-ref main" }

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

# Run a command or script using uv.
[doc]
[private]
[group('uv')]
@uv-run +ARGS:
    uv run {{ UV_CLI_FLAGS }} {{ ARGS }}

# Run a command or script using uv, without updating the uv.lock file.
[group('uv')]
@run +ARGS:
    just uv-run -q --frozen {{ ARGS }}

# Run a command or script using uv, in an isolated virtual environment.
[group('uv')]
@run-isolated +ARGS:
    just uv-run --isolated {{ ARGS }}

# Upgrade all dependencies using uv and prek. <Don’t use! For maintainers only!>
[group('uv')]
upgrade-dependencies: && upgrade-prek-hooks upgrade-uv-dependencies

[group('uv')]
upgrade-prek-hooks:
    # Update pre-commit hook revisions in the checks config via prek
    just run -- prek auto-update --config .pre-commit-config-check.yaml
    # Update pre-commit hook revisions in the formatting config via prek
    just run -- prek auto-update --config .pre-commit-config-format.yaml

# Upgrade all dependencies using uv (uv don't support pyproject.toml update yet). <Don’t use! For maintainers only!>
[group('uv')]
upgrade-uv-dependencies:
    uv sync -U {{ UV_CLI_FLAGS }}

# Upgrade vale packages. <Don’t use! For maintainers only!>
[group('uv')]
upgrade-vale-packages:
    just run -- vale sync

# https://github.com/eclipse-csi/octopin
# Pins GitHub Action versions to use the SHA-1 hash instead of tag to improve security as Git tags are not immutable.
[group('uv')]
pin-github-action-versions:
    git ls-files -z -- '.github/workflows/*.y*ml' | xargs -0 uvx octopin pin --inplace

# Sync all dependencies using uv, without updating the uv.lock file.
[group('uv')]
sync:
    uv sync --frozen {{ UV_CLI_FLAGS }}

# Sync all dependencies using uv, and updating the uv.lock file. <Don’t use! For maintainers only!>
[group('uv')]
sync-lock *ARGS:
    uv sync {{ UV_CLI_FLAGS }} {{ ARGS }}

# Run ipython using uv.
[group('uv')]
ipython:
    just run -- ipython

# endregion Just CLI helpers (meta)
# region ----> QA <----

# Format - Fix formatting and lint violations - Write formatted files back!
[group('qa')]
format *ARGS:
    # Run pre-commit hooks using prek a better `pre-commit`, re-engineered in Rust!
    just run -- prek validate-config .pre-commit-config-format.yaml .pre-commit-config-check.yaml
    just run -- prek run {{ PREK_RUN_ARG }} --config .pre-commit-config-format.yaml {{ ARGS }}

# [Stop running hooks after the first failure]
[group('qa')]
@format-fail-fast: && (format "--fail-fast")

# [Do not run the hooks, but print the hooks that would have been run]
[group('qa')]
@format-dry-runw: && (format "--dry-run")

# [print diagnostics for prek, with hook id and duration]
[group('qa')]
@format-verbose: && (format "--verbose")

# ruff-format - Fix formatting and lint violations - Write formatted files back!
[group('qa')]
ruff-format OUTPUT_FORMAT="full" UNSAFE="":
    # Format Python files using Ruff's formatter (writes changes to disk).
    just run -- ruff format .
    # Check for lint violations, apply fixes to resolve lint violations(only for fixable rules).
    just run -- ruff check --fix --output-format={{OUTPUT_FORMAT}} {{UNSAFE}} .

# [including *unsafe* fixes, NOTE: --unsafe-fixes may change code intent (be careful)]
[group('qa')]
ruff-format-unsafe: && (ruff-format "concise" "--unsafe-fixes")

# [print diagnostics concisely, one per line]
[group('qa')]
@ruff-format-concise: && (ruff-format "concise")

# [group messages by file]
[group('qa')]
@ruff-format-grouped: && (ruff-format "grouped")

# Lint - Check for formatting and lint violations - Avoid writing any formatted files back!
[group('qa')]
lint *ARGS:
    # Run pre-commit hooks using prek a better `pre-commit`, re-engineered in Rust!
    just run -- prek validate-config .pre-commit-config-format.yaml .pre-commit-config-check.yaml
    just run -- prek run {{ PREK_RUN_ARG }} --config .pre-commit-config-check.yaml {{ ARGS }}

# [Stop running hooks after the first failure]
[group('qa')]
@lint-fail-fast: && (lint "--fail-fast")

# [Do not run the hooks, but print the hooks that would have been run]
[group('qa')]
@lint-dry-run: && (lint "--dry-run")

# [print diagnostics for prek, with hook id and duration]
[group('qa')]
@lint-verbose: && (lint "--verbose")

# ruff-check - Check for formatting and lint violations - Avoid writing any formatted files back!
[group('qa')]
ruff-check OUTPUT_FORMAT="full":
    # Check for formatting violations using Ruff
    just run -- ruff format --check --output-format={{OUTPUT_FORMAT}} .
    # Check for lint violations using Ruff
    just run -- ruff check --output-format={{OUTPUT_FORMAT}} .

# Check for lint violations for all rules!
[group('qa')]
ruff-check-all TARGET=".":
    just run -- ruff check --output-format=concise --select ALL --ignore CPY001,TC003,COM812,TD,D101,PLR0904,ARG004,FBT001,FBT002,SLF001 "{{TARGET}}"

# [print diagnostics concisely, one per line]
[group('qa')]
@ruff-check-concise: && (ruff-check "concise")

# [group messages by file]
[group('qa')]
@ruff-check-grouped: && (ruff-check "grouped")

# Type check the project with Ty
[group('qa')]
type-check TARGET=".":
    just run -- ty check "{{TARGET}}"

# Type check the project with Ty - Print diagnostics concisely, one per line
[group('qa')]
type-check-concise TARGET=".":
    just run -- ty check --output-format=concise "{{TARGET}}"

# Annotate types using pyrefly infer
[group('qa')]
type-annotate TARGET="src":
    just run -- pyrefly infer "{{ TARGET }}"

# Run all the formatting, linting, and type checking, for local development.
[group('qa')]
qa: format type-check-concise

# Run all the formatting, linting, type checking and tests for local development.
[group('qa')]
[group('test')]
qa-plus: qa test

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

# Run all the tests, for CI.
[private]
[group('test')]
test-ci:
    just uv-run --no-dev --group test -- pytest

# Run tests with lowest compatible versions for direct dependencies and highest compatible versions for indirect ones.
[group('test')]
test-lowest-direct-resolution:
    just run-isolated --no-dev --group test --resolution=lowest-direct -- pytest

# Run all the tests on a specified Python version
[group('test')]
test-on PY_VERSION:
    just run-isolated --python={{ PY_VERSION }} -- pytest

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

# Serve docs locally.
[group('docs')]
doc-serve:
    just run -- mkdocs serve -a localhost:3000

# Serve docs locally and open them in a new tab.
[group('docs')]
doc-serve-open:
    just run -- mkdocs serve --open -a localhost:3000

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
