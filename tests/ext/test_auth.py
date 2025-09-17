import pytest
from fastapi.testclient import TestClient

import air


def test_app_has_session():
    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    github_oauth_router = air.ext.GitHubOAuthRouterFactory(
        github_client_id="CLIENT_ID",
        github_client_secret="CLIENT_SECRET",
        github_process_callable=github_process_callable,
        login_redirect_to="/",
    )

    app = air.Air()
    app.include_router(github_oauth_router)

    client = TestClient(app)
    with pytest.raises(AssertionError):
        client.get("/account/github/login")


def test_github_login_route():
    async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
        pass

    github_oauth_router = air.ext.GitHubOAuthRouterFactory(
        github_client_id="CLIENT_ID",
        github_client_secret="CLIENT_SECRET",
        github_process_callable=github_process_callable,
        login_redirect_to="/",
    )

    app = air.Air()
    app.add_middleware(air.SessionMiddleware, secret_key="insecure")
    app.include_router(github_oauth_router)

    client = TestClient(app)
    response = client.get("/account/github/login")

    assert response.history[0].status_code == 302
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response._request.url.host == "github.com"  # ty:ignore[possibly-unbound-attribute]
    assert response._request.url.path == "/login/oauth/authorize"  # ty:ignore[possibly-unbound-attribute]
