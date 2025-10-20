### Latest Changes

# 0.37.0 - 2025-10-16

## What's Changed
* BOOK: The Air Book by @audreyfeldroy in https://github.com/feldroy/air/pull/504
* BUG: Constrain renderers to only stringify items inheriting from BaseTag by @bluerosej  and @pydanny in https://github.com/feldroy/air/pull/561
* DOCS: book example uses the wrong library #576 by @MrValdez in https://github.com/feldroy/air/pull/577
* docs(tags): add docstring Args for S to Small by @vanessapigwin in https://github.com/feldroy/air/pull/558
* Integrate spelling and grammar checkers (`codespell` and `typos`) for the entire project! by @tallerasaf in https://github.com/feldroy/air/pull/548
* Fix link to air tags by @pydanny in https://github.com/feldroy/air/pull/567
* docs: add Args for Source to Sup tags by @vanessapigwin in https://github.com/feldroy/air/pull/568
* chore(deps): update astral-sh/setup-uv digest to 3259c62 by @renovate[bot] in https://github.com/feldroy/air/pull/562
* Finish moving ext.sql to ext.sqlmodel by @pydanny in https://github.com/feldroy/air/pull/560
* Quickstart: SSE plus file in `/examples` by @pydanny in https://github.com/feldroy/air/pull/572
* Address doclink warnings by @pydanny in https://github.com/feldroy/air/pull/573
* Configure project for mkdocs-llmstxt by @pydanny in https://github.com/feldroy/air/pull/574

## New Contributors
* @bluerosej made their first contribution in https://github.com/feldroy/air/pull/561
* @MrValdez made their first contribution in https://github.com/feldroy/air/pull/577

**Full Changelog**: https://github.com/feldroy/air/compare/v0.36.0...v0.37.0

# 0.36.0 - 2025-10-10

## What's Changed
* Implement .htmx object on air.Request by @pydanny in https://github.com/feldroy/air/pull/524
* Drop Python 3.12 support! by @tallerasaf in https://github.com/feldroy/air/pull/538
* Add forms quickstart by @pydanny in https://github.com/feldroy/air/pull/536 and https://github.com/feldroy/air/pull/539
* Restore llms.txt for LLM-friendly documentation by @intellectronica in https://github.com/feldroy/air/pull/552
* fixed broken cookbook docs link by @alaminopu in https://github.com/feldroy/air/pull/553
* Temporary just tdd fix for Python 3.14 by @tallerasaf in https://github.com/feldroy/air/pull/555
* Add comprehensive tests for default_form_widget by @kernelshard in https://github.com/feldroy/air/pull/535
* Remove redundant CI workflow and simplify coverage configuration by @tallerasaf in https://github.com/feldroy/air/pull/542
* Fix the request part of the docs by @pydanny in https://github.com/feldroy/air/pull/557
* chore(deps): update astral-sh/setup-uv action to v7 by @renovate[bot] in https://github.com/feldroy/air/pull/541
* chore(deps): update dependency uv_build to >=0.9.0,<0.10.0 by @renovate[bot] in https://github.com/feldroy/air/pull/543
* ⬆(deps): Bump the python-dependencies group across 1 directory with 5 updates by @dependabot[bot] in https://github.com/feldroy/air/pull/556

## New Contributors
* @kernelshard made their first contribution in https://github.com/feldroy/air/pull/535
* @intellectronica made their first contribution in https://github.com/feldroy/air/pull/552

**Full Changelog**: https://github.com/feldroy/air/compare/v0.35.0...v0.36.0

# 0.35.0 - 2025-10-06

## What's Changed
* FEAT: add option for app.page decorator to convert underscores to forward slashes by default by @alaminopu in https://github.com/feldroy/air/pull/522
* FEAT: Add support for Python 3.14! by @tallerasaf in https://github.com/feldroy/air/pull/529
* DOCS: : add usage and recipes for requests.Request by @zorexsalvo in https://github.com/feldroy/air/pull/527
* DOCS: Add mixed bread AI search on docs by @pydanny and @audreyfeldroy in https://github.com/feldroy/air/pull/530
* DOCS: Refine `ruff` configuration by @tallerasaf in https://github.com/feldroy/air/pull/528
* DOCS: Show use of include router for bigger apps by @pydanny in https://github.com/feldroy/air/pull/531
* build(deps): lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/534
* chore(deps): update wechuli/allcheckspassed action to v2.1.0 by @renovate[bot] in https://github.com/feldroy/air/pull/532

## New Contributors
* @zorexsalvo made their first contribution in https://github.com/feldroy/air/pull/527

**Full Changelog**: https://github.com/feldroy/air/compare/v0.34.0...v0.35.0

# 0.34.0 - 2025-10-04

## What's Changed
* REFACTOR: Change name of air.ext.sql to air.ext.sqlmodel by @pydanny in https://github.com/feldroy/air/pull/526
* DOCS: Quickstart javascript and CSS files by @pydanny in https://github.com/feldroy/air/pull/520
* DOCS: Describes adding variables in different ways to URLs in Quickstart by @pydanny in https://github.com/feldroy/air/pull/523
* build(deps): lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/509

**Full Changelog**: https://github.com/feldroy/air/compare/v0.33.1...v0.34.0

# 0.33.1 - 2025-09-30

## What's Changed
* BUGFIX: Provide option to set GH callback URI by @pydanny in https://github.com/feldroy/air/pull/517
* DOCS: Roadmap docs cleanup by @pydanny in https://github.com/feldroy/air/pull/507
* DOCS: Move alternatives to use admonitions by @pydanny in https://github.com/feldroy/air/pull/508
* DOCS: Add routing to quickstart by @pydanny in https://github.com/feldroy/air/pull/514
* DOCS: Add airblog example by @pydanny in https://github.com/feldroy/air/pull/513

**Full Changelog**: https://github.com/feldroy/air/compare/v0.33.0...v0.33.1

# 0.33.0 - 2025-09-26

## New Features
* Show type of form failure rather than just an error happened by @prodigisoftwares in https://github.com/feldroy/air/pull/495
* Constrain the exports from air.ext.sql by @pydanny in https://github.com/feldroy/air/pull/496
* Add dark theme support to docs by @EnriqueSoria in https://github.com/feldroy/air/pull/499
* Renderable Type for Tag children by @audreyfeldroy in https://github.com/feldroy/air/pull/498

## Bugfixes

* docs: update jinja templating example by @alaminopu in https://github.com/feldroy/air/pull/497

## Chores
* ⬆(deps): Bump the python-dependencies group across 1 directory with 5 updates by @dependabot[bot] in https://github.com/feldroy/air/pull/494
* Bring forward old version release instructions by @pydanny in https://github.com/feldroy/air/pull/501

## New Contributors
* @EnriqueSoria made their first contribution in https://github.com/feldroy/air/pull/499

**Full Changelog**: https://github.com/feldroy/air/compare/v0.32.0...v0.33.0

# 0.32.0 - 2025-09-24

## What's Changed
* FEAT: Add changelog link to pyproject.toml by @alaminopu in https://github.com/feldroy/air/pull/480
* FEAT: Make the default status_code of air.RedirectResponse be 303 by @alaminopu in https://github.com/feldroy/air/pull/481
* Merge cookbook into learn section by @pydanny in https://github.com/feldroy/air/pull/483
* DOCS:  Enhance contribution guide with detailed setup instructions by @tallerasaf in https://github.com/feldroy/air/pull/484
* Add GitHubOAuthClientFactory to support easier authentication by @pydanny and @audreyfeldroy in https://github.com/feldroy/air/pull/487
* Improved learn docs for SQL by @pydanny in https://github.com/feldroy/air/pull/488
* Add script to look for missing examples in callables by @pydanny in https://github.com/feldroy/air/pull/489
* FEAT: pretty_render enhancements by @tallerasaf in https://github.com/feldroy/air/pull/477
* docs: add docstrings for P, Q and R tags by @vanessapigwin in https://github.com/feldroy/air/pull/492
* Various minor fixes to documentation by @pydanny in https://github.com/feldroy/air/pull/493
* build(deps): lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/482
* chore(deps): update wechuli/allcheckspassed action to v2 by @renovate[bot] in https://github.com/feldroy/air/pull/491

## New Contributors
* @alaminopu made their first contribution in https://github.com/feldroy/air/pull/480

**Full Changelog**: https://github.com/feldroy/air/compare/v0.31.0...v0.32.0

# 0.31.0 - 2025-09-21

## What's Changed
* Add latest-changes GitHub Action workflow (Issue #163) by @prodigisoftwares in https://github.com/feldroy/air/pull/437
* Issue #60-Document-is_htmx_request - Add documentation and add a coup… by @prodigisoftwares in https://github.com/feldroy/air/pull/458
* Incremental doc improvements by @pydanny in https://github.com/feldroy/air/pull/448
* Documentation on Airtag cleanup by @pydanny in https://github.com/feldroy/air/pull/450
* chore(deps): update actions/checkout action to v5 by @renovate[bot] in https://github.com/feldroy/air/pull/449
* Added a new "all" group for combined optional dependencies in `pyproject.toml` by @tallerasaf in https://github.com/feldroy/air/pull/451
* Add missing doc pages by @pydanny in https://github.com/feldroy/air/pull/452
* Add requests to documentation by @pydanny in https://github.com/feldroy/air/pull/455
* Add PR checklist by @pydanny in https://github.com/feldroy/air/pull/456
* ⬆(deps): Bump rich from 12.6.0 to 14.1.0 in the python-dependencies group across 1 directory by @dependabot[bot] in https://github.com/feldroy/air/pull/457
* Small refactor extracted from a big PR by @tallerasaf in https://github.com/feldroy/air/pull/459
* Add type annotations to the entire codebase using pyrefly and ruff(What they could do, still not 100%) by @tallerasaf in https://github.com/feldroy/air/pull/441
* chore: update Codecov config and refine coverage exclusions by @tallerasaf in https://github.com/feldroy/air/pull/469
* Drop Python 3.10 and 3.11 by @tallerasaf in https://github.com/feldroy/air/pull/470
* Added get_object_or_404 to air.ext.sql. by @pydanny and @audreyfeldroy in https://github.com/feldroy/air/pull/466
* Move ty ignore rule to correct location in pyproject.toml by @pydanny in https://github.com/feldroy/air/pull/471
* Add docs issue template by @pydanny in https://github.com/feldroy/air/pull/474
* Change air.db.sql path to air.ext.sql in docs by @pydanny in https://github.com/feldroy/air/pull/476
* Add lifespan db func to air.ext.sql by @pydanny and @audreyfeldroy in https://github.com/feldroy/air/pull/478
* Make contributing.md more concise by @pydanny in https://github.com/feldroy/air/pull/479

## New Contributors
* @prodigisoftwares made their first contribution in https://github.com/feldroy/air/pull/437

**Full Changelog**: https://github.com/feldroy/air/compare/v0.30.0...v0.31.0

# 0.30.0 - 2025-09-17

## What's Changed

### New contributor submissions
* BUG: resolve type-check errors pyrefly in docs by adding path by @datnq26 in https://github.com/feldroy/air/pull/415
* DOCS: add two uv steps by @modasserbillah in https://github.com/feldroy/air/pull/416
* DOCS: Import Field from pydantic by @tamerz in https://github.com/feldroy/air/pull/419

### Big changes
* FEAT: Improve tag rendering by @tallerasaf in https://github.com/feldroy/air/pull/377
* FEAT: Add GitHub OAuth router Factory by @pydanny in https://github.com/feldroy/air/pull/443
* FEAT: Add templating.Renderer ComponentLoader by @pydanny in https://github.com/feldroy/air/pull/430

### Everything else

* ⬆(deps): Bump pytest-asyncio from 1.1.0 to 1.2.0 in the python-dependencies group by @dependabot[bot] in https://github.com/feldroy/air/pull/413
* BUG: Move content of db to ext by @pydanny in https://github.com/feldroy/air/pull/421
* TOOL: Migrate airdocs to mkdocs by @pydanny in https://github.com/feldroy/air/pull/422
* TOOL: Add build command back by @pydanny in https://github.com/feldroy/air/pull/424
* DOCS: Fix rotating reasons not to use air by @pydanny in https://github.com/feldroy/air/pull/425
* DOCS: Fix doc index links by @pydanny in https://github.com/feldroy/air/pull/426
* DOCS: Fix errant doc links by @pydanny in https://github.com/feldroy/air/pull/427
* build(deps): lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/428
* FEAT: Get test coverage back up to 95+% by @pydanny in https://github.com/feldroy/air/pull/432
* DOCS: Include ext.sql in docs by @pydanny in https://github.com/feldroy/air/pull/433
* TOOL: Improve Justfile by @tallerasaf in https://github.com/feldroy/air/pull/431
* BUG: Fix broken links by @Isaac-Flath in https://github.com/feldroy/air/pull/440
* BUG: Updated the example usage command to `just run-py-module examples.tags_render`. by @tallerasaf in https://github.com/feldroy/air/pull/439
* DOCS: SQL doc cleanup and fix why page by @pydanny in https://github.com/feldroy/air/pull/442

* BUG: Cleanup ext namespace by @pydanny in https://github.com/feldroy/air/pull/445

## New Contributors
* @datnq26 made their first contribution in https://github.com/feldroy/air/pull/415
* @modasserbillah made their first contribution in https://github.com/feldroy/air/pull/416
* @tamerz made their first contribution in https://github.com/feldroy/air/pull/419

**Full Changelog**: https://github.com/feldroy/air/compare/v0.29.0...v0.30.0

# 0.29.0 - 2025-09-12

## What's Changed
* FEAT: Common sense async/sync defaults for SQLModel and SQLAlchemy by @pydanny in https://github.com/feldroy/air/pull/399
* REFACTOR: Integrate airdocs into core by @pydanny in https://github.com/feldroy/air/pull/409
* FEAT: Add just command to deploy docs to FastAPI cloud by @pydanny in https://github.com/feldroy/air/pull/412
* ⬆(deps): Bump the python-dependencies group with 2 updates by @dependabot[bot] in https://github.com/feldroy/air/pull/405
* ⬆(deps): Bump ruff from 0.12.12 to 0.13.0 in the python-dependencies group by @dependabot[bot] in https://github.com/feldroy/air/pull/408

**Full Changelog**: https://github.com/feldroy/air/compare/v0.27.2...v0.29.0

# 0.27.2 - 2025-09-08

## What's Changed
* BUG: Address JinjaRenderer conflicts with Sentry by @pydanny in https://github.com/feldroy/air/pull/404
* TOOLS: Lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/403

**Full Changelog**: https://github.com/feldroy/air/compare/v0.27.1...v0.27.2

# 0.27.1 - 2025-09-06

## What's Changed
* REFACTOR: Proxy HTTPException from FastAPI by @XueSongTap in https://github.com/feldroy/air/pull/391
* REFACTOR: make air.TagResponse represent AirResponse by @vanessapigwin in https://github.com/feldroy/air/pull/392
* BUG: Input/Textarea tag boolean attributes to use bool type by @audreyfeldroy in https://github.com/feldroy/air/pull/396
* TOOLS: command output redirection in run-with-relative-paths by @audreyfeldroy in https://github.com/feldroy/air/pull/397
* ⬆(deps):Lock file maintenance by @renovate[bot] in https://github.com/feldroy/air/pull/390
* ⬆(deps): Bump pyrefly from 0.30.0 to 0.31.0 in the python-dependencies group by @dependabot[bot] in https://github.com/feldroy/air/pull/393
* ⬆(deps): Bump the python-dependencies group across 1 directory with 3 updates by @dependabot[bot] in https://github.com/feldroy/air/pull/395

## New Contributors
* @XueSongTap made their first contribution in https://github.com/feldroy/air/pull/391

**Full Changelog**: https://github.com/feldroy/air/compare/v0.27.0...v0.27.1

# 0.27.0 - 2025-08-31

## What's Changed
* REFACTOR: Rename templates.py to templating.py by @Akhilanandateja in https://github.com/feldroy/air/pull/352
* REFACTOR: cleanup some noqa, missing-attribute from tools.pyrefly.errors by @vanessapigwin in https://github.com/feldroy/air/pull/375
* CHORE: Remove docs GH workflow by @pydanny in https://github.com/feldroy/air/pull/365
* TEST: increase test coverage by adding some tests by @mecit-san in https://github.com/feldroy/air/pull/371
* FEAT: Add includes argument to AirForm rendering by @pydanny in https://github.com/feldroy/air/pull/378
* FEAT: Add AirRouter for combining multiple Air apps into with shared middleware and dependencies by @pydanny in https://github.com/feldroy/air/pull/367
* ⬆(deps): Bump ruff from 0.12.10 to 0.12.11 in the python-dependencies group by @dependabot[bot] in https://github.com/feldroy/air/pull/370

## New Contributors
* @Akhilanandateja made their first contribution in https://github.com/feldroy/air/pull/352

**Full Changelog**: https://github.com/feldroy/air/compare/v0.26.0...v0.27.0

# 0.26.0 - 2025-08-27

## Changes by New Contributors

* DOCS: add args doctrings for rest of O, some P tags by @vanessapigwin in https://github.com/feldroy/air/pull/355
* FEAT: Override mvpcss default layout padding by @mecit-san in https://github.com/feldroy/air/pull/358
* REFACTOR: move is_htmx_request to dependencies by @mecit-san in https://github.com/feldroy/air/pull/357

## What's Changed

* FEAT: Benchmark suite with pytest-benchmark by @audreyfeldroy in https://github.com/feldroy/air/pull/345
* FEAT: Implement hx boost in layout functions by @pydanny in https://github.com/feldroy/air/pull/361
* FEAT: Implement RedirectResponse into Air namespace by @WatanabeChika in https://github.com/feldroy/air/pull/337
* FEAT: Create examples directory by @pydanny in https://github.com/feldroy/air/pull/360
* REFACTOR: Remove mkdocs by @pydanny in https://github.com/feldroy/air/pull/364
* REFACTOR: locals cleanup utility and streamline attribute handling by @tallerasaf in https://github.com/feldroy/air/pull/359
* REFACTOR: Move benchmarks to isolated directory by @pydanny in https://github.com/feldroy/air/pull/351
* REFACTOR: Run ruff on code after enabling more rules by @tallerasaf in https://github.com/feldroy/air/pull/346
* TESTS: Add tests for locals_cleanup in tags utils by @audreyfeldroy in https://github.com/feldroy/air/pull/344
* ⬆(deps): Bump pyrefly from 0.29.2 to 0.30.0 in the python-dependencies group by @dependabot[bot] in https://github.com/feldroy/air/pull/362
* ⬆(deps): bump the python-dependencies group with 4 updates by @dependabot[bot] in https://github.com/feldroy/air/pull/341

## New Contributors
* @vanessapigwin made their first contribution in https://github.com/feldroy/air/pull/355
* @mecit-san made their first contribution in https://github.com/feldroy/air/pull/357

**Full Changelog**: https://github.com/feldroy/air/compare/v0.25.2...v0.26.0

# 0.25.2 - 2025-08-23

## What's Changed
* Fix memory leak by @pydanny in https://github.com/feldroy/air/pull/343


**Full Changelog**: https://github.com/feldroy/air/compare/v0.25.1...v0.25.2

# 0.25.1 - 2025-08-23

## What's Changed
* TOOL: PyRefly by @tallerasaf in https://github.com/feldroy/air/pull/318
* BUG: Performance optimizations by @pydanny in https://github.com/feldroy/air/pull/342
* BUG: Add missing autofocus option to AirField by @pydanny in https://github.com/feldroy/air/pull/324
* ⬆(deps): bump ty from 0.0.1a18 to 0.0.1a19 by @dependabot[bot] in https://github.com/feldroy/air/pull/323
* ⬆(deps): bump rust-just from 1.42.3 to 1.42.4 by @dependabot[bot] in https://github.com/feldroy/air/pull/331

**Full Changelog**: https://github.com/feldroy/air/compare/v0.25.0...v0.25.1

# 0.25.0 - 2025-08-22

## What's Changed
* FEAT: Add SessionMiddleware class by @pydanny in https://github.com/feldroy/air/pull/334
* BUG: `attribute_set_to_true=True` converts underscores to dashes by @WatanabeChika in https://github.com/feldroy/air/pull/327
* DOC: Rearrange MVPCSS docs by @pydanny in https://github.com/feldroy/air/pull/330
* ⬆(deps): bump mkdocstrings-python from 1.16.12 to 1.17.0 by @dependabot[bot] in https://github.com/feldroy/air/pull/320
* ⬆(deps): bump pytest-memray from 1.7.0 to 1.8.0 by @dependabot[bot] in https://github.com/feldroy/air/pull/319

## New Contributors
* @WatanabeChika made their first contribution in https://github.com/feldroy/air/pull/327

**Full Changelog**: https://github.com/feldroy/air/compare/v0.24.2...v0.25.0

# 0.24.2 - 2025-08-21

## What's Changed
* BUG: AirForm.validate method returns boolean instead of None by @pydanny in https://github.com/feldroy/air/pull/317
* TOOL: New CI overview by @tallerasaf in https://github.com/feldroy/air/pull/304
* DOC: Docstring improvements by @pydanny in https://github.com/feldroy/air/pull/322
* DOC: Fix document grammar by @pydanny in https://github.com/feldroy/air/pull/328
* ⬆(deps): bump ruff from 0.12.0 to 0.12.9 by @dependabot[bot] in https://github.com/feldroy/air/pull/321
* ⬆(deps): Bump ty from 0.0.1a16 to 0.0.1a18 by @dependabot[bot] in https://github.com/feldroy/air/pull/306
* ⬆(deps): Bump uvicorn from 0.34.3 to 0.35.0 by @dependabot[bot] in https://github.com/feldroy/air/pull/308
* ⬆(deps): Bump types-markdown from 3.8.0.20250415 to 3.8.0.20250809 by @dependabot[bot] in https://github.com/feldroy/air/pull/309

**Full Changelog**: https://github.com/feldroy/air/compare/v0.24.1...v0.24.2


# 0.24.1 - 2025-08-18

## What's Changed

* BUG: Address for_ and as_ args for label and link tags by @pydanny in https://github.com/feldroy/air/pull/312
* BUG: Change AirForm's default_form_widget to use mvp.css by @pydanny in https://github.com/feldroy/air/pull/314
* DOC: Add module level docstrings by @pydanny in https://github.com/feldroy/air/pull/298
* TOOL: Configure Renovate by @renovate[bot] in https://github.com/feldroy/air/pull/300
* TOOL: CI Overview by @tallerasaf in https://github.com/feldroy/air/pull/303
* TOOL: Ruff - 1 by @tallerasaf in https://github.com/feldroy/air/pull/299
* TOOL: Ty by @tallerasaf in https://github.com/feldroy/air/pull/302
* TOOL: Fix dependabot by @tallerasaf in https://github.com/feldroy/air/pull/310
* TOOL: Lint with new rules by @pydanny in https://github.com/feldroy/air/pull/313

**Full Changelog**: https://github.com/feldroy/air/compare/v0.24.0...v0.24.1

# 0.24.0 - 2025-08-17

## What's Changed
* Convert underscores to dashes in app.page method by @pydanny in https://github.com/feldroy/air/pull/293
* Remove last unnecessary type: ignore by @pydanny in https://github.com/feldroy/air/pull/291
* Bring in the new logo to the README by @pydanny in https://github.com/feldroy/air/pull/289
* Docstring improvements by @pydanny in https://github.com/feldroy/air/pull/296
* Document docstring management in CONTRIBUTING.md by @pydanny in https://github.com/feldroy/air/pull/297


**Full Changelog**: https://github.com/feldroy/air/compare/v0.23.0...v0.24.0

# 0.23.0 - 2025-08-15

## Summary

For users, the function signatures on Air SVG tags by @dfundako will make building SVGs much easier for both humans and LLMs. @tallerasaf vastly improves our code coverage build and turns Air poetic with this statement about the wall of badges they have created for us:

> "Each badge gleams like a prayer stitched in code, blessing the dawn of an open-source journey."

## What's Changed

* Add function signatures to Air SVG Tags by @dfundako in https://github.com/feldroy/air/pull/246
* Enhance test coverage enforcement and README badges by @tallerasaf in https://github.com/feldroy/air/pull/288
* Add justfile list recipe by @pydanny in https://github.com/feldroy/air/pull/285
* Improve SVG testing by @pydanny in https://github.com/feldroy/air/pull/286
* Lower coverage threshold to 95% by @pydanny in https://github.com/feldroy/air/pull/287

## New Contributors
* @dfundako made their first contribution in https://github.com/feldroy/air/pull/246

**Full Changelog**: https://github.com/feldroy/air/compare/v0.22.1...v0.23.0

# 0.22.1 - 2025-08-14

## What's Changed
* BUG: Repair the svg import path by @pydanny in https://github.com/feldroy/air/pull/284


**Full Changelog**: https://github.com/feldroy/air/compare/v0.22.0...v0.22.1

# 0.22.0 - 2025-08-14

## What's Changed

This is mostly a CI release, which doesn't affect users of Air itself. Many thanks to @tallerasaf who put most of these together.

* Feat Improved development environment setup by @tallerasaf in https://github.com/feldroy/air/pull/267
* Switch from pytest-rich to pytest-modern by @pydanny in https://github.com/feldroy/air/pull/275
* Full - CI Test Coverage by @tallerasaf in https://github.com/feldroy/air/pull/272
* Improve CI workflows, annotations in the GitHub using GitHub Actions and CI for ubuntu-latest, windows-latest, macos-latest  by @tallerasaf in https://github.com/feldroy/air/pull/279
* BUG: Fix logo in README by @pydanny in https://github.com/feldroy/air/pull/281
* Refine test coverage tasks and commands in Justfile by @tallerasaf in https://github.com/feldroy/air/pull/283

We did get in one feature to Air itself:

* Support MVP.css air.Header tag not being in body by @pydanny in https://github.com/feldroy/air/pull/273

**Full Changelog**: https://github.com/feldroy/air/compare/v0.21.0...v0.22.0

# 0.21.0 - 2025-08-12

## What's Changed

* Use HTML page for 500 errors by @pydanny in https://github.com/feldroy/air/pull/265
* SSEResponse now handles str, Tag, and Any types, with linebreaks handled cleanly by @pydanny in https://github.com/feldroy/air/pull/257
* Improvements to pyproject.toml - by @tallerasaf in https://github.com/feldroy/air/pull/261 and https://github.com/feldroy/air/pull/262
* Refactor tags module into a modular package structure by @tallerasaf in https://github.com/feldroy/air/pull/260
* Convert default exception handlers to use mvpcss for layout by @pydanny in https://github.com/feldroy/air/pull/266
* Set up an "Air" Discord badge by @tallerasaf in https://github.com/feldroy/air/pull/256 and https://github.com/feldroy/air/pull/258
* Add missing env and context processors to JinjaRenderer by @pydanny in https://github.com/feldroy/air/pull/263

* ⬆ Bump actions/checkout from 4 to 5 by @dependabot[bot] in https://github.com/feldroy/air/pull/264


**Full Changelog**: https://github.com/feldroy/air/compare/v0.20.0...v0.21.0

# 0.20.0 - 2025-08-07

## What's Changed
* pyproject.toml to expose a new optional-extras group called standard by @tallerasaf in https://github.com/feldroy/air/pull/252
* Refactor EventStreamResponse to SSEResponse by @pydanny in https://github.com/feldroy/air/pull/249
* Readme improvements by @audreyfeldroy in https://github.com/feldroy/air/pull/245
* Update justfile by @tallerasaf in https://github.com/feldroy/air/pull/244
* Add missing starlette.requests.Request passthrough by @pydanny in https://github.com/feldroy/air/pull/254

**Full Changelog**: https://github.com/feldroy/air/compare/v0.19.0...v0.20.0

# 0.19.0 - 2025-08-04

## What's Changed
* Support for SSE by @pydanny and @audreyfeldroy in https://github.com/feldroy/air/pull/240
* refactor: consolidate tag imports in __init__.py by @tallerasaf in https://github.com/feldroy/air/pull/239
* Fix justfile pdb option by @pydanny in https://github.com/feldroy/air/pull/233
* Remove deprecated Jinja2Renderer by @pydanny in https://github.com/feldroy/air/pull/234
* Begin phasing out content in docs by @pydanny in https://github.com/feldroy/air/pull/235
* Better types for width and height tag attrs by @pydanny in https://github.com/feldroy/air/pull/236
* Clarification of internal tag control name by @pydanny in https://github.com/feldroy/air/pull/237
* Add issue templates for bugs, features, discussions, etc by @pydanny in https://github.com/feldroy/air/pull/238
* Document how to use forms Starlette style by @pydanny in https://github.com/feldroy/air/pull/228

## New Contributors
* @tallerasaf made their first contribution in https://github.com/feldroy/air/pull/239

**Full Changelog**: https://github.com/feldroy/air/compare/v0.18.0...v0.19.0

# 0.18.0 - 2025-08-02

## What's Changed
* Clarify about minimalist core by @audreyfeldroy in https://github.com/feldroy/air/pull/222
* feat: disable docs by default by @kmehran1106 in https://github.com/feldroy/air/pull/221
* Remove CLI and static site generator by @pydanny in https://github.com/feldroy/air/pull/216
* Remove unused dependencies by @pydanny in https://github.com/feldroy/air/pull/217
* Change dependency groups by @pydanny in https://github.com/feldroy/air/pull/218
* Add .vscode to gitignore by @pydanny in https://github.com/feldroy/air/pull/219
* Fine tune justfile by @pydanny in https://github.com/feldroy/air/pull/220

**Full Changelog**: https://github.com/feldroy/air/compare/v0.17.0...v0.18.0

# 0.17.0 - 2025-07-30

## What's Changed
* refactor: removing type ignore  by @kmehran1106 in https://github.com/feldroy/air/pull/213
* Fix tag nav by @pydanny in https://github.com/feldroy/air/pull/207
* Tags and Tag passes through other tags when called directly by @pydanny in https://github.com/feldroy/air/pull/210
* Remove the HTML to Air Tag utility by @pydanny in https://github.com/feldroy/air/pull/215

## New Contributors
* @kmehran1106 made their first contribution in https://github.com/feldroy/air/pull/213

**Full Changelog**: https://github.com/feldroy/air/compare/v0.16.0...v0.17.0


# 0.16.0 - 2025-07-28

## What's Changed
* Rename Jinja2Renderer to JinjaRenderer by @pydanny in https://github.com/feldroy/air/pull/204
* Autorender tags in JinjaRender by @pydanny in https://github.com/feldroy/air/pull/205
* Document tags starting with I by @pydanny in https://github.com/feldroy/air/pull/189
* Layouts concepts by @Isaac-Flath in https://github.com/feldroy/air/pull/192
* Document the L tags by @pydanny in https://github.com/feldroy/air/pull/194
* Add in chart example by @pydanny in https://github.com/feldroy/air/pull/197
* Document Mark and Menu tags by @pydanny in https://github.com/feldroy/air/pull/198
* More docs for tags by @pydanny in https://github.com/feldroy/air/pull/199
* Type args and kwargs in tags and bump ty version by @pydanny in https://github.com/feldroy/air/pull/200
* Refactor tag docs by @pydanny in https://github.com/feldroy/air/pull/201

**Full Changelog**: https://github.com/feldroy/air/compare/v0.15.0...v0.16.0

# 0.15.0 - 2025-07-22


## What's Changed
* Add type hints for tags with attributes by @Isaac-Flath in https://github.com/feldroy/air/pull/143
* Replace Makefile with justfile by @audreyfeldroy in https://github.com/feldroy/air/pull/184
* AirField args now include all of Pydantic Field args by @pydanny in https://github.com/feldroy/air/pull/167
* Change RawHTML to Raw by @pydanny in https://github.com/feldroy/air/pull/169
* Document Tag args to button by @pydanny in https://github.com/feldroy/air/pull/173
* Tests for background task by @pydanny in https://github.com/feldroy/air/pull/175
* Improve tests for forms by @pydanny in https://github.com/feldroy/air/pull/176
* Document tags and clean up tag types by @pydanny in https://github.com/feldroy/air/pull/177
* Undo Optional[str] by @pydanny in https://github.com/feldroy/air/pull/178
* Switch to use uv run for python options in Make by @pydanny in https://github.com/feldroy/air/pull/179
* Improve test coverage for tags.py by @pydanny in https://github.com/feldroy/air/pull/180
* Document more tags by @pydanny in https://github.com/feldroy/air/pull/181
* Single source of version by @pydanny in https://github.com/feldroy/air/pull/188


**Full Changelog**: https://github.com/feldroy/air/compare/v0.14.2...v0.15.0


# 0.14.2 - 2025-07-18

## What's Changed
* Create AirField wrapper for Pydantic Field  by @pydanny in https://github.com/feldroy/air/pull/164
* Update what is claimed for Python support by @pydanny in https://github.com/feldroy/air/pull/156
* Add support for returning multiple children in Air Tags from views by @pydanny in https://github.com/feldroy/air/pull/158
* Add types of contribution section to CONTRIBUTING.md by @pydanny in https://github.com/feldroy/air/pull/160
* Add jinja to the alternatives page by @pydanny in https://github.com/feldroy/air/pull/161
* Add default HTML page for 404 errors by @pydanny in https://github.com/feldroy/air/pull/162

**Full Changelog**: https://github.com/feldroy/air/compare/v0.13.0...v0.14.2


# 0.13.0 - 2025-07-17

## What's Changed
* Implement FastAPI background tasks by @pydanny in https://github.com/feldroy/air/pull/127
* Pass through requests by @pydanny in https://github.com/feldroy/air/pull/138
* Add function signature for Tag A by @pydanny in https://github.com/feldroy/air/pull/140
* Passthru all the responses by @pydanny in https://github.com/feldroy/air/pull/141
* Pass through starlette staticfiles by @pydanny in https://github.com/feldroy/air/pull/144
* Stringify/escape unsupported tag children so 500 errors aren't thrown on tag children type failures by @pydanny in https://github.com/feldroy/air/pull/147
* Explaining how to use Jinja with Air Tags by @pydanny in https://github.com/feldroy/air/pull/148
* Add boolean attributes to Air Tags plus improve docs by @pydanny in https://github.com/feldroy/air/pull/152
* Properly make self-closing tags like input and img self-close by @pydanny in https://github.com/feldroy/air/pull/154
* Switch from mypy to ty by @pydanny in https://github.com/feldroy/air/pull/155


**Full Changelog**: https://github.com/feldroy/air/compare/v0.12.0...v0.13.0

# 0.11.0 - 2025-07-12


## New Features
* Update .editorconfig for improved file handling by @audreyfeldroy in https://github.com/feldroy/air/pull/121
* Added Form rendering by @pydanny in https://github.com/feldroy/air/pull/120
* Added `html_to_airtags` function, converts HTML to Air Tags by @pydanny in https://github.com/feldroy/air/pull/125


## Documentation improvements
* Reorder member order in object docs by @pydanny in https://github.com/feldroy/air/pull/116
* Documentation on how to escape HTML by @pydanny in https://github.com/feldroy/air/pull/108
* Update project description in README and pyproject.toml by @audreyfeldroy in https://github.com/feldroy/air/pull/118
* Update CONTRIBUTING.md with docs, tests, and troubleshooting by @audreyfeldroy in https://github.com/feldroy/air/pull/119

**Full Changelog**: https://github.com/feldroy/air/compare/v0.11.0...v0.12.0

# 0.11.0 - 2025-07-09

## What's Changed

* Add layouts module with pico example by @audreyfeldroy and @pydanny in https://github.com/feldroy/air/pull/87
* Restructure docs by @pydanny in https://github.com/feldroy/air/pull/100
* Add README badges and refactor README by @pydanny in https://github.com/feldroy/air/pull/101
* Documentation improvements by @pydanny in https://github.com/feldroy/air/pull/102
* Add logo by @audreyfeldroy and @pydanny in https://github.com/feldroy/air/pull/103
* Document how `page` works with index by @pydanny in https://github.com/feldroy/air/pull/105
* For Jinja rendering, change "render" var name to "jinja" by @pydanny in https://github.com/feldroy/air/pull/106
* Restructure docs yet again by @pydanny in https://github.com/feldroy/air/pull/109
* Add MVP.css and change `pico()` function name to `picocss()` by @audreyfeldroy and @pydanny in https://github.com/feldroy/air/pull/114
* Refactor HTML attr cleanup function by @audreyfeldroy and @pydanny in https://github.com/feldroy/air/pull/115


**Full Changelog**: https://github.com/feldroy/air/compare/v0.10.0...v0.11.0

# 0.10.0 - 2025-07-07

## What's Changed

* Remove the ability to change the Air default response class by @pydanny in https://github.com/feldroy/air/pull/79
* Add kwargs to Jinja2Renderer by @pydanny in https://github.com/feldroy/air/pull/84
* About section by @pydanny in https://github.com/feldroy/air/pull/73
* Sort imports and add import sorting to clean command by @pydanny in https://github.com/feldroy/air/pull/90
* Added form validation via Air Forms by @pydanny in https://github.com/feldroy/air/pull/81
* Support mkdoc-material admonitions by @pydanny in https://github.com/feldroy/air/pull/95
* Allow non-escaped code through Style and Script tags by @Isaac-Flath and @pydanny in https://github.com/feldroy/air/pull/96

**Full Changelog**: https://github.com/feldroy/air/compare/v0.9.0...v0.10.0

# 0.9.0 - 2025-07-03

## What's Changed

* Add AirResponse and get-only `app.page` route decorator shortcut by @pydanny in https://github.com/feldroy/air/pull/76

**Full Changelog**: https://github.com/feldroy/air/compare/v0.8.0...v0.9.0

# 0.8.0 - 2025-06-29

## What's Changed
* Remove headers arg from Html tag by @pydanny in https://github.com/feldroy/air/pull/68
* Escape strings in tags  by @pydanny in https://github.com/feldroy/air/pull/72
* Add GH action to release on PyPI by @pydanny in https://github.com/feldroy/air/pull/74


**Full Changelog**: https://github.com/feldroy/air/compare/v0.7.0...v0.8.0

# 0.7.0 - 2025-06-28

## What's Changed
* Api docs by @Isaac-Flath in https://github.com/feldroy/air/pull/47
* Motto grammar fix by @pydanny in https://github.com/feldroy/air/pull/49
* Add missing function signatures to `application.Air` by @pydanny in https://github.com/feldroy/air/pull/52
* Add doc nav improvements and API Ref index by @pydanny in https://github.com/feldroy/air/pull/50
* Add missing applications ref by @pydanny in https://github.com/feldroy/air/pull/53
* Explain air tags by @pydanny in https://github.com/feldroy/air/pull/62
* Convert `Tag.children` property to for loop and fix bug by @pydanny in https://github.com/feldroy/air/pull/64
* Dependency upgrade by @pydanny in https://github.com/feldroy/air/pull/67


**Full Changelog**: https://github.com/feldroy/air/compare/v0.6.0...v0.7.0

# 0.6.0 - 2025-06-26

## What's Changed
* Add run instructions to quickstart docs by @Isaac-Flath in https://github.com/feldroy/air/pull/45
* Create applications.Air wrapper for fastapi.FastAPI by @pydanny in https://github.com/feldroy/air/pull/46

Minimal apps now look like this:

```python
import air

app = air.Air()

@app.get("/")
async def index():
    return air.Html(air.H1("Hello, world!", style="color: blue;"))
```

## New Contributors
* @Isaac-Flath made their first contribution in https://github.com/feldroy/air/pull/45

**Full Changelog**: https://github.com/feldroy/air/compare/v0.5.0...v0.6.0

# 0.5.0 - 2025-06-25

## What's Changed
* Merged in fastapi-tags by @pydanny in https://github.com/feldroy/air/pull/36
* Improve install docs by @audreyfeldroy in https://github.com/feldroy/air/pull/39
* Shortcut renderer for jinja2 by @pydanny in https://github.com/feldroy/air/pull/40
* Document how to remove HTML results from API docs by @pydanny in https://github.com/feldroy/air/pull/41
* Quick start tutorial by @pydanny in https://github.com/feldroy/air/pull/42


**Full Changelog**: https://github.com/feldroy/air/compare/v0.4.0...v0.5.0

# 0.4.0 - 2025-06-24

## What's Changed
* Create a GitHub Actions workflow for running tests with Tox by @audreyfeldroy in https://github.com/feldroy/air/pull/8
* Convert to vanilla uv by @pydanny in https://github.com/feldroy/air/pull/12
* Upgrade checks to use UV by @pydanny in https://github.com/feldroy/air/pull/14
* docs: fix link to audrey.feldroy.com in README by @johnfraney in https://github.com/feldroy/air/pull/15
* Convert CLI to use typer by @pydanny in https://github.com/feldroy/air/pull/17
* Add fastapi-tags for Python classes to render HTML by @pydanny in https://github.com/feldroy/air/pull/16
* Add docs by @pydanny in https://github.com/feldroy/air/pull/18
* Improve readme and move static site generation to docs by @pydanny in https://github.com/feldroy/air/pull/23
* Various repo cleanup chores by @pydanny in https://github.com/feldroy/air/pull/24

## New Contributors
* @audreyfeldroy made their first contribution in https://github.com/feldroy/air/pull/8
* @pydanny made their first contribution in https://github.com/feldroy/air/pull/12
* @johnfraney made their first contribution in https://github.com/feldroy/air/pull/15

**Full Changelog**: https://github.com/feldroy/air/compare/0.3.0...v0.4.0


# 0.3.0 - 2024-07-07

* Static site generation
* Template inheritance
* Markdown support
