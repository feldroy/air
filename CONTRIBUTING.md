# Contributing to Air

Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

Fork and clone this repository, and install the dependencies:

```bash
git clone https://github.com/feldroy/air.git
cd air
uv venv
source .venv/bin/activate
uv sync --extra dev
```

Now you're ready to run Air from your local clone of your fork. Play with it, fix bugs, document, have fun!

## Types of Contributions

We are actively looking for contributions in the following areas:

*   **Bug fixes:** If you find a bug, please feel free to submit a pull request with a fix.
*   **Refactoring:** We welcome improvements to the existing codebase for clarity, performance, and maintainability.
*   **Documentation:** Enhancements to our documentation, including docstrings, are always appreciated.

While we are grateful for all interest, we are more hesitant to accept contributions that:

*   Add new features
*   Introduce new dependencies

This helps us keep the core of Air lean and focused. If you have an idea for a new feature, we recommend discussing it with us by opening an issue first. Do understand that for most new feature ideas we will suggest that you create your own package that extends or uses Air rather than adding a new feature to core Air itself.

## Docs

The docs are temporarily in this repo in docs/ and are built with [MkDocs](https://www.mkdocs.org/). Soon they will be in https://github.com/feldroy/airdocs

If you are contributing to the files in docs/ and want to build the MkDocs site, install those dependencies:

```sh
uv sync --extra docs
```

## Tests

Run the tests:

```bash
make test
```

## Linting and Formatting

To lint and format the code to pass the linters:

```bash
make clean
```

As needed, make your changes, write tests, and submit a pull request.

## Plugins vs. Core Features

We don't have a plugin system yet, but when we do:

Try to implement features as plugins rather than adding them to the core codebase. This will keep the core codebase small and focused.

## Releasing a New Version

Change the version number in `src/air/__init__.py` and `pyproject.toml`.

Regenerate the lockfile:

```bash
uv lock
```

Commit the changes:

```sh
git commit -am "Release version x.y.z"
```

Tag the release and push to github:

```sh
make tag
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
* Make sure you aren't accidentally activating another virtualenv in your shell startup files.
* File a GitHub issue with details if you're still stuck.
