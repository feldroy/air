from unittest.mock import AsyncMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

import air
from air import auth
from air.auth import GitHubOAuthRouterFactory


def test_app_has_session() -> None:
    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    github_oauth_client = auth.GitHubOAuthClientFactory(
        github_client_id="CLIENT_ID",
        github_client_secret="CLIENT_SECRET",
        github_process_callable=github_process_callable,
        login_redirect_to="/",
    )

    app = air.Air()
    app.include_router(github_oauth_client.router)

    client = TestClient(app)
    with pytest.raises(AssertionError):
        client.get("/account/github/login")


def test_github_login_route() -> None:
    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    github_oauth_client = auth.GitHubOAuthClientFactory(
        github_client_id="CLIENT_ID",
        github_client_secret="CLIENT_SECRET",
        github_process_callable=github_process_callable,
        login_redirect_to="/",
    )

    app = air.Air()
    app.add_middleware(air.SessionMiddleware, secret_key="insecure")
    app.include_router(github_oauth_client.router)

    client = TestClient(app)
    response = client.get("/account/github/login")

    assert response.history[0].status_code == 302
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response._request.url.host == "github.com"  # ty:ignore[possibly-unbound-attribute]
    assert response._request.url.path == "/login/oauth/authorize"  # ty:ignore[possibly-unbound-attribute]


def test_github_callback_route() -> None:
    test_token = {"access_token": "test_token"}

    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    with patch("air.ext.auth.OAuth") as mock_oauth_class:
        mock_oauth = mock_oauth_class.return_value
        mock_github_client = AsyncMock()
        mock_github_client.authorize_access_token = AsyncMock(return_value=test_token)
        mock_oauth.create_client.return_value = mock_github_client

        github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
            github_client_id="CLIENT_ID",
            github_client_secret="CLIENT_SECRET",
            github_process_callable=github_process_callable,
            login_redirect_to="/",
        )
    github_oauth_router = auth.GitHubOAuthRouterFactory(
        github_client_id="CLIENT_ID",
        github_client_secret="CLIENT_SECRET",
        github_process_callable=github_process_callable,
        login_redirect_to="/",
    )

    app = air.Air()
    app.add_middleware(air.SessionMiddleware, secret_key="insecure")
    app.include_router(github_oauth_client.router)

    @app.page
    def index():
        return air.H1("Hello, world")

    client = TestClient(app)

    login_resp = client.get("/account/github/login", follow_redirects=False)
    assert login_resp.status_code in (302, 307)
    location = login_resp.headers["location"]

    # Extract the generated `state` from the GitHub redirect URL
    state = parse_qs(urlparse(location).query)["state"][0]

    with patch(
        "authlib.integrations.starlette_client.apps.StarletteOAuth2App.authorize_access_token",
        new=AsyncMock(return_value=test_token),
    ):
        response = client.get(f"/account/github/callback?code=dummy&state={state}")

    # Followed redirect back to "/"
    assert response.history[0].status_code == 303
    assert response.status_code == 200
    assert "Hello" in response.text
