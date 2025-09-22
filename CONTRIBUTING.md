# Contributing to Air

Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

Fork and clone this repository, and install the dependencies:

```bash
git clone https://github.com/feldroy/air.git
cd air
uv venv
uv sync --extra all
```

Now you're ready to make changes and test Air from your local clone of your fork.

## Tests

Run the tests:

```bash
just test
```

## Linting and Formatting

To lint and format the code to pass the linters:

```bash
just qa
```

As needed, make your changes, write tests, and submit a pull request.

---

## Types of Contributions we're looking for

We are actively looking for contributions in the following areas:

* **Bug fixes:** If you find a bug, please feel free to submit a pull request with a fix.
* **Refactoring:** We welcome improvements to the existing codebase for clarity, performance, and maintainability.
* **Documentation:** Enhancements to our documentation, including docstrings, are always appreciated.
* **Features:** Any FEAT (feature) ticket marked with `Status: Approved`

> [!IMPORTANT]
> If you have an idea for a **new** feature, discuss it with us by opening an issue before writing any code. We want to keep Air light and breezy instead of adding too much to this package.

### Documentation: Docstrings and API Reference

The API reference is generated from docstrings in this code, and the docs are built by the [github.com/feldroy/airdocs](https://github.com/feldroy/airdocs) project. All public functions, classes, and methods require complete docstrings. This will help us maintain a high-quality documentation site. Rules for writing docstrings:

- Every function, class, and method should have a docstring
- Docstrings should be clear, concise, and informative
- Docstrings are written in Markdown format
- HTML tags are not allowed in docstrings unless surrounded by backticks (e.g., `<tag>` should be written as `` `<tag>` ``) or inside code blocks (e.g., ```` ```html <tag> ``` ````)
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all public functions, classes, and methods.
  - Use the `Args:` and `Return:` (or `Yields:` for generators) directives to document parameters and return values
  - Use the `Example:` directive to document how to use the function, class, or method being documented.

## Plugins vs. Core Features

We do not have a plugin system yet, but when we do:

Try to implement features as plugins rather than adding them to the core codebase. This will keep the core codebase small and focused.

## Releasing a New Version

Change the version number in `pyproject.toml`.

Regenerate the lockfile:

```bash
uv lock
```

Commit the changes:

```sh
git commit -am "Release version x.y.z"
```

Tag the release and push to GitHub:

```sh
just tag
```

This will deploy the new package to PyPI. Once confirmed the new package has been found on GitHub.

Finally, create a new release on GitHub:

* Create a new release on GitHub by clicking "Create a new release"
* From the tag dropdown, choose the tag you just created
* Click "Generate release notes" to auto-populate the release notes
* Copy in whatever notes you have from the `CHANGELOG.md` file
* Revise the notes as needed
* Click "Publish release"

## Troubleshooting

If you run into issues, try the following:

* Delete `.venv/` and run `uv venv` again to recreate the virtualenv.
* Make sure you are not accidentally activating another virtualenv in your shell startup files.
* If code changes do not seem to apply, run via `uv run <command>` (which auto-syncs), or re-run `uv sync`.
* Upgrade uv if needed: `uv self update`.
* Still stuck? File a GitHub issue with details.
