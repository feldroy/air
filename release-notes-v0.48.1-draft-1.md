## Air 0.48.1: HEAD requests work on every route

Air sites now respond correctly to HTTP HEAD requests. If you use Facebook link previews, Twitter cards, Slack unfurls, or uptime monitors that send HEAD, they work on Air out of the box.

```
uv tool upgrade air
```

### What's fixed

- **HTTP HEAD requests return 200 instead of 405.** Every GET route (`@app.page`, `@app.get`, `@router.page`, `@router.get`) now responds to HEAD with the correct status, headers, and empty body. FastAPI's routing layer has never added HEAD to GET routes the way Starlette does. Air now restores that behavior in its own route class. ([#1123](https://github.com/feldroy/air/pull/1123))

- **Cleaner linter config for dependency injection.** Air's `ruff.toml` now lists its immutable function calls (`Depends`, `Query`, `Header`, etc.) in `extend-immutable-calls`, removing the need for `noqa: B008` comments throughout the codebase. ([#1109](https://github.com/feldroy/air/pull/1109))

### Contributors

[@audreyfeldroy](https://github.com/audreyfeldroy) (Audrey M. Roy Greenfeld) traced the HEAD bug to FastAPI's route initialization and wrote the fix.

[@pydanny](https://github.com/pydanny) (Daniel Roy Greenfeld) cleaned up the doc build.

Thanks to [@francisdbillones](https://github.com/francisdbillones) (Francis Billones) for adding `extend-immutable-calls` to the ruff config and cleaning up the `noqa` comments.
