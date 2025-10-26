from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

import air


def test_app_has_session() -> None:
    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
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

    github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
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
    assert response._request.url.host == "github.com"
    assert response._request.url.path == "/login/oauth/authorize"


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

        app = air.Air()
        app.add_middleware(air.SessionMiddleware, secret_key="insecure")
        app.include_router(github_oauth_client.router)

        @app.page
        def index():
            return air.H1("Hello, world")

        client = TestClient(app)

        response = client.get("/account/github/callback")

        assert response.history[0].status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.status_code == 200
        assert "Hello" in response.text
