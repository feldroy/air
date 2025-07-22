# Run all the formatting, linting, and testing commands
qa:
    ruff format .
    ruff check . --fix
    ruff check --select I --fix .
    ty check .
    pytest .

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.10 --extra dev pytest
    uv run --python=3.11 --extra dev pytest
    uv run --python=3.12 --extra dev pytest
    uv run --python=3.13 --extra dev pytest

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --extra dev pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.13 --with pytest --with httpx pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}

# Run coverage, and build to HTML
coverage:
    coverage run -m pytest .
    coverage report -m
    coverage html

# Build the project, useful for checking that packaging is correct
build:
    rm -rf build
    rm -rf dist
    uv build

VERSION := `python -c "import air; print(air.__version__)"`

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
    mkdocs gh-deploy --force
