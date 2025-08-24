"""Example demonstrating BasicAuthBackend usage in Air framework."""

from starlette.middleware.authentication import AuthenticationMiddleware

import air


# Simple credential verification function
def verify_credentials(username: str, password: str) -> bool:
    """Verify user credentials.

    In a real application, you would check against a database
    or other secure credential store.
    """
    # Simple hardcoded users for demo
    users = {"admin": "secret", "user": "password", "demo": "demo123"}
    return users.get(username) == password


# Create the authentication backend
auth_backend = air.BasicAuthBackend(verify_credentials)

# Create Air application
app = air.Air()

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware, backend=auth_backend)


@app.page
async def index(request: air.Request):
    """Public homepage."""
    if request.user.is_authenticated:
        return air.layouts.mvpcss(
            air.H1("Welcome!"),
            air.P(f"Hello, {request.user.display_name}!"),
            air.P(air.A("Go to protected area", href="/protected")),
            air.P(air.A("Logout", href="/logout")),
        )
    else:
        return air.layouts.mvpcss(
            air.H1("Air Basic Auth Example"),
            air.P("You are not logged in."),
            air.P("Try visiting ", air.A("/protected", href="/protected"), " to see basic auth in action."),
            air.Hr(),
            air.H3("Test Credentials:"),
            air.Ul(
                air.Li("Username: admin, Password: secret"),
                air.Li("Username: user, Password: password"),
                air.Li("Username: demo, Password: demo123"),
            ),
        )


@app.page
async def protected(request: air.Request):
    """Protected page that requires authentication."""
    if not request.user.is_authenticated:
        # Return 401 Unauthorized with WWW-Authenticate header
        headers = {"WWW-Authenticate": 'Basic realm="Air App"'}
        return air.responses.Response("Authentication required", status_code=401, headers=headers)

    return air.layouts.mvpcss(
        air.H1("Protected Area"),
        air.P(f"Welcome to the protected area, {request.user.display_name}!"),
        air.P("This page requires authentication to view."),
        air.P("Your authentication scopes: ", str(list(request.auth.scopes))),
        air.P(air.A("Back to home", href="/")),
    )


@app.page
async def admin(request: air.Request):
    """Admin-only page (demo of role-based access)."""
    if not request.user.is_authenticated:
        headers = {"WWW-Authenticate": 'Basic realm="Air App"'}
        return air.responses.Response("Authentication required", status_code=401, headers=headers)

    # Simple role check
    if request.user.display_name != "admin":
        return air.responses.Response("Access forbidden - Admin only", status_code=403)

    return air.layouts.mvpcss(
        air.H1("Admin Panel"),
        air.P("This is the admin-only area."),
        air.P("Only the 'admin' user can access this page."),
        air.P(air.A("Back to home", href="/")),
    )


@app.page
async def logout(request: air.Request):
    """Logout page - instructs user how to log out of basic auth."""
    return air.layouts.mvpcss(
        air.H1("Logout"),
        air.P("With Basic Authentication, logout must be handled by the browser."),
        air.P("Most browsers will forget credentials when you:"),
        air.Ul(
            air.Li("Close all browser windows/tabs"),
            air.Li("Clear browser cache/cookies"),
            air.Li("Use incognito/private browsing mode"),
        ),
        air.P(air.A("Back to home", href="/")),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
