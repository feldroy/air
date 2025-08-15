# Load .env automatically (for colors, etc.)
set dotenv-load := true
set dotenv-filename := ".env"

# List all the justfile recipes
list:
    just -l

# Run all the formatting, linting, and type checking commands
qa:
    uv run --python=3.13 --isolated --group lint -- ruff format .
    uv run --python=3.13 --isolated --group lint -- ruff check --fix .
    uv run --python=3.13 --isolated --group lint --group test -- ty check .

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python=3.13 --isolated --group test -- pytest

# Run Test Coverage
test-coverage:
    uv run --python=3.13 --isolated --group test -- pytest --cov -q

# Show the 10 slowest tests (timings)
test-durations:
    uv run --python=3.13 --isolated --group test -- pytest --durations=10 -vvv --no-header

# Build, store and open the HTML coverage report
coverage-html:
    uv run --python=3.13 --isolated --group test -- pytest -vvv --cov --cov-fail-under=0 --cov-report=html
    open ./htmlcov/index.html

# Build and store the XML coverage report
coverage-xml:
    uv run --python=3.13 --isolated --group test -- pytest -vvv --cov --cov-fail-under=0 --cov-report=xml

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --isolated --group test -- pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb MAXFAIL="10" *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --isolated --group test -- pytest --pdb --maxfail={{MAXFAIL}} {{ARGS}}

# TDD mode: stop at the first test failure
tdd: (pdb "1")
    @echo "TDD mode (stop at first failure)."

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
    uv run --python=3.13 --isolated --group docs -- mkdocs serve -a localhost:3000

# Build and deploy docs
doc-build:
    uv run --python=3.13 --isolated --group docs -- mkdocs gh-deploy --force
