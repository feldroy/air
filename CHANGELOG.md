### Latest Changes

# 0.45 - 2025-01-09

## What's Changed

### New Contributors

- @ohhaus made their first contribution in <https://github.com/feldroy/air/pull/919>

### Build items

- BUILD: Added `djhtml` hook to both `.pre-commit-config-check.yaml` and `.pre-commit-config-format.yaml` to automate formatting of HTML files and Jinja Templates! by @pygarap in <https://github.com/feldroy/air/pull/932>
- BUILD: Improvements to the project's code quality tooling and configuration management. by @pygarap in <https://github.com/feldroy/air/pull/957>
- BUILD: Add pre-commit-hooks: Some out-of-the-box hooks for pre-commit. by @pygarap in <https://github.com/feldroy/air/pull/935>
- BUILD: Added the `validate-pyproject` hook by @pygarap in <https://github.com/feldroy/air/pull/959>
- BUILD: Some hooks can run in parallel by priority(the new prek priority feature) & Added new hooks: check-jsonschema, yamlfmt & typos now run inside prek! by @pygarap in <https://github.com/feldroy/air/pull/960>
- BUILD: Added several new pre-commit hooks: creosote, complexipy, flake8-class-attributes-order, flake8-pydantic and pyroma! by @pygarap in <https://github.com/feldroy/air/pull/962>
- BUILD: Added new pre-commit hooks: rumdl - A modern, high-performance Markdown linter and formatter, built for speed in Rust & editorconfig-checker - A tool to verify that your files are in harmony with your .editorconfig by @pygarap in <https://github.com/feldroy/air/pull/966>
- BUILD: hotfix: now renovate will upgrade the just-install action correctly! by @pygarap in <https://github.com/feldroy/air/pull/970>

###  Chores

- CHORE: enable Ruff rule A (builtins shadowing) by @ohhaus in <https://github.com/feldroy/air/pull/919>
- CHORE: Remove ruff lint per file ignores by @msaizar in <https://github.com/feldroy/air/pull/930>
- CHORE: Remove air_tag_source_samples.py from ruff lint per-file-ignore by @msaizar in <https://github.com/feldroy/air/pull/954>
- CHORE: chore(deps): update endbug/latest-tag digest to 52ce15b by @renovate[bot] in <https://github.com/feldroy/air/pull/968>
- CHORE: chore(deps): update actions/checkout action to v6.0.1 by @renovate[bot] in <https://github.com/feldroy/air/pull/971>
- CHORE: chore(deps): update astral-sh/setup-uv action to v7.2.0 - autoclosed by @renovate[bot] in <https://github.com/feldroy/air/pull/972>
- CHORE: chore-ruff-rule: tc-sub-issue task of #642 completed by @sankarebarri in <https://github.com/feldroy/air/pull/973>
- CHORE: chore(deps): update pre-commit hook tombi-toml/tombi-pre-commit to v0.7.16 by @renovate[bot] in <https://github.com/feldroy/air/pull/974>
- CHORE: chore(deps): update pre-commit hook rvben/rumdl-pre-commit to v0.0.212 by @renovate[bot] in <https://github.com/feldroy/air/pull/975>

### Doc changes

- DOCS: Make location of docs consistent by @pydanny in <https://github.com/feldroy/air/pull/963>
- DOCS: Instructions for serving air uses the air CLI now by @pydanny in <https://github.com/feldroy/air/pull/958>
- DOCS: Add a few more tools to the Air site by @pydanny in <https://github.com/feldroy/air/pull/980>

### New features

- FEAT: Air CLI polish for clarity and joy by @audreyfeldroy in <https://github.com/feldroy/air/pull/929>
- FEAT: Convert routing.AirRouter to composition by @pydanny in <https://github.com/feldroy/air/pull/964>
- FEAT: Remove extraneous HTTP method args from AirRouter by @pydanny in <https://github.com/feldroy/air/pull/976>

### Bug fixes

- FIX: `id_` inconsistently used to represent HTML attribute of `id` by @msaizar in <https://github.com/feldroy/air/pull/926>
- FIX: Replace type argument with type_ in tags by @msaizar in <https://github.com/feldroy/air/pull/931>
- FIX: Rename max argument to max_ in tags to prevent builtin shadowing by @msaizar in <https://github.com/feldroy/air/pull/933>
- FIX: Rename min to min_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/936>
- FIX: Rename open to open_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/938>
- FIX: Rename reversed to reversed_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/947>
- FIX: Rename list to list_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/952>
- FIX: Rename dir to dir_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/953>

### Refactors

- REFACTOR: Rename nested helper functions inside tests by @msaizar in <https://github.com/feldroy/air/pull/934>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.44.0...v0.45.0>

## 0.44.1 - 2025-12-31

## What's Changed

- CHORE: Air CLI polish for clarity and joy by @audreyfeldroy in <https://github.com/feldroy/air/pull/929>
- CHORE: enable Ruff rule A (builtins shadowing) by @ohhaus in <https://github.com/feldroy/air/pull/919>
- CHORE: `id_` inconsistently used to represent HTML attribute of `id` by @msaizar in <https://github.com/feldroy/air/pull/926>
- CHORE: Replace type argument with type_ in tags by @msaizar in <https://github.com/feldroy/air/pull/931>
- CHORE: Remove ruff lint per file ignores by @msaizar in <https://github.com/feldroy/air/pull/930>
- CHORE: Added `djhtml` hook to both `.pre-commit-config-check.yaml` and `.pre-commit-config-format.yaml` to automate formatting of HTML files and Jinja Templates! by @pygarap in <https://github.com/feldroy/air/pull/932>
- CHORE: Rename max argument to max_ in tags to prevent builtin shadowing by @msaizar in <https://github.com/feldroy/air/pull/933>
- CHORE: Rename min to min_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/936>
- CHORE: Rename open to open_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/938>
- CHORE: Add pre-commit-hooks: Some out-of-the-box hooks for pre-commit. by @pygarap in <https://github.com/feldroy/air/pull/935>
- CHORE: Rename reversed to reversed_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/947>
- CHORE: Rename list to list_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/952>
- CHORE: Rename dir to dir_ to prevent builtin shadowing in tags by @msaizar in <https://github.com/feldroy/air/pull/953>
- CHORE: Remove air_tag_source_samples.py from ruff lint per-file-ignore by @msaizar in <https://github.com/feldroy/air/pull/954>

## New Contributors

- @ohhaus made their first contribution in <https://github.com/feldroy/air/pull/919>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.44.0...v0.44.1>

## 0.44.0 - 2025-12-27

## What's Changed

### Features

- FEAT: Add "air run" and "air version" CLI commands, make uvicorn a main dep by @audreyfeldroy in <https://github.com/feldroy/air/pull/920>
- FEAT: add `prek` a better `pre-commit`, re-engineered in Rust & blacken-docs, Run `black` on python code blocks in documentation files! by @pygarap in <https://github.com/feldroy/air/pull/918>
- FEAT: Introduced two new class methods to `BaseTag` in `src/air/tags/models/base.py` by @pygarap in <https://github.com/feldroy/air/pull/917:>
  - `from_html_file` for building an air-tag tree from a file
  - `from_html_file_to_source` for generating the instantiable source from a file

### Refactoring

- REFACTOR: Type Annotations Adjustments in the `air.tags.models.base.BaseTag` class! by @pygarap in <https://github.com/feldroy/air/pull/914>
- REFACTOR: rename `kwargs` to `custom_attributes` for improved clarity! by @pygarap in <https://github.com/feldroy/air/pull/915>
- REFACTOR: reorganize test files into `tags` subdirectory! by @pygarap in <https://github.com/feldroy/air/pull/916>
- REFACTOR: Convert air.Application from inheritance to composition by @pydanny in <https://github.com/feldroy/air/pull/906>

### Docs

- DOC: Added remaining docstrings to HTML air tags, finishing the awesome effort by @vanessapigwin! by @pydanny in <https://github.com/feldroy/air/pull/923>

### Bugfixes

- BUGFIX: Fix for docsite by @pydanny in <https://github.com/feldroy/air/pull/924>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.43.0...v0.44.0>

## 0.43.0 - 2025-12-22

## What's Changed

### New feature

- FEAT: Add support for query params in .url() function by @aybruhm in <https://github.com/feldroy/air/pull/899> (First time contribution!)
- FEAT: Add caching for inspect.signature and inspect.unwrap by @msaizar in <https://github.com/feldroy/air/pull/903>

## Bugfixes

- BUGFIX Handle more edge cases in from_html by @pygarap in <https://github.com/feldroy/air/pull/891>
- BUGFIX: Resolve PEP 563 string annotations in AirRoute by @msaizar in <https://github.com/feldroy/air/pull/893>

## Documentation changes

- DOCS: Update html to source tag by @pydanny in <https://github.com/feldroy/air/pull/883>
- DOCS: Remove airbook by @pydanny in <https://github.com/feldroy/air/pull/884>
- DOCS: Improve docs in preparation for the beta of Air by @audreyfeldroy in <https://github.com/feldroy/air/pull/890>
- DOCS: Improve page decorator docs by @audreyfeldroy in <https://github.com/feldroy/air/pull/894>
- DOCS: improve RedirectResponse for AI and editors by @audreyfeldroy in <https://github.com/feldroy/air/pull/897>

## Chores

- CHORE: Update FastAPI to 0.125.0 and modernize other libraries by @pydanny in <https://github.com/feldroy/air/pull/901>
- CHORE: Remove ANN201 and add return types by @msaizar in <https://github.com/feldroy/air/pull/880>
- CHORE: Remove ANN202 rule by @msaizar in <https://github.com/feldroy/air/pull/887>
- CHORE: Remove FBT rules by @msaizar in <https://github.com/feldroy/air/pull/888>
- CHORE: Uncomment PT rule in ruff by @msaizar in <https://github.com/feldroy/air/pull/889>
- CHORE: Exclude htmlcov directory from codespell checks by @audreyfeldroy in <https://github.com/feldroy/air/pull/898>
- CHORE: Uncomment DOC ruff rule by @msaizar in <https://github.com/feldroy/air/pull/900>
- CHORE: Renovate to update by version not hash by @pydanny in <https://github.com/feldroy/air/pull/905>

## New Contributors

- @aybruhm made their first contribution in <https://github.com/feldroy/air/pull/899>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.42.0...v0.43.0>

## 0.42.0 - 2025-12-08

## What's Changed

- feat: migrate AirConvert functionality to air-tags by introducing `BaseTag.from_html_to_source`! by @pygarap in <https://github.com/feldroy/air/pull/879>
- [FEAT] Add new AirConvert functionality powered by selectolax by @pygarap in <https://github.com/feldroy/air/pull/879>
- [FEAT] Improvements to AirTag typing and constants management by @pygarap in <https://github.com/feldroy/air/pull/879>
- [FEAT] New utility methods for BaseTag and children by @pygarap in <https://github.com/feldroy/air/pull/879>
  - `BaseTag.is_attribute_free_void_element`
  - `BaseTag.has_children`
  - `BaseTag.first_child`
  - `BaseTag.last_child`
  - `BaseTag.first_attribute`
  - `BaseTag.last_attribute`
  - `BaseTag.num_of_direct_children`
  - `BaseTag.num_of_attributes`
  - `BaseTag.tag_id`
- [CHORE] Remove FURB189 ruff rule by @msaizar in <https://github.com/feldroy/air/pull/872>
- [CHORE] Add 100% test coverage to missing_examples script by @msaizar in <https://github.com/feldroy/air/pull/873>
- [CHORE] Add baseline and check modes for scripts/missing_examples.py by @msaizar in <https://github.com/feldroy/air/pull/874>
- [CHORE] Remove ANN001 from pyproject.toml by @msaizar in <https://github.com/feldroy/air/pull/877>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.41.2...v0.42.0>

## 0.41.2 - 2025-11-28

## What's Changed

- DOCS: Add source example for AirModel.to_form by @msaizar in <https://github.com/feldroy/air/pull/864>
- CHORE: Remove dependabot by @pydanny in <https://github.com/feldroy/air/pull/867>
- chore(deps): update actions/checkout action to v6 by @renovate[bot] in <https://github.com/feldroy/air/pull/839>
- CHORE: Ruff rule: E501 by @msaizar in <https://github.com/feldroy/air/pull/866>
- CHORE: remove PGH004 ruff rule by @msaizar in <https://github.com/feldroy/air/pull/870>
- CHORE: remove W505 ruff rule by @msaizar in <https://github.com/feldroy/air/pull/871>
- CHORE: Upgrade `ty`,and address its errors! by @pygarap in <https://github.com/feldroy/air/pull/868>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/859>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.41.1...v0.41.2>

## 0.41.1 - 2025-11-24

*Note: This should have been a feature release thanks to XXXXXXXXXXXXXXXX. Rather than yank the release, as XXXXXXXXXXXXXXXX is additive and not a behaviorial change, we decided to leave as-is.*

## Features & Bugs

- BUG: Fix AirRouter default 404 handler by @msaizar in <https://github.com/feldroy/air/pull/858>
- FEAT: compact_render: minified HTML rendering to the Air tag system by @pygarap in <https://github.com/feldroy/air/pull/800>
- FEAT: async functions for copy_src_example_to_callable.py by @msaizar in <https://github.com/feldroy/air/pull/829>
- FEAT: Add tests for copy_src_example_to_callable script by @msaizar in <https://github.com/feldroy/air/pull/856>

## Documentation

- DOC: Added `CHANGELOG.md` to the `extend-exclude` list of typos by @pygarap in <https://github.com/feldroy/air/pull/803>
- DOC: Removes all code and documentation related to the optional authentication ("auth") feature by @pygarap in <https://github.com/feldroy/air/pull/801>
- DOC: SRC/EXAMPLE for AirForm class by @pydanny in <https://github.com/feldroy/air/pull/819>
- DOC: examples request htmx by @sankarebarri in <https://github.com/feldroy/air/pull/799>
- DOC: Adds a new section on agentic coding to `README.md` by @pygarap in <https://github.com/feldroy/air/pull/821>
- DOC: add src example for AirForm.validate by @msaizar in <https://github.com/feldroy/air/pull/820>
- DOC: src example for src/air/background.py by @msaizar in <https://github.com/feldroy/air/pull/805>
- DOC: Add chore PR checklist item by @pydanny in <https://github.com/feldroy/air/pull/823>
- DOC: src example forms airfield by @sankarebarri in <https://github.com/feldroy/air/pull/825>
- DOC: add src example for AirForm.from_request by @msaizar in <https://github.com/feldroy/air/pull/824>
- DOC: add src example for default_form_widget by @msaizar in <https://github.com/feldroy/air/pull/827>
- DOC: src_example(airform-widget): Add custom widget example for AirForm.widget by @sankarebarri in <https://github.com/feldroy/air/pull/826>
- DOC: : update `README.md` with PePy reference and `pyproject.toml` with `Repository` and `Sponsor` URLs by @pygarap in <https://github.com/feldroy/air/pull/828>
- DOC: Remove links to old docs by @pydanny in <https://github.com/feldroy/air/pull/831>
- DOC: improving test readability! by @pygarap in <https://github.com/feldroy/air/pull/836>
- DOC: : fix Air.get src example for copy_src_example_to_callable.py by @msaizar in <https://github.com/feldroy/air/pull/832>
- DOC: Revert back to mkdocs by @pydanny in <https://github.com/feldroy/air/pull/841>
- DOC: : fix Air.post src example for copy_src_example_to_callable.py by @msaizar in <https://github.com/feldroy/air/pull/846>
- DOC: : fix src example test files names by @msaizar in <https://github.com/feldroy/air/pull/847>
- DOC: Default lang for docs is python by @pydanny in <https://github.com/feldroy/air/pull/849>
- DOC: feat: add src example for mvpcss by @msaizar in <https://github.com/feldroy/air/pull/845>
- DOC: feat: support AirField edge case in copy_src_example_to_callable.py by @msaizar in <https://github.com/feldroy/air/pull/851>
- DOC: docs(examples): add example and tests for AirForm.render by @sankarebarri in <https://github.com/feldroy/air/pull/850>
- DOC: docs: fix Air.page src example by @msaizar in <https://github.com/feldroy/air/pull/852>
- DOC: Remove docstring prefix from src examples by @pydanny in <https://github.com/feldroy/air/pull/853>
- DOC: : add src example for picocss by @msaizar in <https://github.com/feldroy/air/pull/854>
- DOC: : rename AirForm source example test file by @msaizar in <https://github.com/feldroy/air/pull/855>

## Dependency Management

- ⬆(deps): bump click from 8.2.1 to 8.3.0 in the python-dependencies group across 1 directory by @dependabot[bot] in <https://github.com/feldroy/air/pull/807>
- DEPS: Update dependencies and describe the process by @pydanny in <https://github.com/feldroy/air/pull/810>
- BUILD: Removed `rust-just` from the `devtools` section in `pyproject.toml` by @pygarap in <https://github.com/feldroy/air/pull/783>
- chore(deps): update dependency click to v8.3.1 by @renovate[bot] in <https://github.com/feldroy/air/pull/822>
- chore(deps): update actions/checkout digest to 93cb6ef by @renovate[bot] in <https://github.com/feldroy/air/pull/834>
- ⬆(deps): bump astral-sh/setup-uv from 7.1.2 to 7.1.4 in the gha-minor-patch group by @dependabot[bot] in <https://github.com/feldroy/air/pull/843>
- REFACTOR: Remove ruff rule 'n' by @pydanny in <https://github.com/feldroy/air/pull/860>

## New Contributors

- @msaizar made their first contribution in <https://github.com/feldroy/air/pull/820>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.41.0...v0.41.1>

## 0.41.0 - 2025-11-11

## Breaking change

- Removed ext sqlmodel by @pydanny in <https://github.com/feldroy/air/pull/769>

## Other things that have changed

- Add support for HTML comments in the Air tag system! by @pygarap in <https://github.com/feldroy/air/pull/750>
- docs(contributing): add short welcoming intro by @sankarebarri in <https://github.com/feldroy/air/pull/756>
- Airblog test example by @Isaac-Flath in <https://github.com/feldroy/air/pull/752>
- docs(contributing): emphasize using the PR template when opening pull requests by @sankarebarri in <https://github.com/feldroy/air/pull/757>
- docs: add docstrings for base tags Table to Textarea by @vanessapigwin in <https://github.com/feldroy/air/pull/758>
- Some type annotation improvements by @pygarap in <https://github.com/feldroy/air/pull/759>
- Making `rich-cli` a separate tool and not part of the dev dependencies! by @pygarap in <https://github.com/feldroy/air/pull/760>
- Live reload for docs by @pydanny in <https://github.com/feldroy/air/pull/766>
- docs(examples): move src_examples to examples/src and update paths (#743) by @sankarebarri in <https://github.com/feldroy/air/pull/764>
- Add support for 'async_' key in HTML attributes by @Isaac-Flath in <https://github.com/feldroy/air/pull/772>
- Add deprecation working for ext.auth by @pydanny in <https://github.com/feldroy/air/pull/771>
- Added a link to "What makes documentation good?" to the documentation section in `CONTRIBUTING.md` by @pygarap in <https://github.com/feldroy/air/pull/782>
- Migrate from Material for MkDocs to Zensical! Stage 1! by @pygarap in <https://github.com/feldroy/air/pull/777>
- Fix broken pages deployment by @pydanny in <https://github.com/feldroy/air/pull/786>
- docs: add PyPI stats and star history sections to README by @pygarap in <https://github.com/feldroy/air/pull/788>
- Updates repository ownership and funding information to reflect current maintainers. by @pygarap in <https://github.com/feldroy/air/pull/773>
- docs: Small README fix by @pygarap in <https://github.com/feldroy/air/pull/790>
- Updates the `pyproject.toml` file to improve project metadata and discoverability by @pygarap in <https://github.com/feldroy/air/pull/774>
- add args to docstrings for T elements by @vanessapigwin in <https://github.com/feldroy/air/pull/791>
- When publishing libraries, it is recommended to separately run tests with --resolution lowest or --resolution lowest-direct in continuous integration to ensure compatibility with the declared lower bounds. by @pygarap in <https://github.com/feldroy/air/pull/795>
- refactor: simplify `pretty` implementation and Integrated `lxml` and `rich` as default dependencies for improved usability. by @pygarap in <https://github.com/feldroy/air/pull/784>
- Update air tag docs for all reserved Python words by @pydanny in <https://github.com/feldroy/air/pull/798>
- Refactor duplicated methods from applications.Air and router.AirRouter into one by @pydanny in <https://github.com/feldroy/air/pull/749>
- chore(deps): update astral-sh/setup-uv digest to 5a7eac6 by @renovate[bot] in <https://github.com/feldroy/air/pull/793>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.40.0...v0.41.0>

## 0.40.0 - 2025-11-03

## Contributions from new contributors

- feat: docs-only src_example for exceptionhandlers.py by @elliedel in <https://github.com/feldroy/air/pull/714>
- sample Dockerfile and README.md for containerization how-to by @hardwyrd in <https://github.com/feldroy/air/pull/722>
- sample deployment YAML and README for k8s deployment how-to by @hardwyrd in <https://github.com/feldroy/air/pull/726>
- docs(contributing): require working examples for all new callables (#241) by @sankarebarri in <https://github.com/feldroy/air/pull/740>

## What's Changed

- feat: Add HTML5 validation attributes from Pydantic constraints by @hamelsmu in <https://github.com/feldroy/air/pull/689>
- add missing uv init on the installation step of index.md by @KevsterAmp in <https://github.com/feldroy/air/pull/730>
- Proxy Request to AirRequest by @pydanny in <https://github.com/feldroy/air/pull/739>
- Air Book improvements chapters 1 through 4 by @pydanny in <https://github.com/feldroy/air/pull/735>
- Improvements to Air Book chapters 5+ by @pydanny in <https://github.com/feldroy/air/pull/738>
- DOC: import starlette.requests.Request on Jinja example by @KevsterAmp in <https://github.com/feldroy/air/pull/734>
- Deprecation of sqlmodel by @pydanny in <https://github.com/feldroy/air/pull/736>
- Enhance example script parsing and add SessionMiddleware example by @pydanny in <https://github.com/feldroy/air/pull/675>
- Add SessionMiddleware example test by @pydanny in <https://github.com/feldroy/air/pull/742>
- AirModel with .form() by @audreyfeldroy in <https://github.com/feldroy/air/pull/727>
- Add patch, put, and delete route decorators to Air by @pydanny in <https://github.com/feldroy/air/pull/747>

## New Contributors

- @elliedel made their first contribution in <https://github.com/feldroy/air/pull/714>
- @hardwyrd made their first contribution in <https://github.com/feldroy/air/pull/722>
- @sankarebarri made their first contribution in <https://github.com/feldroy/air/pull/740>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.39.0...v0.40.0>

## 0.39.0 - 2025-10-28

## What's changed by new contributors

- feat: add .url() method to route functions by @nedpals in <https://github.com/feldroy/air/pull/706>
- docs: removed one slash in the link preview, and added one slash in the link url (issue #613) by @kindadailybren in <https://github.com/feldroy/air/pull/671>
- docs: issue 618 - Change 'Reference for all the entire' to 'Reference for the entire' by @edchelstephens in <https://github.com/feldroy/air/pull/670>
- docs: fix inspirations grammatical error by @gabbyxiane in <https://github.com/feldroy/air/pull/672>
- docs: Correct example usage from 'app = air.App()' to 'app = air.Air()'. by @edchelstephens in <https://github.com/feldroy/air/pull/674>
- fix: remove self-closing slashes from void elements by @alasdiel in <https://github.com/feldroy/air/pull/673>
- docs: fix (line 11) word from engineer to databases by @oreocapybara in <https://github.com/feldroy/air/pull/677>
- fix: grammatical errors in jinja.md by @chalorejo in <https://github.com/feldroy/air/pull/680>
- docs: Update badges and improve index.md formatting by @zorexsalvo in <https://github.com/feldroy/air/pull/683>
- docs: change syntactal to syntactic from docs/about/inspirations.md by @dkeithdj in <https://github.com/feldroy/air/pull/682>
- Fix/docs/readme comment error by @gabbyxiane in <https://github.com/feldroy/air/pull/684>
- docs: fixed pluralization issue on the word routes by @alasdiel in <https://github.com/feldroy/air/pull/685>
- test: add tests for compute_page_path by @ouattararomuald in <https://github.com/feldroy/air/pull/663>
- docs: README comment typo by @ouattararomuald in <https://github.com/feldroy/air/pull/664>
- Update github oath demo removed the duplicateof databases = {} by @aaronjalapon in <https://github.com/feldroy/air/pull/676>
- replaced pico to picocss by @aaronjalapon in <https://github.com/feldroy/air/pull/691>
- Tests: missing_examples.py script tests for functions by @kindadailybren in <https://github.com/feldroy/air/pull/692>
- docs: fixed checkbox formatting on roadmap.md by @alasdiel in <https://github.com/feldroy/air/pull/693>
- docs: fixed code shadowing on air = air.Air() by @RMRizal-UP in <https://github.com/feldroy/air/pull/696>
- docs: fix missing closing > in Jinja example (#609) by @ogbinar in <https://github.com/feldroy/air/pull/695>
- chore: address inconsistent default response by @dkeithdj in <https://github.com/feldroy/air/pull/686>
- Fixed deprecated issues and passed all Air test by @joohhhnnnny in <https://github.com/feldroy/air/pull/698>
- DOC: add missing space before parenthesis on CONTRIBUTING.md by @KevsterAmp in <https://github.com/feldroy/air/pull/700>
- docs: clarify explanation for Variables in URLs by @RMRizal-UP in <https://github.com/feldroy/air/pull/703>
- refac(src_examples): add samples and tests for other htmx requests besides get request by @jlorion in <https://github.com/feldroy/air/pull/702>
- add create_sync_engine example by @KevsterAmp in <https://github.com/feldroy/air/pull/715>
- Sprint day updates by @trbyte in <https://github.com/feldroy/air/pull/713>
- Feat(benchmarks)/print memory scaling results by @alasdiel in <https://github.com/feldroy/air/pull/711>

## What's changed by existing contributors

- Addition of sponsor and contributor acknowledgments to the `README.md`. by @pygarap in <https://github.com/feldroy/air/pull/607>
- Add Community page by @Isaac-Flath in <https://github.com/feldroy/air/pull/632>
- Consolidate doc links by @pydanny in <https://github.com/feldroy/air/pull/656>
- Add Libraries to Community Page by @Isaac-Flath in <https://github.com/feldroy/air/pull/662>
- Add sprinter instructions by @audreyfeldroy in <https://github.com/feldroy/air/pull/665>
- src_example directory with example and script by @pydanny in <https://github.com/feldroy/air/pull/659>
- Explain how to contribute to src_examples/ by @audreyfeldroy in <https://github.com/feldroy/air/pull/694>
- chore(deps): update astral-sh/setup-uv digest to 8585678 by @renovate[bot] in <https://github.com/feldroy/air/pull/717>
- chore: enable PLC rules and update files that break it by @zorexsalvo in <https://github.com/feldroy/air/pull/705>

## New Contributors

- @kindadailybren made their first contribution in <https://github.com/feldroy/air/pull/671>
- @edchelstephens made their first contribution in <https://github.com/feldroy/air/pull/670>
- @gabbyxiane made their first contribution in <https://github.com/feldroy/air/pull/672>
- @alasdiel made their first contribution in <https://github.com/feldroy/air/pull/673>
- @oreocapybara made their first contribution in <https://github.com/feldroy/air/pull/677>
- @chalorejo made their first contribution in <https://github.com/feldroy/air/pull/680>
- @dkeithdj made their first contribution in <https://github.com/feldroy/air/pull/682>
- @ouattararomuald made their first contribution in <https://github.com/feldroy/air/pull/663>
- @aaronjalapon made their first contribution in <https://github.com/feldroy/air/pull/676>
- @RMRizal-UP made their first contribution in <https://github.com/feldroy/air/pull/696>
- @ogbinar made their first contribution in <https://github.com/feldroy/air/pull/695>
- @joohhhnnnny made their first contribution in <https://github.com/feldroy/air/pull/698>
- @KevsterAmp made their first contribution in <https://github.com/feldroy/air/pull/700>
- @jlorion made their first contribution in <https://github.com/feldroy/air/pull/702>
- @nedpals made their first contribution in <https://github.com/feldroy/air/pull/706>
- @trbyte made their first contribution in <https://github.com/feldroy/air/pull/713>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.38.1...v0.39.0>

## 0.38.1 - 2025-10-22

## What's Changed

- Fix CI badge by @pydanny in <https://github.com/feldroy/air/pull/604>
- chore(deps): update astral-sh/setup-uv digest to 2ddd2b9 by @renovate[bot] in <https://github.com/feldroy/air/pull/593>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/594>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.38.0...v0.38.1>

## 0.38.0 - 2025-10-22

## What's Changed

Showcase feature that boggles the mind:

- FEATURE: Render Air Tags Fast in the Browser! by @tallerasaf in <https://github.com/feldroy/air/pull/512>

New contributors!

- DOCS: Fix typo in learn Jinja docs (`jinja2` → `jinja`) by @davidbgk in <https://github.com/feldroy/air/pull/587>
- DOCS: Missing end of line in authentication cookbook example by @davidbgk in <https://github.com/feldroy/air/pull/588>
- DOCS Add navigation footer for next/previous page navigation by @hamelsmu in <https://github.com/feldroy/air/pull/601>

Awesome stuff from existing contributors

- BUG: Fix a bug where basedpyright and pyright as well as Zed editor could not parse our pyproject.toml file! by @tallerasaf in <https://github.com/feldroy/air/pull/578>
- BUG: Fix all errors from the newest ty version! by @tallerasaf in <https://github.com/feldroy/air/pull/590>
- DOCS: Quickstart jinja by @pydanny in <https://github.com/feldroy/air/pull/583>
- CHORE: Improve the PR template by @pydanny in <https://github.com/feldroy/air/pull/584>
- DOCS: Fix Discord link and update discussion guidelines by @pydanny in <https://github.com/feldroy/air/pull/589>
- DOCS: Add feature categories by @pydanny and @tallerasaf in <https://github.com/feldroy/air/pull/585>
- DOCS: Add segment on articles and videos by @pydanny in <https://github.com/feldroy/air/pull/595>
- CHORE: Update sponsors config by @pydanny in <https://github.com/feldroy/air/pull/596>
- CHORE: Update FastAPI dependency to >=0.119.1 by @pydanny in <https://github.com/feldroy/air/pull/600>
- CHORE: When publishing libraries, it is recommended to separately run tests with --resolution lowest or --resolution lowest-direct in continuous integration to ensure compatibility with the declared lower bounds. by @tallerasaf in <https://github.com/feldroy/air/pull/59>

## New Contributors

- @davidbgk made their first contribution in <https://github.com/feldroy/air/pull/587>
- @hamelsmu made their first contribution in <https://github.com/feldroy/air/pull/601>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.37.0...v0.38.0>

## 0.37.0 - 2025-10-16

## What's Changed

- BOOK: The Air Book by @audreyfeldroy in <https://github.com/feldroy/air/pull/504>
- BUG: Constrain renderers to only stringify items inheriting from BaseTag by @bluerosej and @pydanny in <https://github.com/feldroy/air/pull/561>
- DOCS: book example uses the wrong library #576 by @MrValdez in <https://github.com/feldroy/air/pull/577>
- docs(tags): add docstring Args for S to Small by @vanessapigwin in <https://github.com/feldroy/air/pull/558>
- Integrate spelling and grammar checkers (`codespell` and `typos`) for the entire project! by @tallerasaf in <https://github.com/feldroy/air/pull/548>
- Fix link to air tags by @pydanny in <https://github.com/feldroy/air/pull/567>
- docs: add Args for Source to Sup tags by @vanessapigwin in <https://github.com/feldroy/air/pull/568>
- chore(deps): update astral-sh/setup-uv digest to 3259c62 by @renovate[bot] in <https://github.com/feldroy/air/pull/562>
- Finish moving ext.sql to ext.sqlmodel by @pydanny in <https://github.com/feldroy/air/pull/560>
- Quickstart: SSE plus file in `/examples` by @pydanny in <https://github.com/feldroy/air/pull/572>
- Address doclink warnings by @pydanny in <https://github.com/feldroy/air/pull/573>
- Configure project for mkdocs-llmstxt by @pydanny in <https://github.com/feldroy/air/pull/574>

## New Contributors

- @bluerosej made their first contribution in <https://github.com/feldroy/air/pull/561>
- @MrValdez made their first contribution in <https://github.com/feldroy/air/pull/577>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.36.0...v0.37.0>

## 0.36.0 - 2025-10-10

## What's Changed

- Implement .htmx object on air.Request by @pydanny in <https://github.com/feldroy/air/pull/524>
- Drop Python 3.12 support! by @tallerasaf in <https://github.com/feldroy/air/pull/538>
- Add forms quickstart by @pydanny in <https://github.com/feldroy/air/pull/536> and <https://github.com/feldroy/air/pull/539>
- Restore llms.txt for LLM-friendly documentation by @intellectronica in <https://github.com/feldroy/air/pull/552>
- fixed broken cookbook docs link by @alaminopu in <https://github.com/feldroy/air/pull/553>
- Temporary just tdd fix for Python 3.14 by @tallerasaf in <https://github.com/feldroy/air/pull/555>
- Add comprehensive tests for default_form_widget by @kernelshard in <https://github.com/feldroy/air/pull/535>
- Remove redundant CI workflow and simplify coverage configuration by @tallerasaf in <https://github.com/feldroy/air/pull/542>
- Fix the request part of the docs by @pydanny in <https://github.com/feldroy/air/pull/557>
- chore(deps): update astral-sh/setup-uv action to v7 by @renovate[bot] in <https://github.com/feldroy/air/pull/541>
- chore(deps): update dependency uv_build to >=0.9.0,<0.10.0 by @renovate[bot] in <https://github.com/feldroy/air/pull/543>
- ⬆(deps): Bump the python-dependencies group across 1 directory with 5 updates by @dependabot[bot] in <https://github.com/feldroy/air/pull/556>

## New Contributors

- @kernelshard made their first contribution in <https://github.com/feldroy/air/pull/535>
- @intellectronica made their first contribution in <https://github.com/feldroy/air/pull/552>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.35.0...v0.36.0>

## 0.35.0 - 2025-10-06

## What's Changed

- FEAT: add option for app.page decorator to convert underscores to forward slashes by default by @alaminopu in <https://github.com/feldroy/air/pull/522>
- FEAT: Add support for Python 3.14! by @tallerasaf in <https://github.com/feldroy/air/pull/529>
- DOCS: : add usage and recipes for requests.Request by @zorexsalvo in <https://github.com/feldroy/air/pull/527>
- DOCS: Add mixed bread AI search on docs by @pydanny and @audreyfeldroy in <https://github.com/feldroy/air/pull/530>
- DOCS: Refine `ruff` configuration by @tallerasaf in <https://github.com/feldroy/air/pull/528>
- DOCS: Show use of include router for bigger apps by @pydanny in <https://github.com/feldroy/air/pull/531>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/534>
- chore(deps): update wechuli/allcheckspassed action to v2.1.0 by @renovate[bot] in <https://github.com/feldroy/air/pull/532>

## New Contributors

- @zorexsalvo made their first contribution in <https://github.com/feldroy/air/pull/527>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.34.0...v0.35.0>

## 0.34.0 - 2025-10-04

## What's Changed

- REFACTOR: Change name of air.ext.sql to air.ext.sqlmodel by @pydanny in <https://github.com/feldroy/air/pull/526>
- DOCS: Quickstart javascript and CSS files by @pydanny in <https://github.com/feldroy/air/pull/520>
- DOCS: Describes adding variables in different ways to URLs in Quickstart by @pydanny in <https://github.com/feldroy/air/pull/523>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/509>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.33.1...v0.34.0>

## 0.33.1 - 2025-09-30

## What's Changed

- BUGFIX: Provide option to set GH callback URI by @pydanny in <https://github.com/feldroy/air/pull/517>
- DOCS: Roadmap docs cleanup by @pydanny in <https://github.com/feldroy/air/pull/507>
- DOCS: Move alternatives to use admonitions by @pydanny in <https://github.com/feldroy/air/pull/508>
- DOCS: Add routing to quickstart by @pydanny in <https://github.com/feldroy/air/pull/514>
- DOCS: Add airblog example by @pydanny in <https://github.com/feldroy/air/pull/513>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.33.0...v0.33.1>

## 0.33.0 - 2025-09-26

## New Features

- Show type of form failure rather than just an error happened by @prodigisoftwares in <https://github.com/feldroy/air/pull/495>
- Constrain the exports from air.ext.sql by @pydanny in <https://github.com/feldroy/air/pull/496>
- Add dark theme support to docs by @EnriqueSoria in <https://github.com/feldroy/air/pull/499>
- Renderable Type for Tag children by @audreyfeldroy in <https://github.com/feldroy/air/pull/498>

## Bugfixes

- docs: update jinja templating example by @alaminopu in <https://github.com/feldroy/air/pull/497>

## Chores

- ⬆(deps): Bump the python-dependencies group across 1 directory with 5 updates by @dependabot[bot] in <https://github.com/feldroy/air/pull/494>
- Bring forward old version release instructions by @pydanny in <https://github.com/feldroy/air/pull/501>

## New Contributors

- @EnriqueSoria made their first contribution in <https://github.com/feldroy/air/pull/499>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.32.0...v0.33.0>

## 0.32.0 - 2025-09-24

## What's Changed

- FEAT: Add changelog link to pyproject.toml by @alaminopu in <https://github.com/feldroy/air/pull/480>
- FEAT: Make the default status_code of air.RedirectResponse be 303 by @alaminopu in <https://github.com/feldroy/air/pull/481>
- Merge cookbook into learn section by @pydanny in <https://github.com/feldroy/air/pull/483>
- DOCS: Enhance contribution guide with detailed setup instructions by @tallerasaf in <https://github.com/feldroy/air/pull/484>
- Add GitHubOAuthClientFactory to support easier authentication by @pydanny and @audreyfeldroy in <https://github.com/feldroy/air/pull/487>
- Improved learn docs for SQL by @pydanny in <https://github.com/feldroy/air/pull/488>
- Add script to look for missing examples in callables by @pydanny in <https://github.com/feldroy/air/pull/489>
- FEAT: pretty_render enhancements by @tallerasaf in <https://github.com/feldroy/air/pull/477>
- docs: add docstrings for P, Q and R tags by @vanessapigwin in <https://github.com/feldroy/air/pull/492>
- Various minor fixes to documentation by @pydanny in <https://github.com/feldroy/air/pull/493>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/482>
- chore(deps): update wechuli/allcheckspassed action to v2 by @renovate[bot] in <https://github.com/feldroy/air/pull/491>

## New Contributors

- @alaminopu made their first contribution in <https://github.com/feldroy/air/pull/480>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.31.0...v0.32.0>

## 0.31.0 - 2025-09-21

## What's Changed

- Add latest-changes GitHub Action workflow (Issue #163) by @prodigisoftwares in <https://github.com/feldroy/air/pull/437>
- Issue #60-Document-is_htmx_request - Add documentation and add a coup… by @prodigisoftwares in <https://github.com/feldroy/air/pull/458>
- Incremental doc improvements by @pydanny in <https://github.com/feldroy/air/pull/448>
- Documentation on Airtag cleanup by @pydanny in <https://github.com/feldroy/air/pull/450>
- chore(deps): update actions/checkout action to v5 by @renovate[bot] in <https://github.com/feldroy/air/pull/449>
- Added a new "all" group for combined optional dependencies in `pyproject.toml` by @tallerasaf in <https://github.com/feldroy/air/pull/451>
- Add missing doc pages by @pydanny in <https://github.com/feldroy/air/pull/452>
- Add requests to documentation by @pydanny in <https://github.com/feldroy/air/pull/455>
- Add PR checklist by @pydanny in <https://github.com/feldroy/air/pull/456>
- ⬆(deps): Bump rich from 12.6.0 to 14.1.0 in the python-dependencies group across 1 directory by @dependabot[bot] in <https://github.com/feldroy/air/pull/457>
- Small refactor extracted from a big PR by @tallerasaf in <https://github.com/feldroy/air/pull/459>
- Add type annotations to the entire codebase using pyrefly and ruff(What they could do, still not 100%) by @tallerasaf in <https://github.com/feldroy/air/pull/441>
- chore: update Codecov config and refine coverage exclusions by @tallerasaf in <https://github.com/feldroy/air/pull/469>
- Drop Python 3.10 and 3.11 by @tallerasaf in <https://github.com/feldroy/air/pull/470>
- Added get_object_or_404 to air.ext.sql. by @pydanny and @audreyfeldroy in <https://github.com/feldroy/air/pull/466>
- Move ty ignore rule to correct location in pyproject.toml by @pydanny in <https://github.com/feldroy/air/pull/471>
- Add docs issue template by @pydanny in <https://github.com/feldroy/air/pull/474>
- Change air.db.sql path to air.ext.sql in docs by @pydanny in <https://github.com/feldroy/air/pull/476>
- Add lifespan db func to air.ext.sql by @pydanny and @audreyfeldroy in <https://github.com/feldroy/air/pull/478>
- Make contributing.md more concise by @pydanny in <https://github.com/feldroy/air/pull/479>

## New Contributors

- @prodigisoftwares made their first contribution in <https://github.com/feldroy/air/pull/437>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.30.0...v0.31.0>

## 0.30.0 - 2025-09-17

## What's Changed

### New contributor submissions

- BUG: resolve type-check errors pyrefly in docs by adding path by @datnq26 in <https://github.com/feldroy/air/pull/415>
- DOCS: add two uv steps by @modasserbillah in <https://github.com/feldroy/air/pull/416>
- DOCS: Import Field from pydantic by @tamerz in <https://github.com/feldroy/air/pull/419>

###  Big changes

- FEAT: Improve tag rendering by @tallerasaf in <https://github.com/feldroy/air/pull/377>
- FEAT: Add GitHub OAuth router Factory by @pydanny in <https://github.com/feldroy/air/pull/443>
- FEAT: Add templating.Renderer ComponentLoader by @pydanny in <https://github.com/feldroy/air/pull/430>

### Everything else

- ⬆(deps): Bump pytest-asyncio from 1.1.0 to 1.2.0 in the python-dependencies group by @dependabot[bot] in <https://github.com/feldroy/air/pull/413>
- BUG: Move content of db to ext by @pydanny in <https://github.com/feldroy/air/pull/421>
- TOOL: Migrate airdocs to mkdocs by @pydanny in <https://github.com/feldroy/air/pull/422>
- TOOL: Add build command back by @pydanny in <https://github.com/feldroy/air/pull/424>
- DOCS: Fix rotating reasons not to use air by @pydanny in <https://github.com/feldroy/air/pull/425>
- DOCS: Fix doc index links by @pydanny in <https://github.com/feldroy/air/pull/426>
- DOCS: Fix errant doc links by @pydanny in <https://github.com/feldroy/air/pull/427>
- build(deps): lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/428>
- FEAT: Get test coverage back up to 95+% by @pydanny in <https://github.com/feldroy/air/pull/432>
- DOCS: Include ext.sql in docs by @pydanny in <https://github.com/feldroy/air/pull/433>
- TOOL: Improve Justfile by @tallerasaf in <https://github.com/feldroy/air/pull/431>
- BUG: Fix broken links by @Isaac-Flath in <https://github.com/feldroy/air/pull/440>
- BUG: Updated the example usage command to `just run-py-module examples.tags_render`. by @tallerasaf in <https://github.com/feldroy/air/pull/439>
- DOCS: SQL doc cleanup and fix why page by @pydanny in <https://github.com/feldroy/air/pull/442>

- BUG: Cleanup ext namespace by @pydanny in <https://github.com/feldroy/air/pull/445>

## New Contributors

- @datnq26 made their first contribution in <https://github.com/feldroy/air/pull/415>
- @modasserbillah made their first contribution in <https://github.com/feldroy/air/pull/416>
- @tamerz made their first contribution in <https://github.com/feldroy/air/pull/419>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.29.0...v0.30.0>

## 0.29.0 - 2025-09-12

## What's Changed

- FEAT: Common sense async/sync defaults for SQLModel and SQLAlchemy by @pydanny in <https://github.com/feldroy/air/pull/399>
- REFACTOR: Integrate airdocs into core by @pydanny in <https://github.com/feldroy/air/pull/409>
- FEAT: Add just command to deploy docs to FastAPI cloud by @pydanny in <https://github.com/feldroy/air/pull/412>
- ⬆(deps): Bump the python-dependencies group with 2 updates by @dependabot[bot] in <https://github.com/feldroy/air/pull/405>
- ⬆(deps): Bump ruff from 0.12.12 to 0.13.0 in the python-dependencies group by @dependabot[bot] in <https://github.com/feldroy/air/pull/408>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.27.2...v0.29.0>

## 0.27.2 - 2025-09-08

## What's Changed

- BUG: Address JinjaRenderer conflicts with Sentry by @pydanny in <https://github.com/feldroy/air/pull/404>
- TOOLS: Lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/403>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.27.1...v0.27.2>

## 0.27.1 - 2025-09-06

## What's Changed

- REFACTOR: Proxy HTTPException from FastAPI by @XueSongTap in <https://github.com/feldroy/air/pull/391>
- REFACTOR: make air.TagResponse represent AirResponse by @vanessapigwin in <https://github.com/feldroy/air/pull/392>
- BUG: Input/Textarea tag boolean attributes to use bool type by @audreyfeldroy in <https://github.com/feldroy/air/pull/396>
- TOOLS: command output redirection in run-with-relative-paths by @audreyfeldroy in <https://github.com/feldroy/air/pull/397>
- ⬆(deps):Lock file maintenance by @renovate[bot] in <https://github.com/feldroy/air/pull/390>
- ⬆(deps): Bump pyrefly from 0.30.0 to 0.31.0 in the python-dependencies group by @dependabot[bot] in <https://github.com/feldroy/air/pull/393>
- ⬆(deps): Bump the python-dependencies group across 1 directory with 3 updates by @dependabot[bot] in <https://github.com/feldroy/air/pull/395>

## New Contributors

- @XueSongTap made their first contribution in <https://github.com/feldroy/air/pull/391>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.27.0...v0.27.1>

## 0.27.0 - 2025-08-31

## What's Changed

- REFACTOR: Rename templates.py to templating.py by @Akhilanandateja in <https://github.com/feldroy/air/pull/352>
- REFACTOR: cleanup some noqa, missing-attribute from tools.pyrefly.errors by @vanessapigwin in <https://github.com/feldroy/air/pull/375>
- CHORE: Remove docs GH workflow by @pydanny in <https://github.com/feldroy/air/pull/365>
- TEST: increase test coverage by adding some tests by @mecit-san in <https://github.com/feldroy/air/pull/371>
- FEAT: Add includes argument to AirForm rendering by @pydanny in <https://github.com/feldroy/air/pull/378>
- FEAT: Add AirRouter for combining multiple Air apps into with shared middleware and dependencies by @pydanny in <https://github.com/feldroy/air/pull/367>
- ⬆(deps): Bump ruff from 0.12.10 to 0.12.11 in the python-dependencies group by @dependabot[bot] in <https://github.com/feldroy/air/pull/370>

## New Contributors

- @Akhilanandateja made their first contribution in <https://github.com/feldroy/air/pull/352>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.26.0...v0.27.0>

## 0.26.0 - 2025-08-27

## Changes by New Contributors

- DOCS: add args doctrings for rest of O, some P tags by @vanessapigwin in <https://github.com/feldroy/air/pull/355>
- FEAT: Override mvpcss default layout padding by @mecit-san in <https://github.com/feldroy/air/pull/358>
- REFACTOR: move is_htmx_request to dependencies by @mecit-san in <https://github.com/feldroy/air/pull/357>

## What's Changed

- FEAT: Benchmark suite with pytest-benchmark by @audreyfeldroy in <https://github.com/feldroy/air/pull/345>
- FEAT: Implement hx boost in layout functions by @pydanny in <https://github.com/feldroy/air/pull/361>
- FEAT: Implement RedirectResponse into Air namespace by @WatanabeChika in <https://github.com/feldroy/air/pull/337>
- FEAT: Create examples directory by @pydanny in <https://github.com/feldroy/air/pull/360>
- REFACTOR: Remove mkdocs by @pydanny in <https://github.com/feldroy/air/pull/364>
- REFACTOR: locals cleanup utility and streamline attribute handling by @tallerasaf in <https://github.com/feldroy/air/pull/359>
- REFACTOR: Move benchmarks to isolated directory by @pydanny in <https://github.com/feldroy/air/pull/351>
- REFACTOR: Run ruff on code after enabling more rules by @tallerasaf in <https://github.com/feldroy/air/pull/346>
- TESTS: Add tests for locals_cleanup in tags utils by @audreyfeldroy in <https://github.com/feldroy/air/pull/344>
- ⬆(deps): Bump pyrefly from 0.29.2 to 0.30.0 in the python-dependencies group by @dependabot[bot] in <https://github.com/feldroy/air/pull/362>
- ⬆(deps): bump the python-dependencies group with 4 updates by @dependabot[bot] in <https://github.com/feldroy/air/pull/341>

## New Contributors

- @vanessapigwin made their first contribution in <https://github.com/feldroy/air/pull/355>
- @mecit-san made their first contribution in <https://github.com/feldroy/air/pull/357>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.25.2...v0.26.0>

## 0.25.2 - 2025-08-23

## What's Changed

- Fix memory leak by @pydanny in <https://github.com/feldroy/air/pull/343>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.25.1...v0.25.2>

## 0.25.1 - 2025-08-23

## What's Changed

- TOOL: PyRefly by @tallerasaf in <https://github.com/feldroy/air/pull/318>
- BUG: Performance optimizations by @pydanny in <https://github.com/feldroy/air/pull/342>
- BUG: Add missing autofocus option to AirField by @pydanny in <https://github.com/feldroy/air/pull/324>
- ⬆(deps): bump ty from 0.0.1a18 to 0.0.1a19 by @dependabot[bot] in <https://github.com/feldroy/air/pull/323>
- ⬆(deps): bump rust-just from 1.42.3 to 1.42.4 by @dependabot[bot] in <https://github.com/feldroy/air/pull/331>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.25.0...v0.25.1>

## 0.25.0 - 2025-08-22

## What's Changed

- FEAT: Add SessionMiddleware class by @pydanny in <https://github.com/feldroy/air/pull/334>
- BUG: `attribute_set_to_true=True` converts underscores to dashes by @WatanabeChika in <https://github.com/feldroy/air/pull/327>
- DOC: Rearrange MVPCSS docs by @pydanny in <https://github.com/feldroy/air/pull/330>
- ⬆(deps): bump mkdocstrings-python from 1.16.12 to 1.17.0 by @dependabot[bot] in <https://github.com/feldroy/air/pull/320>
- ⬆(deps): bump pytest-memray from 1.7.0 to 1.8.0 by @dependabot[bot] in <https://github.com/feldroy/air/pull/319>

## New Contributors

- @WatanabeChika made their first contribution in <https://github.com/feldroy/air/pull/327>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.24.2...v0.25.0>

## 0.24.2 - 2025-08-21

## What's Changed

- BUG: AirForm.validate method returns boolean instead of None by @pydanny in <https://github.com/feldroy/air/pull/317>
- TOOL: New CI overview by @tallerasaf in <https://github.com/feldroy/air/pull/304>
- DOC: Docstring improvements by @pydanny in <https://github.com/feldroy/air/pull/322>
- DOC: Fix document grammar by @pydanny in <https://github.com/feldroy/air/pull/328>
- ⬆(deps): bump ruff from 0.12.0 to 0.12.9 by @dependabot[bot] in <https://github.com/feldroy/air/pull/321>
- ⬆(deps): Bump ty from 0.0.1a16 to 0.0.1a18 by @dependabot[bot] in <https://github.com/feldroy/air/pull/306>
- ⬆(deps): Bump uvicorn from 0.34.3 to 0.35.0 by @dependabot[bot] in <https://github.com/feldroy/air/pull/308>
- ⬆(deps): Bump types-markdown from 3.8.0.20250415 to 3.8.0.20250809 by @dependabot[bot] in <https://github.com/feldroy/air/pull/309>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.24.1...v0.24.2>

## 0.24.1 - 2025-08-18

## What's Changed

- BUG: Address for_ and as_ args for label and link tags by @pydanny in <https://github.com/feldroy/air/pull/312>
- BUG: Change AirForm's default_form_widget to use mvp.css by @pydanny in <https://github.com/feldroy/air/pull/314>
- DOC: Add module level docstrings by @pydanny in <https://github.com/feldroy/air/pull/298>
- TOOL: Configure Renovate by @renovate[bot] in <https://github.com/feldroy/air/pull/300>
- TOOL: CI Overview by @tallerasaf in <https://github.com/feldroy/air/pull/303>
- TOOL: Ruff - 1 by @tallerasaf in <https://github.com/feldroy/air/pull/299>
- TOOL: Ty by @tallerasaf in <https://github.com/feldroy/air/pull/302>
- TOOL: Fix dependabot by @tallerasaf in <https://github.com/feldroy/air/pull/310>
- TOOL: Lint with new rules by @pydanny in <https://github.com/feldroy/air/pull/313>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.24.0...v0.24.1>

## 0.24.0 - 2025-08-17

## What's Changed

- Convert underscores to dashes in app.page method by @pydanny in <https://github.com/feldroy/air/pull/293>
- Remove last unnecessary type: ignore by @pydanny in <https://github.com/feldroy/air/pull/291>
- Bring in the new logo to the README by @pydanny in <https://github.com/feldroy/air/pull/289>
- Docstring improvements by @pydanny in <https://github.com/feldroy/air/pull/296>
- Document docstring management in CONTRIBUTING.md by @pydanny in <https://github.com/feldroy/air/pull/297>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.23.0...v0.24.0>

## 0.23.0 - 2025-08-15

## Summary

For users, the function signatures on Air SVG tags by @dfundako will make building SVGs much easier for both humans and LLMs. @tallerasaf vastly improves our code coverage build and turns Air poetic with this statement about the wall of badges they have created for us:

> "Each badge gleams like a prayer stitched in code, blessing the dawn of an open-source journey."

## What's Changed

- Add function signatures to Air SVG Tags by @dfundako in <https://github.com/feldroy/air/pull/246>
- Enhance test coverage enforcement and README badges by @tallerasaf in <https://github.com/feldroy/air/pull/288>
- Add justfile list recipe by @pydanny in <https://github.com/feldroy/air/pull/285>
- Improve SVG testing by @pydanny in <https://github.com/feldroy/air/pull/286>
- Lower coverage threshold to 95% by @pydanny in <https://github.com/feldroy/air/pull/287>

## New Contributors

- @dfundako made their first contribution in <https://github.com/feldroy/air/pull/246>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.22.1...v0.23.0>

## 0.22.1 - 2025-08-14

## What's Changed

- BUG: Repair the svg import path by @pydanny in <https://github.com/feldroy/air/pull/284>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.22.0...v0.22.1>

## 0.22.0 - 2025-08-14

## What's Changed

This is mostly a CI release, which doesn't affect users of Air itself. Many thanks to @tallerasaf who put most of these together.

- Feat Improved development environment setup by @tallerasaf in <https://github.com/feldroy/air/pull/267>
- Switch from pytest-rich to pytest-modern by @pydanny in <https://github.com/feldroy/air/pull/275>
- Full - CI Test Coverage by @tallerasaf in <https://github.com/feldroy/air/pull/272>
- Improve CI workflows, annotations in the GitHub using GitHub Actions and CI for ubuntu-latest, windows-latest, macos-latest by @tallerasaf in <https://github.com/feldroy/air/pull/279>
- BUG: Fix logo in README by @pydanny in <https://github.com/feldroy/air/pull/281>
- Refine test coverage tasks and commands in Justfile by @tallerasaf in <https://github.com/feldroy/air/pull/283>

We did get in one feature to Air itself:

- Support MVP.css air.Header tag not being in body by @pydanny in <https://github.com/feldroy/air/pull/273>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.21.0...v0.22.0>

## 0.21.0 - 2025-08-12

## What's Changed

- Use HTML page for 500 errors by @pydanny in <https://github.com/feldroy/air/pull/265>
- SSEResponse now handles str, Tag, and Any types, with linebreaks handled cleanly by @pydanny in <https://github.com/feldroy/air/pull/257>
- Improvements to pyproject.toml - by @tallerasaf in <https://github.com/feldroy/air/pull/261> and <https://github.com/feldroy/air/pull/262>
- Refactor tags module into a modular package structure by @tallerasaf in <https://github.com/feldroy/air/pull/260>
- Convert default exception handlers to use mvpcss for layout by @pydanny in <https://github.com/feldroy/air/pull/266>
- Set up an "Air" Discord badge by @tallerasaf in <https://github.com/feldroy/air/pull/256> and <https://github.com/feldroy/air/pull/258>
- Add missing env and context processors to JinjaRenderer by @pydanny in <https://github.com/feldroy/air/pull/263>

- ⬆ Bump actions/checkout from 4 to 5 by @dependabot[bot] in <https://github.com/feldroy/air/pull/264>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.20.0...v0.21.0>

## 0.20.0 - 2025-08-07

## What's Changed

- pyproject.toml to expose a new optional-extras group called standard by @tallerasaf in <https://github.com/feldroy/air/pull/252>
- Refactor EventStreamResponse to SSEResponse by @pydanny in <https://github.com/feldroy/air/pull/249>
- Readme improvements by @audreyfeldroy in <https://github.com/feldroy/air/pull/245>
- Update justfile by @tallerasaf in <https://github.com/feldroy/air/pull/244>
- Add missing starlette.requests.Request passthrough by @pydanny in <https://github.com/feldroy/air/pull/254>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.19.0...v0.20.0>

## 0.19.0 - 2025-08-04

## What's Changed

- Support for SSE by @pydanny and @audreyfeldroy in <https://github.com/feldroy/air/pull/240>
- refactor: consolidate tag imports in **init**.py by @tallerasaf in <https://github.com/feldroy/air/pull/239>
- Fix justfile pdb option by @pydanny in <https://github.com/feldroy/air/pull/233>
- Remove deprecated Jinja2Renderer by @pydanny in <https://github.com/feldroy/air/pull/234>
- Begin phasing out content in docs by @pydanny in <https://github.com/feldroy/air/pull/235>
- Better types for width and height tag attrs by @pydanny in <https://github.com/feldroy/air/pull/236>
- Clarification of internal tag control name by @pydanny in <https://github.com/feldroy/air/pull/237>
- Add issue templates for bugs, features, discussions, etc by @pydanny in <https://github.com/feldroy/air/pull/238>
- Document how to use forms Starlette style by @pydanny in <https://github.com/feldroy/air/pull/228>

## New Contributors

- @tallerasaf made their first contribution in <https://github.com/feldroy/air/pull/239>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.18.0...v0.19.0>

## 0.18.0 - 2025-08-02

## What's Changed

- Clarify about minimalist core by @audreyfeldroy in <https://github.com/feldroy/air/pull/222>
- feat: disable docs by default by @kmehran1106 in <https://github.com/feldroy/air/pull/221>
- Remove CLI and static site generator by @pydanny in <https://github.com/feldroy/air/pull/216>
- Remove unused dependencies by @pydanny in <https://github.com/feldroy/air/pull/217>
- Change dependency groups by @pydanny in <https://github.com/feldroy/air/pull/218>
- Add .vscode to gitignore by @pydanny in <https://github.com/feldroy/air/pull/219>
- Fine tune justfile by @pydanny in <https://github.com/feldroy/air/pull/220>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.17.0...v0.18.0>

## 0.17.0 - 2025-07-30

## What's Changed

- refactor: removing type ignore by @kmehran1106 in <https://github.com/feldroy/air/pull/213>
- Fix tag nav by @pydanny in <https://github.com/feldroy/air/pull/207>
- Tags and Tag passes through other tags when called directly by @pydanny in <https://github.com/feldroy/air/pull/210>
- Remove the HTML to Air Tag utility by @pydanny in <https://github.com/feldroy/air/pull/215>

## New Contributors

- @kmehran1106 made their first contribution in <https://github.com/feldroy/air/pull/213>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.16.0...v0.17.0>

## 0.16.0 - 2025-07-28

## What's Changed

- Rename Jinja2Renderer to JinjaRenderer by @pydanny in <https://github.com/feldroy/air/pull/204>
- Autorender tags in JinjaRender by @pydanny in <https://github.com/feldroy/air/pull/205>
- Document tags starting with I by @pydanny in <https://github.com/feldroy/air/pull/189>
- Layouts concepts by @Isaac-Flath in <https://github.com/feldroy/air/pull/192>
- Document the L tags by @pydanny in <https://github.com/feldroy/air/pull/194>
- Add in chart example by @pydanny in <https://github.com/feldroy/air/pull/197>
- Document Mark and Menu tags by @pydanny in <https://github.com/feldroy/air/pull/198>
- More docs for tags by @pydanny in <https://github.com/feldroy/air/pull/199>
- Type args and kwargs in tags and bump ty version by @pydanny in <https://github.com/feldroy/air/pull/200>
- Refactor tag docs by @pydanny in <https://github.com/feldroy/air/pull/201>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.15.0...v0.16.0>

## 0.15.0 - 2025-07-22

## What's Changed

- Add type hints for tags with attributes by @Isaac-Flath in <https://github.com/feldroy/air/pull/143>
- Replace Makefile with justfile by @audreyfeldroy in <https://github.com/feldroy/air/pull/184>
- AirField args now include all of Pydantic Field args by @pydanny in <https://github.com/feldroy/air/pull/167>
- Change RawHTML to Raw by @pydanny in <https://github.com/feldroy/air/pull/169>
- Document Tag args to button by @pydanny in <https://github.com/feldroy/air/pull/173>
- Tests for background task by @pydanny in <https://github.com/feldroy/air/pull/175>
- Improve tests for forms by @pydanny in <https://github.com/feldroy/air/pull/176>
- Document tags and clean up tag types by @pydanny in <https://github.com/feldroy/air/pull/177>
- Undo Optional[str] by @pydanny in <https://github.com/feldroy/air/pull/178>
- Switch to use uv run for python options in Make by @pydanny in <https://github.com/feldroy/air/pull/179>
- Improve test coverage for tags.py by @pydanny in <https://github.com/feldroy/air/pull/180>
- Document more tags by @pydanny in <https://github.com/feldroy/air/pull/181>
- Single source of version by @pydanny in <https://github.com/feldroy/air/pull/188>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.14.2...v0.15.0>

## 0.14.2 - 2025-07-18

## What's Changed

- Create AirField wrapper for Pydantic Field by @pydanny in <https://github.com/feldroy/air/pull/164>
- Update what is claimed for Python support by @pydanny in <https://github.com/feldroy/air/pull/156>
- Add support for returning multiple children in Air Tags from views by @pydanny in <https://github.com/feldroy/air/pull/158>
- Add types of contribution section to CONTRIBUTING.md by @pydanny in <https://github.com/feldroy/air/pull/160>
- Add jinja to the alternatives page by @pydanny in <https://github.com/feldroy/air/pull/161>
- Add default HTML page for 404 errors by @pydanny in <https://github.com/feldroy/air/pull/162>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.13.0...v0.14.2>

## 0.13.0 - 2025-07-17

## What's Changed

- Implement FastAPI background tasks by @pydanny in <https://github.com/feldroy/air/pull/127>
- Pass through requests by @pydanny in <https://github.com/feldroy/air/pull/138>
- Add function signature for Tag A by @pydanny in <https://github.com/feldroy/air/pull/140>
- Passthru all the responses by @pydanny in <https://github.com/feldroy/air/pull/141>
- Pass through starlette staticfiles by @pydanny in <https://github.com/feldroy/air/pull/144>
- Stringify/escape unsupported tag children so 500 errors aren't thrown on tag children type failures by @pydanny in <https://github.com/feldroy/air/pull/147>
- Explaining how to use Jinja with Air Tags by @pydanny in <https://github.com/feldroy/air/pull/148>
- Add boolean attributes to Air Tags plus improve docs by @pydanny in <https://github.com/feldroy/air/pull/152>
- Properly make self-closing tags like input and img self-close by @pydanny in <https://github.com/feldroy/air/pull/154>
- Switch from mypy to ty by @pydanny in <https://github.com/feldroy/air/pull/155>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.12.0...v0.13.0>

## 0.11.0 - 2025-07-12

##  New Features

- Update .editorconfig for improved file handling by @audreyfeldroy in <https://github.com/feldroy/air/pull/121>
- Added Form rendering by @pydanny in <https://github.com/feldroy/air/pull/120>
- Added `html_to_airtags` function, converts HTML to Air Tags by @pydanny in <https://github.com/feldroy/air/pull/125>

## Documentation improvements

- Reorder member order in object docs by @pydanny in <https://github.com/feldroy/air/pull/116>
- Documentation on how to escape HTML by @pydanny in <https://github.com/feldroy/air/pull/108>
- Update project description in README and pyproject.toml by @audreyfeldroy in <https://github.com/feldroy/air/pull/118>
- Update CONTRIBUTING.md with docs, tests, and troubleshooting by @audreyfeldroy in <https://github.com/feldroy/air/pull/119>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.11.0...v0.12.0>

## 0.11.0 - 2025-07-09

## What's Changed

- Add layouts module with pico example by @audreyfeldroy and @pydanny in <https://github.com/feldroy/air/pull/87>
- Restructure docs by @pydanny in <https://github.com/feldroy/air/pull/100>
- Add README badges and refactor README by @pydanny in <https://github.com/feldroy/air/pull/101>
- Documentation improvements by @pydanny in <https://github.com/feldroy/air/pull/102>
- Add logo by @audreyfeldroy and @pydanny in <https://github.com/feldroy/air/pull/103>
- Document how `page` works with index by @pydanny in <https://github.com/feldroy/air/pull/105>
- For Jinja rendering, change "render" var name to "jinja" by @pydanny in <https://github.com/feldroy/air/pull/106>
- Restructure docs yet again by @pydanny in <https://github.com/feldroy/air/pull/109>
- Add MVP.css and change `pico()` function name to `picocss()` by @audreyfeldroy and @pydanny in <https://github.com/feldroy/air/pull/114>
- Refactor HTML attr cleanup function by @audreyfeldroy and @pydanny in <https://github.com/feldroy/air/pull/115>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.10.0...v0.11.0>

## 0.10.0 - 2025-07-07

## What's Changed

- Remove the ability to change the Air default response class by @pydanny in <https://github.com/feldroy/air/pull/79>
- Add kwargs to Jinja2Renderer by @pydanny in <https://github.com/feldroy/air/pull/84>
- About section by @pydanny in <https://github.com/feldroy/air/pull/73>
- Sort imports and add import sorting to clean command by @pydanny in <https://github.com/feldroy/air/pull/90>
- Added form validation via Air Forms by @pydanny in <https://github.com/feldroy/air/pull/81>
- Support mkdoc-material admonitions by @pydanny in <https://github.com/feldroy/air/pull/95>
- Allow non-escaped code through Style and Script tags by @Isaac-Flath and @pydanny in <https://github.com/feldroy/air/pull/96>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.9.0...v0.10.0>

## 0.9.0 - 2025-07-03

## What's Changed

- Add AirResponse and get-only `app.page` route decorator shortcut by @pydanny in <https://github.com/feldroy/air/pull/76>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.8.0...v0.9.0>

## 0.8.0 - 2025-06-29

## What's Changed

- Remove headers arg from Html tag by @pydanny in <https://github.com/feldroy/air/pull/68>
- Escape strings in tags by @pydanny in <https://github.com/feldroy/air/pull/72>
- Add GH action to release on PyPI by @pydanny in <https://github.com/feldroy/air/pull/74>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.7.0...v0.8.0>

## 0.7.0 - 2025-06-28

## What's Changed

- Api docs by @Isaac-Flath in <https://github.com/feldroy/air/pull/47>
- Motto grammar fix by @pydanny in <https://github.com/feldroy/air/pull/49>
- Add missing function signatures to `application.Air` by @pydanny in <https://github.com/feldroy/air/pull/52>
- Add doc nav improvements and API Ref index by @pydanny in <https://github.com/feldroy/air/pull/50>
- Add missing applications ref by @pydanny in <https://github.com/feldroy/air/pull/53>
- Explain air tags by @pydanny in <https://github.com/feldroy/air/pull/62>
- Convert `Tag.children` property to for loop and fix bug by @pydanny in <https://github.com/feldroy/air/pull/64>
- Dependency upgrade by @pydanny in <https://github.com/feldroy/air/pull/67>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.6.0...v0.7.0>

## 0.6.0 - 2025-06-26

## What's Changed

- Add run instructions to quickstart docs by @Isaac-Flath in <https://github.com/feldroy/air/pull/45>
- Create applications.Air wrapper for fastapi.FastAPI by @pydanny in <https://github.com/feldroy/air/pull/46>

Minimal apps now look like this:

```python
import air

app = air.Air()


@app.get("/")
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

## New Contributors

- @Isaac-Flath made their first contribution in <https://github.com/feldroy/air/pull/45>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.5.0...v0.6.0>

## 0.5.0 - 2025-06-25

## What's Changed

- Merged in fastapi-tags by @pydanny in <https://github.com/feldroy/air/pull/36>
- Improve install docs by @audreyfeldroy in <https://github.com/feldroy/air/pull/39>
- Shortcut renderer for jinja2 by @pydanny in <https://github.com/feldroy/air/pull/40>
- Document how to remove HTML results from API docs by @pydanny in <https://github.com/feldroy/air/pull/41>
- Quick start tutorial by @pydanny in <https://github.com/feldroy/air/pull/42>

**Full Changelog**: <https://github.com/feldroy/air/compare/v0.4.0...v0.5.0>

## 0.4.0 - 2025-06-24

## What's Changed

- Create a GitHub Actions workflow for running tests with Tox by @audreyfeldroy in <https://github.com/feldroy/air/pull/8>
- Convert to vanilla uv by @pydanny in <https://github.com/feldroy/air/pull/12>
- Upgrade checks to use UV by @pydanny in <https://github.com/feldroy/air/pull/14>
- docs: fix link to audrey.feldroy.com in README by @johnfraney in <https://github.com/feldroy/air/pull/15>
- Convert CLI to use typer by @pydanny in <https://github.com/feldroy/air/pull/17>
- Add fastapi-tags for Python classes to render HTML by @pydanny in <https://github.com/feldroy/air/pull/16>
- Add docs by @pydanny in <https://github.com/feldroy/air/pull/18>
- Improve readme and move static site generation to docs by @pydanny in <https://github.com/feldroy/air/pull/23>
- Various repo cleanup chores by @pydanny in <https://github.com/feldroy/air/pull/24>

## New Contributors

- @audreyfeldroy made their first contribution in <https://github.com/feldroy/air/pull/8>
- @pydanny made their first contribution in <https://github.com/feldroy/air/pull/12>
- @johnfraney made their first contribution in <https://github.com/feldroy/air/pull/15>

**Full Changelog**: <https://github.com/feldroy/air/compare/0.3.0...v0.4.0>

## 0.3.0 - 2024-07-07

- Static site generation
- Template inheritance
- Markdown support
