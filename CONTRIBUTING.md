# Contributing to Air

Make sure you have [Rye](https://rye.astral.sh/) installed.

Clone the repository and install the dependencies:

```bash
git clone https://github.com/feldroy/air.git
cd air
python3 -m venv .venv
source .venv/bin/activate
rye sync
```

Run the tests:

```bash
rye test
```

Experiment by creating an `input` directory with some templates or Markdown files, and run the `air` command:

```bash
rye run air
```

The generated site will be in the `public` directory.

Make your changes, write tests, and submit a pull request.

Try to implement features as plugins rather than adding them to the core codebase. This will keep the core codebase small and focused.

## Releasing a New Version

```bash
rye version -b minor
git commit -am "Release version x.y.z"
rye build
```

Make sure the built package works:

```bash
python -m venv .venvtmp
source .venvtmp/bin/activate
pip install dist/your-package-0.3.0-py3-none-any.whl
(test your package here)
deactivate
rm -rf .venvtmp
```

Then publish the package to PyPI:

```bash
rye publish
```

Then publish the tag to GitHub:

```bash
git tag -a x.y.z -m "Version x.y.z"
git push --tags
```

Finally, create a new release on GitHub:

* Create a new release on GitHub by clicking "Create a new release"
* From the tag dropdown, choose the tag you just created
* Click "Generate release notes" to auto-populate the release notes
* Copy in whatever notes you have from the `CHANGELOG.md` file
* Revise the notes as needed
* Attach the distribution package: drag and drop the `.tar.gz` and `.whl` files from the `dist/` directory
* Click "Publish release"
