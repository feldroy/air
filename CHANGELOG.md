# Changelog

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
