# Maintainer's Guide

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

## Categorizing Features

In the `Features: Categories` section of CONTRIBUTING.md there are four categories, each should be assigned to feature issues and pull requests.

## Updating Dependencies

```sh
just upgrade-dependencies
just type-check-concise
```

Fix any type errors that arise, then run the tests and qa to ensure nothing is broken.

```sh
just qa-plus
```

Finally, commit the changes:

```sh
git commit -am "Upgrade dependencies"
```
