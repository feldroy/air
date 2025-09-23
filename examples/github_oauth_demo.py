"""
A demonstration of the basic auth capabilities of AIR.
This little app demonstrates how to use AIR for authentication.
Run:

    uv sync --all-extras --no-extra standard
    uv run --env-file .env fastapi dev github_oauth_demo.py
"""

from datetime import datetime
from os import environ

from rich import print

import air

database = {}


async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
    access_token = token["access_token"]
    print(access_token)
    if access_token in database:
        database[access_token]["updated_at"] = datetime.now()
    else:
        database[access_token] = token
        database[access_token]["created_at"] = datetime.now()
        database[access_token]["updated_at"] = datetime.now()
        database[access_token]["access_token"] = access_token
    request.session["github_access_token"] = access_token
    print(database)


github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
    github_client_id=environ["GITHUB_CLIENT_ID"],
    github_client_secret=environ["GITHUB_CLIENT_SECRET"],
    github_process_callable=github_process_callable,
    login_redirect_to="/",
)


app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
app.include_router(github_oauth_client.router)


database = {}


@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1("GitHub OAuth Login Demo"),
        air.P(air.A("Login to Github", href="/account/github/login")),
        air.P(request.session.get("github_access_token", "Not authenticated yet")),
    )
