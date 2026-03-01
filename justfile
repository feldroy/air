# Air justfile - run `just` to see all recipes

# List available recipes
[private]
default:
    @just --list

# Install/update project dependencies
sync:
    uv sync

# Run the test suite
test *args:
    uv run pytest {{ args }}

# Run tests with coverage
test-cov:
    uv run coverage run -m pytest
    uv run coverage report

# Run linting, formatting check, and type checking
qa:
    uv run ruff format --check .
    uv run ruff check .
    uv run ty check .

# Auto-fix formatting and lint issues
fix:
    uv run ruff format .
    uv run ruff check --fix .

# Run a Python module (e.g., just run-example examples.tags_render)
run-example mod:
    uv run python -m {{ mod }}
