# Run all the formatting, linting, and testing commands
qa:
    uv run --python=3.13 --extra test ruff format .
    uv run --python=3.13 --extra test ruff check . --fix
    uv run --python=3.13 --extra test ruff check --select I --fix .
    uv run --python=3.13 --extra test ty check .
    uv run --python=3.13 --extra test pytest .

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.10 --extra test pytest
    uv run --python=3.11 --extra test pytest
    uv run --python=3.12 --extra test pytest
    uv run --python=3.13 --extra test pytest

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --extra test pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13  --extra test --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}

# Run coverage, and build to HTML
coverage:
    uv run --python=3.13 --extra test coverage run -m pytest .
    uv run --python=3.13 --extra test coverage report -m
    uv run --python=3.13 --extra test coverage html

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
    uv run --extra docs mkdocs serve -a localhost:3000

# Build and deploy docs
doc-build:
    uv run --extra docs mkdocs gh-deploy --force
