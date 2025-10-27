from collections.abc import Callable

from authlib.integrations.starlette_client import OAuth

from ..requests import Request
from ..responses import RedirectResponse
from ..routing import AirRouter


class GitHubOAuthClientFactory:
    def __init__(
        self,
        github_client_id: str,
        github_client_secret: str,
        github_process_callable: Callable,
        github_redirect_uri: str = "http://localhost:8000/account/github/callback",
        login_redirect_to: str = "/",
        scope: str = "user:email",
    ) -> None:
        """Creates an `air.AirRouter` affiliated with the supplied credentials.

        ARGS:
            github_client_id: The GitHub client ID.
            github_client_secret: The GitHub client secret. Do not include this in your repo, use environment variables!
            github_process_callable: A callable (function, class, or method) that takes three arguments, request, token, and client
            login_redirect_to: The path to send the user to once they have authenticated
            scope: What parts of the GitHub API is accessible

        Example:

            import air
            from os import environ

            app = air.Air()
            app.add_middleware(air.SessionMiddleware, secret_key="change-me")

            async def save_github_token(
                request: air.Request, token: dict, client: Any
            ) -> None:
                "Save the GitHub user's login name to an SQL database."
                resp = await client.get('user', token=token)
                profile = resp.json()
                github_login = profile.get('login')

                async_session = await air.ext.sqlmodel.create_async_session()
                async with async_session() as session:
                    # check if access_token is in database
                    stmt = select(User).where(User.github_login==github_login)
                    result = await session.exec(stmt)
                    user = result.one_or_none()
                    if not user:
                        user = User(
                            github_login=github_login, status=UserStatusEnum.active
                        )
                        session.add(user)
                        await session.commit()
                    # Save the token in place to request.session
                    request.session["user"] = dict(
                        github_login=github_login, updated_at=str(datetime.now())
                    )

            github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
                github_client_id=environ['GITHUB_CLIENT_ID'],
                github_client_secret=environ['GITHUB_CLIENT_SECRET'],
                github_process_callable=save_github_token,
                github_redirect_uri=environ['GITHUB_REDIRECT_URI']
                login_redirect_to='/dashboard',
                scope='read:profile user:email'
            )
            app.include_router(github_oauth_client.router)
        """
        self.github_redirect_uri = github_redirect_uri
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
            client_kwargs={"scope": scope},
        )
        self.client = oauth.create_client("github")

        @router.get("/account/github/login")
        async def github_login(request: Request):
            assert hasattr(request, "session")
            return await self.client.authorize_redirect(request, self.github_redirect_uri)

        @router.get("/account/github/callback")
        async def github_callback(request: Request):
            assert hasattr(request, "session")
            token = await self.client.authorize_access_token(request)

            await github_process_callable(request=request, token=token, client=self.client)

            return RedirectResponse(login_redirect_to)

        self.router = router
