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
PYTHON_VERSION := read(".python-version")

# -----------------------------------------------------------------------------
# RECIPES:
# -----------------------------------------------------------------------------

# List all the justfile recipes
list:
    @just --list

# region ----> QA <----

# Format code and auto-fix simple issues with Ruff
format:
    uv run -- ruff format .
    uv run -- ruff check --fix .

# Run Ruff checks without fixing to report issues
lint:
    # Avoid writing any formatted files back; instead, exit with a non-zero
    # status code if any files would have been modified, and zero otherwise,
    # and the difference between the current file and how the formatted file would look like.
    uv run -- ruff format --diff .
    uv run -- ruff check --no-fix .

# Type check the project with Ty
type-check:
    uv run -- ty check .

# Run all the formatting, linting, and type checking commands,
# for local development.
qa: format type-check

# endregion QA

# region ----> Test <----
# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.10 --isolated -- pytest
    uv run --python=3.11 --isolated -- pytest
    uv run --python=3.12 --isolated -- pytest
    uv run -- pytest

# Run Test Coverage
test-coverage:
    uv run -- pytest --cov -q

# Show the 10 slowest tests (timings)
test-durations:
    uv run -- pytest --durations=10 -vvv --no-header

# Build, store and open the HTML coverage report
coverage-html:
    uv run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=html
    open ./htmlcov/index.html

# Build and store the XML coverage report
coverage-xml:
    uv run -- pytest -vvv --cov --cov-fail-under=0 --cov-report=xml

# Build and store the MD coverage report - Automatically find diff lines that need test coverage.
coverage-md: coverage-xml
    diff-cover coverage.xml --format markdown:report.md
    open report.md

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run -- pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb MAXFAIL="10" *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run -- pytest --pdb --maxfail={{MAXFAIL}} {{ARGS}}

# TDD mode: stop at the first test failure
tdd: (pdb "1")
    @echo "TDD mode (stop at first failure)."
# endregion Test

# region ----> Rich <----
# Print a centered title with a magenta rule
@title TEXT="":
    rich "{{ TEXT }}" --rule --rule-style "red" --rule-char "=" --style "bold white on magenta"

# Print text inside a double-line panel with optional title and caption
@panel TEXT="" TITLE="" CAPTION="":
    rich "{{ TEXT }}" --title "{{ TITLE }}" --caption "{{ CAPTION }}" \
     --print --panel double --center --panel-style "magenta"

# Show Ruff analyze graph as JSON via rich (reads from stdin)
@ruff-graph: (title "Ruff - Graph")
    ruff analyze graph -q | rich - --force-terminal --json

# View a Markdown file with rich using the Dracula theme
@readmd FILE_NAME: (title FILE_NAME)
    rich "{{ FILE_NAME }}" --markdown --theme dracula --emoji --hyperlinks --pager

# Open README.md with rich
@readme: (readmd "README.md")

# Open CONTRIBUTING.md with rich
@contributing: (readmd "CONTRIBUTING.md")

# Open CHANGELOG.md with rich
@changelog: (readmd "CHANGELOG.md")

# View a Python file with syntax highlight, line numbers, and guides
@readpy FILE_PATH: (title FILE_PATH)
    rich "{{ FILE_PATH }}" --syntax --line-numbers --guides --theme dracula --pager

# endregion Rich

# Build the project, useful for checking that packaging is correct
build:
    rm -rf build
    rm -rf dist
    uv build

VERSION := `grep -m1 '^version' pyproject.toml | sed -E 's/version = "(.*)"/\1/'`

# Print the current version of the project
version:
    @echo "Current version is {{VERSION}}"

# Tag the current version in git and put to github
tag:
    echo "Tagging version v{{VERSION}}"
    git tag -a v{{VERSION}} -m "Creating version v{{VERSION}}"
    git push origin v{{VERSION}}

# Serve docs locally
doc:
    uv run -- mkdocs serve -a localhost:3000

# Build and deploy docs
doc-build:
    uv run -- mkdocs gh-deploy --force
