from os import getenv

from authlib.integrations.starlette_client import OAuth
from rich import print

from ...exceptions import HTTPException
from ...requests import Request
from ...responses import RedirectResponse
from ...routing import AirRouter



GITHUB_CLIENT_ID:str = getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET: str = getenv("GITHUB_CLIENT_SECRET")

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

user_router = AirRouter()
"""Router for GitHub auth that includes the views listed below this router:
"""


def check_session_middleware(request: Request):
    if not hasattr(request, 'session'):
        raise HTTPException(
            status_code=500, 
            detail="Session middleware not installed"
        )


@user_router.page
async def login_github(request: Request):
    redirect_uri = request.url_for("auth_github")
    return await github.authorize_redirect(request, redirect_uri)


@user_router.page
async def auth_github(request: Request):
    token = await oauth.github.authorize_access_token(request)
    print(token)
    # TODO save the github access token for the user
    github_access_token = token["access_token"]
    request.session["github_access_token"] = github_access_token
    return RedirectResponse("/")
