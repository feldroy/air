# Contributing to the Air Web Framework

Welcome!
We're glad you're here.

## Prerequisites

1. [uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) (package manager)
2. [just](https://just.systems/man/en/packages.html) (command runner)
3. [gh](https://github.com/cli/cli#installation) (GitHub CLI)

## Getting started

```bash
# Fork, clone, and set up remotes in one step
gh repo fork feldroy/air --clone --remote
cd air

# Fetch latest and create your branch
git fetch upstream
git switch -c your-branch-name upstream/main

# Install dependencies
just sync
```

### IDE setup

**VS Code:** Command Palette → "Python: Select Interpreter" → enter `.venv/bin/python`

**PyCharm:** Settings → Python Interpreter → Add Interpreter → type `uv`, point to `.venv/bin/python`. [Details](https://www.jetbrains.com/help/pycharm/uv.html)

## Development workflow

Make your changes, then:

```bash
just qa      # format check + lint + type check (must pass before PR)
just test    # run the test suite (must pass before PR)
just fix     # auto-fix formatting and lint issues
```

Run `just` by itself to see all available recipes.

## Submitting your PR

```bash
git commit -am "<type>(<scope>): <description>"
git push -u origin your-branch-name
gh pr create --fill --repo feldroy/air
```

For commit message format, see the [Conventional Commits Cheatsheet](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13).

> [!IMPORTANT]
> Fill out the **Pull Request Template** completely. It helps maintainers review your contribution quickly.

## What we're looking for

- **Bug fixes:** Found a bug? Submit a PR with a fix.
- **Refactoring:** Improvements for clarity, performance, and maintainability.
- **Documentation:** Better docstrings and docs are always appreciated.
- **Features:** Any feature ticket marked with `Status: Approved`.

> [!IMPORTANT]
> Have an idea for a **new** feature? Open an issue to discuss it before writing code. We want to keep Air light and breezy.

### Feature categories

| Category                       | Label                           |
| ------------------------------ | ------------------------------- |
| Core Air Feature               | Feature: Core                   |
| Optional Air Feature           | Feature: Optional               |
| Third-Party Integrated Feature | Feature: Third-Party Integrated |
| Out-of-Scope Feature           | Feature: Out-of-Scope           |

**Core:** In the main repo, on by default. Fully documented and tested. Examples: Air Tags, FastAPI integration controls.

**Optional:** In the repo but off by default, installed via extras. Opt-in to keep the core small. Examples: authentication, CSRF validation.

**Third-Party Integrated:** Not implemented by Air. We provide guides and examples for integrating external libraries. Example: SQL integration.

**Out-of-Scope:** Not implemented, documented, or supported. Redirected to community solutions.

### Docstrings and API reference

The API reference is generated from docstrings in this repo and built with [MkDocs](https://www.mkdocs.org/) (see `mkdocs.yaml` and `docs/`). Rules:

- Every public function, class, and method needs a docstring
- Every new public callable **must include at least one working example**
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) in Markdown format
- Use `Args:`, `Return:` (or `Yields:`), and `Example:` directives
- HTML tags in docstrings must be in backticks (`` `<tag>` ``) or code blocks

## Troubleshooting

- Delete `.venv/` and run `uv venv` to recreate the virtualenv
- Make sure you're not activating another virtualenv in your shell startup files
- If code changes don't apply, use `uv run <command>` (auto-syncs) or re-run `uv sync`
- Upgrade uv: `uv self update`
- Still stuck? File a GitHub issue with details
