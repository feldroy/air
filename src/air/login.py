from typing import Any, Callable
from urllib.parse import quote

from fastapi import HTTPException, Depends
from .requests import Request
from .responses import RedirectResponse


class LoginManager:
    """User login management for air routes

    This class provides login, logout, and dependency-based authentication
    similar to Flask-Login and Microdot. It stores the user ID
    in the session and redirects unauthenticated users to a login page.

    Example:

        from fastapi import FastAPI, Depends
        import air

        app = air.Air()
        app.add_middleware(air.SessionMiddleware, secret_key="change-me")

        manager = air.LoginManager(login_url="/login")

        # Register user loader callback
        @manager.user_loader
        def load_user(user_id: str):
            # Replace with real DB lookup
            if user_id == "42":
                return {"id": 42, "name": "Alice"}
            return None

        @app.get("/login")
        async def login_page():
            # Example login page
            return air.layouts.mvpcss(
                air.H1("Login"),
                air.Form(action="/do-login", method="post")(
                    air.Input(type="text", name="username"),
                    air.Input(type="password", name="password"),
                    air.Button("Login")
                ),
            )

        @app.post("/do-login")
        async def do_login(request: Request):
            # Example login logic
            form = await request.form()
            user_id = "42"  # hardcoded for example
            return await manager.login_user(request, user_id, redirect_url="/")

        @app.get("/")
        async def index(user=Depends(manager)):
            # If user not logged in, they get redirected
            return air.layouts.mvpcss(
                air.H1(f"Hello {user['name']}!"),
                air.A("Logout", href="/logout")
            )
    """

    USER_KEY = "_user_id"

    def __init__(self, login_url: str = '/login'):
        """Initialize the login manager.

        Args:
            login_url: The URL path to redirect unauthenticated users.
                       Defaults to ``/login``.
        """
        self.login_url = login_url
        self._load_user: Callable[[str], Any] | None = None

    def user_loader(self, callback: Callable[[str], Any]):
        """Register a function to load a user by ID.

        The callback should take a user ID string and return a user object,
        or ``None`` if the user does not exist.
        """
        self._load_user = callback

    async def login_user(self, request: Request, user_id: str, redirect_url: str = '/'):
        """Log a user in and redirect.

        Args:
            request: The current request.
            user_id: The ID of the user to store in the session.
            redirect_url: Default redirect path if no ``next`` parameter
                          is present in the request. Defaults to ``/``.

        Returns:
            RedirectResponse to the next URL or the default redirect.
        """
        session = self._get_session(request)
        session[self.USER_KEY] = user_id

        next_url = request.query_params.get('next', redirect_url)
        if not next_url.startswith('/'):
            next_url = redirect_url
        return RedirectResponse(next_url, status_code=302)

    async def logout_user(self, request: Request):
        """Log out the current user by clearing the session."""
        session = self._get_session(request)
        session.pop(self.USER_KEY, None)

    def _get_session(self, request: Request) -> dict:
        """Return the session dict or raise error if SessionMiddleware is missing."""
        assert "session" in request.scope, "SessionMiddleware must be installed to use LoginManager"
        return request.session

    def _redirect_to_login(self, request: Request):
        """Raise an HTTPException redirecting to the login page.

        The current request URL is added as a ``next`` parameter.
        """
        raise HTTPException(
            status_code=302,
            headers={
                "Location": f"{self.login_url}?next={quote(str(request.url.path))}"
            }
        )

    async def __call__(self, request: Request) -> Any:
        """Dependency entry point for retrieving the current user.

        This makes ``LoginManager`` usable with ``Depends`` in FastAPI.

        Args:
            request: The incoming request, provided automatically by FastAPI.

        Returns:
            The user object loaded by the registered ``user_loader``.

        Raises:
            HTTPException: Redirect to the login page if no user is found.
        """
        session = self._get_session(request)
        user_id = session.get(self.USER_KEY)
        if not user_id:
            self._redirect_to_login(request)

        user = self._load_user(user_id)
        if not user:
            self._redirect_to_login(request)

        return user
