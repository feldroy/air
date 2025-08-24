"""Tests for Air authentication functionality."""

import base64
from unittest.mock import AsyncMock

import pytest
from starlette.applications import Starlette
from starlette.authentication import AuthCredentials, AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from air.auth import AnonymousUser, BasicAuthBackend, User


class TestBasicAuthBackend:
    """Test cases for BasicAuthBackend."""

    @pytest.mark.asyncio
    async def test_no_authorization_header(self):
        """Test that missing Authorization header returns None."""
        backend = BasicAuthBackend()

        # Mock connection without Authorization header
        class MockConnection:
            headers = {}

        result = await backend.authenticate(MockConnection())
        assert result is None

    @pytest.mark.asyncio
    async def test_wrong_auth_scheme(self):
        """Test that non-basic auth schemes return None."""
        backend = BasicAuthBackend()

        class MockConnection:
            headers = {"Authorization": "Bearer token123"}

        result = await backend.authenticate(MockConnection())
        assert result is None

    @pytest.mark.asyncio
    async def test_malformed_credentials(self):
        """Test that malformed credentials raise AuthenticationError."""
        backend = BasicAuthBackend()

        class MockConnection:
            headers = {"Authorization": "Basic invalid-base64"}

        with pytest.raises(AuthenticationError):
            await backend.authenticate(MockConnection())

    @pytest.mark.asyncio
    async def test_valid_credentials_no_verifier(self):
        """Test successful authentication without credential verifier."""
        backend = BasicAuthBackend()

        # Create valid basic auth header
        credentials = base64.b64encode(b"testuser:testpass").decode("ascii")

        class MockConnection:
            headers = {"Authorization": f"Basic {credentials}"}

        result = await backend.authenticate(MockConnection())

        assert result is not None
        auth_credentials, user = result
        assert isinstance(auth_credentials, AuthCredentials)
        assert "authenticated" in auth_credentials.scopes
        assert user.display_name == "testuser"

    @pytest.mark.asyncio
    async def test_valid_credentials_with_sync_verifier(self):
        """Test authentication with synchronous credential verifier."""

        def verify_sync(username, password):
            return username == "admin" and password == "secret"

        backend = BasicAuthBackend(verify_sync)

        # Valid credentials
        credentials = base64.b64encode(b"admin:secret").decode("ascii")

        class MockConnection:
            headers = {"Authorization": f"Basic {credentials}"}

        result = await backend.authenticate(MockConnection())

        assert result is not None
        auth_credentials, user = result
        assert user.display_name == "admin"

    @pytest.mark.asyncio
    async def test_invalid_credentials_with_verifier(self):
        """Test authentication failure with credential verifier."""

        def verify_fail(username, password):
            return False

        backend = BasicAuthBackend(verify_fail)

        credentials = base64.b64encode(b"user:pass").decode("ascii")

        class MockConnection:
            headers = {"Authorization": f"Basic {credentials}"}

        result = await backend.authenticate(MockConnection())
        assert result is None

    @pytest.mark.asyncio
    async def test_async_verifier(self):
        """Test authentication with asynchronous credential verifier."""

        async def verify_async(username, password):
            return username == "async_user" and password == "async_pass"

        backend = BasicAuthBackend(verify_async)

        credentials = base64.b64encode(b"async_user:async_pass").decode("ascii")

        class MockConnection:
            headers = {"Authorization": f"Basic {credentials}"}

        result = await backend.authenticate(MockConnection())

        assert result is not None
        auth_credentials, user = result
        assert user.display_name == "async_user"


class TestUser:
    """Test cases for User class."""

    def test_user_creation(self):
        """Test User object creation and properties."""
        user = User("testuser", extra_data={"email": "test@example.com"})

        assert user.username == "testuser"
        assert user.is_authenticated is True
        assert user.display_name == "testuser"
        assert user["email"] == "test@example.com"
        assert user.get("email") == "test@example.com"
        assert user.get("nonexistent", "default") == "default"

    def test_user_with_display_name(self):
        """Test User with custom display name."""
        user = User("jdoe", display_name="John Doe")

        assert user.username == "jdoe"
        assert user.display_name == "John Doe"

    def test_user_representation(self):
        """Test User string representation."""
        user = User("testuser")
        repr_str = repr(user)

        assert "testuser" in repr_str
        assert "authenticated=True" in repr_str


class TestAnonymousUser:
    """Test cases for AnonymousUser class."""

    def test_anonymous_user_properties(self):
        """Test AnonymousUser properties."""
        user = AnonymousUser()

        assert user.is_authenticated is False
        assert user.display_name == "Anonymous"
        assert user.username is None
        assert user.get("anything", "default") == "default"

    def test_anonymous_user_getitem_raises(self):
        """Test that AnonymousUser raises KeyError for dict access."""
        user = AnonymousUser()

        with pytest.raises(KeyError):
            _ = user["nonexistent"]

    def test_anonymous_user_representation(self):
        """Test AnonymousUser string representation."""
        user = AnonymousUser()
        assert repr(user) == "AnonymousUser()"


class TestIntegration:
    """Integration tests with Starlette middleware."""

    def test_basic_auth_middleware_integration(self):
        """Test BasicAuthBackend integration with AuthenticationMiddleware."""

        def verify_credentials(username, password):
            return username == "admin" and password == "secret"

        backend = BasicAuthBackend(verify_credentials)

        async def protected(request):
            if not request.user.is_authenticated:
                return JSONResponse({"error": "Not authenticated"}, status_code=401)
            return JSONResponse({"user": request.user.display_name})

        from starlette.middleware import Middleware
        from starlette.routing import Route

        app = Starlette(
            routes=[Route("/protected", protected)], middleware=[Middleware(AuthenticationMiddleware, backend=backend)]
        )

        client = TestClient(app)

        # Test without credentials
        response = client.get("/protected")
        assert response.status_code == 401

        # Test with invalid credentials
        headers = {"Authorization": "Basic " + base64.b64encode(b"wrong:creds").decode()}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401

        # Test with valid credentials
        headers = {"Authorization": "Basic " + base64.b64encode(b"admin:secret").decode()}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"user": "admin"}
