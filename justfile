# Run all the formatting, linting, and testing commands
qa:
    uv run --python=3.13 --isolated --group lint -- ruff format .
    uv run --python=3.13 --isolated --group lint -- ruff check --fix .
    uv run --python=3.13 --isolated --group lint --group test -- ty check .
    uv run --python=3.13 --isolated --group test -- pytest

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python=3.13 --isolated --group test -- pytest

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --isolated --group test -- pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --isolated --group test -- pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}

# Run coverage, and build to HTML
coverage:
    uv run --python=3.13 --isolated --group test -- coverage run -m pytest .
    uv run --python=3.13 --isolated --group test -- coverage report -m
    uv run --python=3.13 --isolated --group test -- coverage html

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
