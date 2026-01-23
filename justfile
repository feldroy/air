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

# Run a command or script using uv, perform an exact sync, removing extraneous packages.
[group('uv')]
@run-exact +ARGS:
    just run --exact {{ ARGS }}

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
    just sync-lock --upgrade

# Modify a specific dependency version using uv (uv don't support pyproject.toml update yet). <Don’t use! For maintainers only!>
[group('uv')]
modify-uv-dependency-version PACKAGE_NAME PACKAGE_VERSION:
    just sync-lock --upgrade-package {{ PACKAGE_NAME }}=={{ PACKAGE_VERSION }}

# Upgrade vale packages. <Don’t use! For maintainers only!>
[group('uv')]
upgrade-vale-packages:
    just run -- vale sync

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

# https://github.com/eclipse-csi/octopin
# Pins GitHub Action versions to use the SHA-1 hash instead of tag to improve security as Git tags are not immutable.
[group('uv')]
pin-github-action-versions:
    git ls-files -z -- '.github/workflows/*.y*ml' | xargs -0 uvx octopin@latest pin --inplace

# Validate Renovate config
renovate-config-validator:
    npx --yes --package renovate@latest -- renovate-config-validator --strict .github/renovate.json5

# --------------------------------------- prek ------------------------------------------------------------------------
BRANCH_NAME := `git branch --show-current`
DEFAULT_PREK_FILES := if BRANCH_NAME == "main" { "--all-files" } else { "--from-ref upstream/main" }
PREK_RUN_ARG := "--all-files" # TODO -> Delete this var.
# prek run --config .pre-commit-config-check.yaml --files $(git ls-files --modified) ✅
# prek run rumdl --config .pre-commit-config-check.yaml --files $(git ls-files --modified) ✅
# prek run --last-commit --config .pre-commit-config-check.yaml ✅
# prek run --from-ref upstream/main --config .pre-commit-config-check.yaml ✅
# git diff --quiet || { echo "Unstaged changes, stopping."; }




text505 B=BRANCH_NAME:
    echo {{ B }}

UNCOMMITTED_CHANGES_WARNING_MSG := (
    "You have uncommitted changes (staged and/or unstaged)." +
    "Please commit (or stash) them before running this recipe."
)

# Check for uncommitted changes (staged and/or unstaged)!
[group('git')]
@check-uncommitted-changes:
  git diff --quiet && git diff --cached --quiet || { echo "{{ UNCOMMITTED_CHANGES_WARNING_MSG }}"; exit 1; }

# [arg("HOOKS_OR_PROJECTS", long="hooks-or-projects", help="Include the specified hooks or projects")]

# Run pre-commit hooks using prek a better `pre-commit`, re-engineered in Rust!
[group('prek')]
[arg("CONFIG_FILE", long="config-file", help="Path to alternate config file")]
[arg("DRY_RUN", long="dry-run", value="--dry-run", help="Do not run the hooks, but print the hooks that would have been run")]
[arg("FAIL_FAST", long="fail-fast", value="--fail-fast", help="Stop running hooks after the first failure")]
[arg("VERBOSE", long="verbose", value="--verbose", help="Use verbose output")]
[arg("ALL_FILES", long="all-files", value="--all-files", help="Run on all files in the repo")]
[arg("PR_CHANGES", long="pr-changes", value="--from-ref upstream/main", help="Use verbose output")]
[arg("LAST_COMMIT", long="last-commit", value="--last-commit", help="Use verbose output")]
[arg("UNSTAGED_CHANGES", long="unstaged-changes", value="--files $(git ls-files --modified)", help="Use verbose output")]
[arg("FILES", long="files", help="Specific filenames to run hooks on")]
prek-run \
        CONFIG_FILE \
        DRY_RUN="" FAIL_FAST="" VERBOSE="" \
        ALL_FILES="" PR_CHANGES="" LAST_COMMIT="" UNSTAGED_CHANGES="" \
        FILES=DEFAULT_PREK_FILES *HOOKS_OR_PROJECTS:
    just check-uncommitted-changes
    just run -- prek validate-config .pre-commit-config-format.yaml .pre-commit-config-check.yaml
    just run -- prek run {{ HOOKS_OR_PROJECTS }} \
                         {{ DRY_RUN }} {{ FAIL_FAST }} {{ VERBOSE }} \
                         {{ ALL_FILES }} {{ PR_CHANGES }} {{ LAST_COMMIT }} {{ UNSTAGED_CHANGES }} \
                         --config {{ CONFIG_FILE }} \
                         {{ FILES }}

# 1. if BRANCH_NAME == "main" -> --all-files (Default)
# -. if BRANCH_NAME != "main":
#    2. --all-files
#    3. --last-commit
#    4. --from-ref upstream/main (PR changes) (Default)
#    5. --files $(git ls-files --modified) (Unstaged changes)
#    5. --from-ref "@{upstream}" (Local changes(not pushed yet))

#prek-run-old CONFIG_FILE MODE FILES=DEFAULT_PREK_FILES *HOOKS_OR_PROJECTS:
#   just run -- prek validate-config .pre-commit-config-format.yaml .pre-commit-config-check.yaml
# 1.
#   just run -- prek run {{ HOOKS }} {{ PROJECTS }} --config {{ CONFIG_FILE }} --all-files
# 2.
#    just run -- prek run {{ HOOKS }} {{ PROJECTS }} --config {{ CONFIG_FILE }} --last-commit
# 3.
#    just run -- prek run {{ HOOKS }} {{ PROJECTS }} --config {{ CONFIG_FILE }} --from-ref upstream/main
# 4.
#    just run -- prek run {{ HOOKS }} {{ PROJECTS }} --config {{ CONFIG_FILE }} --files $(git ls-files --modified)

# [Run on all files in the repo]
[group('prek')]
@prek-run-all-files:
    just prek-run --files --all-files
    just prek-run --files --last-commit
    just prek-run --files --all-files

# [Stop running hooks after the first failure]
[group('prek')]
@prek-run-fast: && (prek-run "--fail-fast")

# [Do not run the hooks, but print the hooks that would have been run]
[group('prek')]
@prek-run-dry-run: && (prek-run "--dry-run")

# [print diagnostics for prek, with hook id and duration]
[group('prek')]
@prek-run-verbose: && (prek-run "--verbose")

# Format - Fix formatting and lint violations - Write formatted files back!
[group('qa')]
format *HOOKS_OR_PROJECTS:
    just prek-run --config-file .pre-commit-config-format.yaml {{ HOOKS_OR_PROJECTS }}

# Lint - Check for formatting and lint violations - Avoid writing any formatted files back!
[group('qa')]
lint *HOOKS_OR_PROJECTS:
    just prek-run --config-file .pre-commit-config-check.yaml {{ HOOKS_OR_PROJECTS }}

# --------------------------------------- prek ------------------------------------------------------------------------


# endregion Just CLI helpers (meta)
# region ----> QA <----

# Format - Fix formatting and lint violations - Write formatted files back!
[group('qa')]
format-old *ARGS:
    # Run pre-commit hooks using prek a better `pre-commit`, re-engineered in Rust!
    just run -- prek validate-config .pre-commit-config-format.yaml .pre-commit-config-check.yaml
    just run -- prek run {{ PREK_RUN_ARG }} --config .pre-commit-config-format.yaml {{ ARGS }}

# [Stop running hooks after the first failure]
[group('qa')]
@format-fail-fast: && (format "--fail-fast")

# [Do not run the hooks, but print the hooks that would have been run]
[group('qa')]
@format-dry-run: && (format "--dry-run")

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
lint-old *ARGS:
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
    just run-exact -- pytest

# Run all the tests, for CI.
[private]
[group('test')]
test-ci:
    just uv-run --exact --no-dev --group test -- pytest

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
