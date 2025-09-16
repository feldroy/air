"""
A demonstration of the basic auth capabilities of AIR.

This little app demonstrates how to AIR for authentication.

Run:
    `uv sync --all-extras --no-extra standard`
    `fastapi dev examples/auth_demo.py`
"""

import air

auth_router = air.ext.auth


app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
app.include_router(air.ext.auth.auth_router)


@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1("GitHub OAuth Login Demo"),
        air.P(air.A("Login to Github", href="/account/github/login")),
        air.P(request.session.get("github_access_token", "Not authenticated yet")),
    )
