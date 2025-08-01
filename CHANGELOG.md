# Changelog

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


## Documentaton improvements
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
