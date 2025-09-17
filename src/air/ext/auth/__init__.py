"""
Implementing the User model with GitHub OAuth.

!!! note "Coming Soon: More authentication methods!"

    We chose GitHub OAuth because configuring it is straightforward. Our plan is to expand to other OAuth providers as well as other registration and authentication mechanisms.

# Setup

## Step 1: Configuration

First, set these three environment variables based on your GitHub app configuration:

- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET
- AUTH_LOGIN_REDIRECT_TO

## Step 2: Bring in session middleware and auth routes

```python
import air

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
app.include_router(air.ext.auth.auth_router)
```

## Step 3: Code a link to the login


```python
@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1("GitHub OAuth Login Demo"),
        air.P(air.A("Login to Github", href="/account/github/login")),
        air.P(request.session.get("github_access_token", "Not authenticated yet")),
    )
```

Try it out!

---

# API

"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...requests import Request
    from ...responses import Response
    from ...routing import AirRouter

    auth_router: AirRouter
    AUTH_LOGIN_REDIRECT_TO: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    async def github_callback(request: Request) -> Response: ...
    async def github_login(request: Request) -> Response: ...


try:
    from .router import (
        AUTH_LOGIN_REDIRECT_TO as AUTH_LOGIN_REDIRECT_TO,
        GITHUB_CLIENT_ID as GITHUB_CLIENT_ID,
        GITHUB_CLIENT_SECRET as GITHUB_CLIENT_SECRET,
        auth_router as auth_router,
        github_callback as github_callback,
        github_login as github_login,
    )
except ImportError:  # pragma: no cover
    msg = "air.ext.auth requires installing the authlib, sqlmodel, and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    def __getattr__(name: str) -> Any:
        return NotImportable()
