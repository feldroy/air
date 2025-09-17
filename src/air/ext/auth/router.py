from os import getenv

from authlib.integrations.starlette_client import OAuth

from ...exceptions import HTTPException
from ...requests import Request
from ...responses import RedirectResponse
from ...routing import AirRouter

GITHUB_CLIENT_ID: str = getenv("GITHUB_CLIENT_ID", "")
"""Provided by GitHub in their OAuth app configuration screen."""

GITHUB_CLIENT_SECRET: str = getenv("GITHUB_CLIENT_SECRET", "")
"""Secret key value provided by GitHub in their OAuth app configuration screen. Only displayed once."""

AUTH_LOGIN_REDIRECT_TO: str = getenv("AUTH_LOGIN_REDIRECT_TO", "/")
"""Where users go after they have been authenticated."""

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


def check_session_middleware(request: Request):
    if not hasattr(request, "session"):
        raise HTTPException(status_code=500, detail="Session middleware not installed")


@auth_router.get("/account/github/login")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await github.authorize_redirect(request, redirect_uri)  # pyrefly: ignore[missing-attribute]


@auth_router.get("/account/github/callback")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)  # pyrefly: ignore[missing-attribute]
    # TODO save the github access token for the user
    # Use a function defined somewhere as a setting
    github_access_token = token["access_token"]
    request.session["github_access_token"] = github_access_token
    return RedirectResponse(AUTH_LOGIN_REDIRECT_TO)
