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

If you are writing docs, install those dependencies

```sh
uv sync --extra docs
```

Add features, fix bugs, document!

Run the tests:

```bash
make test
```

Experiment with the CLI by creating an `input` directory with some templates or Markdown files, and run the `air` command:

```bash
air
```

The generated site will be in the `public` directory.

Make your changes, write tests, and submit a pull request.

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

Build locally:

```bash
make build
```

Publish the package to PyPI:

```bash
uv publish -t $UV_PUBLISH_TOKEN
```

Finally, create a new release on GitHub:

* Create a new release on GitHub by clicking "Create a new release"
* From the tag dropdown, choose the tag you just created
* Click "Generate release notes" to auto-populate the release notes
* Copy in whatever notes you have from the `CHANGELOG.md` file
* Revise the notes as needed
* Click "Publish release"
