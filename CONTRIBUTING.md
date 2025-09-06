# Contributing to Air

Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

Fork and clone this repository, and install the dependencies:

```bash
git clone https://github.com/feldroy/air.git
cd air
uv sync --all-extras --no-extra standard
```

Now you're ready to run Air from your local clone of your fork. Play with it, fix bugs, document, have fun!

## How Air installs in development (uv + build backend)

**Short version:** for a library, installing the library itself into the virtual environment (not just its dependencies) is how modern Python packaging works. Many features only “exist” after install because they are defined by packaging standards, not by just having files on disk.

### Official Python basis (why install matters)
- **PEP 517/518 build systems.** Projects declare a build backend in `pyproject.toml`. Front-ends (pip, uv, etc.) build and install through that backend, creating an installed distribution (aka: installable package) with metadata(version, entry points, requirements).
- **Editable installs (PEP 660).** In development we install editable (meaning: linked to your working tree), so code changes take effect without reinstalling.
- **Entry points and console scripts.** CLI commands and plugin hooks are created at install time from entry points (for example, `project.scripts`). Without install, those commands and hooks do not exist.
- **Distribution metadata.** Tools read version and entry points via `importlib.metadata` from the installed `.dist-info`. If not installed, there is nothing to read.
- **`src/` layout.** With `src/`, tests and tools should import the installed package (editable), not in-tree files. This matches how end users import from PyPI.

### What uv does here (how the tooling helps you)
- **Package vs “virtual” project.** Air is configured as a package, so `uv sync` and `uv run` install Air itself (editable) into the venv, not only its dependencies.
- **Auto-sync.** `uv run` checks the lockfile and environment before every run and keeps them up to date, so commands run against the installed distribution.
- **Editable by default.** uv installs your project editable unless you pass `--no-editable`.
- **Backend declared.** We declare `uv_build` as the build backend. This is the preferred path; it is fast and strict (meaning: validates structure early).

### Day-to-day commands
- Create or update your env and install Air (editable) plus default groups:
  `uv sync --all-extras --no-extra standard`
- Run tests (auto-syncs first if needed):
  `uv run pytest -q`
- Run any tool in the venv (auto-syncs):
  `uv run <command>`

If your Python is older than 3.13, don't worry! uv will automatically install Python 3.13 just for this project, the library does work on Python 3.10->3.13, but dev tools (group `dev`) are pinned to Python 3.13+ to keep the toolchain modern.

---

## Types of Contributions

We are actively looking for contributions in the following areas:

* **Bug fixes:** If you find a bug, please feel free to submit a pull request with a fix.
* **Refactoring:** We welcome improvements to the existing codebase for clarity, performance, and maintainability.
* **Documentation:** Enhancements to our documentation, including docstrings, are always appreciated.

> [!IMPORTANT]
> If you have an idea for a new feature, discuss it with us by opening an issue before writing any code. Do understand that we are working to remove features from core, and for new features you will almost always create your own package that extends or uses Air instead of adding to this package. This is by design, as our vision is for the Air package ecosystem to be as much a "core" part of Air as the code in this minimalist base package.

## Documentation: Docstrings and API Reference

The API reference is generated from docstrings in this code, and the docs are built by the [github.com/feldroy/airdocs](https://github.com/feldroy/airdocs) project. All public functions, classes, and methods require complete docstrings. This will help us maintain a high-quality documentation site. Rules for writing docstrings:

- Every function, class, and method should have a docstring
- Docstrings should be clear, concise, and informative
- Docstrings are written in Markdown format
- HTML tags are not allowed in docstrings unless surrounded by backticks (e.g., `<tag>` should be written as `` `<tag>` ``) or inside code blocks (e.g., ```` ```html <tag> ``` ````)
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all public functions, classes, and methods.
  - Use the `Args:` and `Return:` (or `Yields:` for generators) directives to document parameters and return values
  - Use the `Example:` directive to document how to use the function, class, or method being documented.


## Documentation: Concepts, Tutorials, and Guides

These are managed in the <a href="https://github.com/feldroy/airdocs" target="_blank">github.com/feldroy/airdocs</a> repository which is hosted at [airdocs.fastapicloud.dev/](https://airdocs.fastapicloud.dev/). If you want to contribute to the documentation, please fork that repository and submit a pull request there.


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
