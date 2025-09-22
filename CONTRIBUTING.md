# Contributing to Air

Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

#### 1. Create the fork on GitHub, clone it locally, and wire remotes correctly.

###### Autoconfigure the remotes(origin[your fork = your_github_username/air], upstream[original repo = feldroy/air]).

```bash
gh repo fork feldroy/air --clone --remote
```

#### 2. Move into the new project directory.

```bash
cd air
```

#### 3. Fetch the latest changes from upstream.

```bash
git fetch upstream
```

#### 4. Create and switch to a new feature branch starting from upstream/main.

```bash
git switch -c your-new-branch-name upstream/main
```

#### 5. Update the project's environment(ensures that all project dependencies are installed and up-to-date with the lockfile).

```bash
uv sync --frozen --extra all
```

#### 6. Configure your IDE with the uv environment:

###### 1. VS Code (macOS, Linux, Windows):

> 1. Open the project folder (air) in VS Code.
> 2. Open the Command Palette (Cmd+Shift+P on macOS, Ctrl+Shift+P on Windows/Linux) → “Python: Select Interpreter”.
> 3. Choose “Enter interpreter path…”, paste the path to `.venv/bin/python`, and press Enter.
> 4. If .venv appears, select it. If not, choose Enter interpreter path… and use:
>     - macOS/Linux: ./.venv/bin/python
>     - Windows: .\.venv\Scripts\python.exe

###### 2. PyCharm (macOS, Linux, Windows):

> 1. Open the project folder (air) in PyCharm → Settings → Python → Interpreter → "Add Interpreter"
>   → "Add Local Interpreter" → "select existing" → "select existing" → "select existing":
>    - "Type": `uv`.
>    - "Path to uv": bash```which uv```
>    - "uv env use": `<project>/air/.venv/bin/python`.
> 2. Click OK/Apply. More details: https://www.jetbrains.com/help/pycharm/uv.html

#### 7. Make your code changes and write/adjust tests to cover them (keep changes focused and small).

#### 8. Format the code and auto-fix simple issues(lint) with Ruff and Type check the project with Ty and pyrefly.

```bash
just qa
```

Make sure `just qa` does not produce any errors before you open a PR!

#### 9. Run the full pytest test suite

```bash
just test
```

Make sure `just test` does not produce any errors before you open a PR!

#### 10. Make a single commit that includes your tracked file changes with a clear message.

```bash
git commit -am "feat: brief, clear message"
```

#### 11. Push your branch to your fork and set the remote tracking.

```bash
git push -u origin your-new-branch-name
```

#### 12. Open a Pull Request back to feldroy/air with a prefilled title and body (edit as needed).

```bash
gh pr create --fill --repo feldroy/air
```

---

## Types of Contributions we're looking for

We are actively looking for contributions in the following areas:

* **Bug fixes:** If you find a bug, please feel free to submit a pull request with a fix.
* **Refactoring:** We welcome improvements to the existing codebase for clarity, performance, and maintainability.
* **Documentation:** Enhancements to our documentation, including docstrings, are always appreciated.
* **Features:** Any FEAT (feature) ticket marked with `Status: Approved`

> [!IMPORTANT]
> If you have an idea for a **new** feature, discuss it with us by opening an issue before writing any code. We want to
> keep Air light and breezy instead of adding too much to this package.

### Documentation: Docstrings and API Reference

The API reference is generated from docstrings in this code, and the docs are built by
the [github.com/feldroy/airdocs](https://github.com/feldroy/airdocs) project. All public functions, classes, and methods
require complete docstrings. This will help us maintain a high-quality documentation site. Rules for writing docstrings:

- Every function, class, and method should have a docstring
- Docstrings should be clear, concise, and informative
- Docstrings are written in Markdown format
- HTML tags are not allowed in docstrings unless surrounded by backticks (e.g., `<tag>` should be written as
  `` `<tag>` ``) or inside code blocks (e.g., ```` ```html <tag> ``` ````)
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all
  public functions, classes, and methods.
    - Use the `Args:` and `Return:` (or `Yields:` for generators) directives to document parameters and return values
    - Use the `Example:` directive to document how to use the function, class, or method being documented.

## Plugins vs. Core Features

We do not have a plugin system yet, but when we do:

Try to implement features as plugins rather than adding them to the core codebase. This will keep the core codebase
small and focused.

## Troubleshooting

If you run into issues, try the following:

* Delete `.venv/` and run `uv venv` again to recreate the virtualenv.
* Make sure you are not accidentally activating another virtualenv in your shell startup files.
* If code changes do not seem to apply, run via `uv run <command>` (which auto-syncs), or re-run `uv sync`.
* Upgrade uv if needed: `uv self update`.
* Still stuck? File a GitHub issue with details.
