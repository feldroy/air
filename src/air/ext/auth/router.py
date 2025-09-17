from contextlib import suppress
from datetime import datetime
from os import getenv

from authlib.integrations.starlette_client import OAuth

from ...exceptions import HTTPException
from ...requests import Request
from ...responses import RedirectResponse
from ...routing import AirRouter

with suppress(ImportError):
    from rich import print

GITHUB_CLIENT_ID: str = getenv("GITHUB_CLIENT_ID", "")
"""Provided by GitHub in their OAuth app configuration screen."""

GITHUB_CLIENT_SECRET: str = getenv("GITHUB_CLIENT_SECRET", "")
"""Secret key value provided by GitHub in their OAuth app configuration screen. Only displayed once."""

AUTH_LOGIN_REDIRECT_TO: str = getenv("AUTH_LOGIN_REDIRECT_TO", "/")
"""Where users go after they have been authenticated. Defaults to '/'."""

oauth = OAuth()
oauth.register(
    name="github",
    client_id=getenv("GITHUB_CLIENT_ID"),
    client_secret=getenv("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
github = oauth.create_client("github")

auth_router = AirRouter()
"""Router for GitHub auth that includes the views listed below this router.

Note: Doesn't yet work with the `prefix` keyword argument in declaring routers.

```python
import air

auth_router = air.ext.auth


app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
app.include_router(air.ext.auth.auth_router)
```
"""

database = {}


async def add_user_to_session(request: Request, token: dict) -> None:
    access_token = token["access_token"]
    print(token)
    if access_token in database:
        database[access_token]["updated_at"] = datetime.now()
    else:
        database[access_token] = token
        database[access_token]["created_at"] = datetime.now()
        database[access_token]["updated_at"] = datetime.now()
        database[access_token]["access_token"] = access_token
    print(database)


def _check_session_middleware(request: Request):
    """TODO: change out for a dependency"""
    if not hasattr(request, "session"):
        raise HTTPException(status_code=500, detail="Session middleware not installed.")


@auth_router.get("/account/github/login")
async def github_login(request: Request):
    _check_session_middleware(request)
    redirect_uri = request.url_for("github_callback")
    return await github.authorize_redirect(request, redirect_uri)


@auth_router.get("/account/github/callback")
async def github_callback(request: Request):
    _check_session_middleware(request)
    token = await oauth.github.authorize_access_token(request)

    # TODO make this configurable via an environment variable or some other method
    await add_user_to_session(request=request, token=token)

    return RedirectResponse(AUTH_LOGIN_REDIRECT_TO)
