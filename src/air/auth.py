"""Authentication backends and utilities for Air framework.

Provides authentication functionality similar to Starlette's authentication system,
adapted for the Air framework's conventions and patterns.
"""

import base64
import binascii
from typing import Optional, Tuple

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import HTTPConnection


class BasicAuthBackend(AuthenticationBackend):
    """HTTP Basic Authentication backend for Air.

    Authenticates users using the HTTP Basic Authentication scheme.
    Extracts username and password from the Authorization header
    and validates credentials.

    Example:

        import air
        from air.auth import BasicAuthBackend
        from starlette.middleware.authentication import AuthenticationMiddleware

        def verify_credentials(username: str, password: str) -> bool:
            # Implement your credential verification logic
            return username == "admin" and password == "secret"

        backend = BasicAuthBackend(verify_credentials)
        app = air.Air()
        app.add_middleware(AuthenticationMiddleware, backend=backend)

        @app.page
        async def protected(request: air.Request):
            if not request.user.is_authenticated:
                return air.responses.Response("Unauthorized", status_code=401)
            return air.H1(f"Hello, {request.user.display_name}!")
    """

    def __init__(self, verify_credentials: Optional[callable] = None):
        """Initialize BasicAuthBackend.

        Args:
            verify_credentials: Optional callable that takes (username, password)
                              and returns True if credentials are valid.
                              If None, all credentials are accepted (for testing).
        """
        self.verify_credentials = verify_credentials

    async def authenticate(self, conn: HTTPConnection) -> Optional[Tuple[AuthCredentials, SimpleUser]]:
        """Authenticate request using HTTP Basic Authentication.

        Args:
            conn: The HTTP connection containing request headers

        Returns:
            Tuple of (AuthCredentials, SimpleUser) if authenticated, None otherwise

        Raises:
            AuthenticationError: If authentication credentials are malformed
        """
        if "Authorization" not in conn.headers:
            return None

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split(" ", 1)
            if scheme.lower() != "basic":
                return None
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")

        # Verify credentials if verifier is provided
        if self.verify_credentials:
            if not await self._call_verifier(username, password):
                return None

        return AuthCredentials(["authenticated"]), SimpleUser(username)

    async def _call_verifier(self, username: str, password: str) -> bool:
        """Call the credential verifier function.

        Handles both sync and async verifier functions.
        """
        import asyncio
        import inspect

        if inspect.iscoroutinefunction(self.verify_credentials):
            return await self.verify_credentials(username, password)
        else:
            return self.verify_credentials(username, password)


class User:
    """Extended user class with additional Air-specific functionality.

    Provides a more feature-rich user object compared to Starlette's SimpleUser.
    """

    def __init__(
        self,
        username: str,
        is_authenticated: bool = True,
        display_name: Optional[str] = None,
        extra_data: Optional[dict] = None,
    ):
        """Initialize User.

        Args:
            username: The user's username/identifier
            is_authenticated: Whether the user is authenticated
            display_name: Display name for the user (defaults to username)
            extra_data: Additional user data dictionary
        """
        self.username = username
        self.is_authenticated = is_authenticated
        self.display_name = display_name or username
        self.extra_data = extra_data or {}

    def __getitem__(self, key):
        """Allow dict-like access to extra_data."""
        return self.extra_data[key]

    def get(self, key, default=None):
        """Get value from extra_data with default."""
        return self.extra_data.get(key, default)

    def __repr__(self):
        return f"User(username='{self.username}', authenticated={self.is_authenticated})"


class AnonymousUser:
    """Represents an unauthenticated user."""

    def __init__(self):
        self.is_authenticated = False
        self.display_name = "Anonymous"
        self.username = None

    def __getitem__(self, key):
        raise KeyError(f"AnonymousUser has no attribute '{key}'")

    def get(self, key, default=None):
        return default

    def __repr__(self):
        return "AnonymousUser()"
