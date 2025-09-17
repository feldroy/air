from collections.abc import Callable

from authlib.integrations.starlette_client import OAuth

from ..exceptions import HTTPException
from ..requests import Request
from ..responses import RedirectResponse
from ..routing import AirRouter


def _check_session_middleware(request: Request):
    """Confirms the session middleware is installed, raises a 500 exception if it is not.

    TODO: Turn into a dependency, put in the dependencies.py module as `check_session_middleware`
    """
    if not hasattr(request, "session"):
        raise HTTPException(status_code=500, detail="Session middleware not installed.")


def GitHubOAuthRouterFactory(
    github_client_id: str, github_client_secret: str, github_process_callable: Callable, login_redirect_to: str = "/"
) -> AirRouter:
    router = AirRouter()
    oauth = OAuth()
    oauth.register(
        name="github",
        client_id=github_client_id,
        client_secret=github_client_secret,
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email"},
    )
    github = oauth.create_client("github")

    @router.get("/account/github/login")
    async def github_login(request: Request):
        _check_session_middleware(request)
        redirect_uri = request.url_for("github_callback")
        return await github.authorize_redirect(request, redirect_uri)

    @router.get("/account/github/callback")
    async def github_callback(request: Request):
        _check_session_middleware(request)
        token = await oauth.github.authorize_access_token(request)

        await github_process_callable(request=request, token=token)

        return RedirectResponse(login_redirect_to)

    return router
