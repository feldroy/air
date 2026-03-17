# Air Auth: Username/Password Authentication

## What Django gets right

Django ships `django.contrib.auth` with every install. A new developer gets:

- A `User` model with username, email, hashed password
- `login()`, `logout()`, `authenticate()` functions
- `@login_required` decorator
- Password hashing (PBKDF2 by default, bcrypt/argon2 optional)
- Session-backed auth (user ID in session, full user loaded per request)
- Built-in login/logout views and forms
- `create_user()` / `create_superuser()` management commands

The result: most Django apps have working auth on day one. The auth isn't perfect (no email-as-username by default, the `User` model is hard to swap later), but having it built in means developers don't waste their first day wiring up bcrypt and session cookies.

Air should match this: built-in, zero-config auth that works out of the box, with escape hatches for customization.

## Design principles

1. **One import away.** `import air.auth` gives you a working auth system. No configuration file, no settings dict, no third-party packages to install.

2. **Session-based.** Store the user ID in Starlette's signed cookie session (Air already ships `SessionMiddleware`). Load the full user on each request via middleware. This is the Django model, and it works for server-rendered HTML apps.

3. **Pydantic for validation, TortoiseORM for persistence.** Air already uses Pydantic (`AirModel`). TortoiseORM is async-native, uses the same `field = Field()` patterns as Pydantic, and supports PostgreSQL. The User model is a Tortoise model; Pydantic schemas handle input validation.

4. **Password hashing is not optional.** `air.auth` hashes passwords with argon2 (via `argon2-cffi`) by default. No "store passwords in plain text for development" mode. The API makes the secure path the easy path.

5. **Dependency injection for access control.** Air and FastAPI use `Depends()` for cross-cutting concerns. Auth follows the same pattern: `require_login`, `require_staff` are dependencies you attach to routes.

6. **Progressive disclosure.** Basic apps use `air.auth.User` as-is. Apps that need custom fields subclass it. Apps that need OAuth or API tokens add those later without replacing the core.

## Components

### User model (TortoiseORM)

```python
# air/auth/models.py
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=150, unique=True, index=True)
    email = fields.CharField(max_length=254, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    date_joined = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)

    class Meta:
        table = "air_users"
```

**Why these fields:**
- `username` and `email` both unique and indexed. Either can be used for login.
- `password_hash` stores the argon2 output. Never exposed via Pydantic schemas.
- `is_active` for soft-delete/ban without losing data. Inactive users can't log in.
- `is_staff` is the simplest authorization: staff vs. non-staff. Covers 80% of cases. Role-based access control is a later feature.
- No `first_name`/`last_name`. Django has these and everyone argues about them. A profile model is the user's job.

### Pydantic schemas

```python
# air/auth/schemas.py
import air


class UserCreate(air.AirModel):
    username: str = air.AirField(min_length=3, max_length=150)
    email: str = air.AirField(type="email")
    password: str = air.AirField(type="password", min_length=8)


class UserLogin(air.AirModel):
    username: str = air.AirField(autofocus=True)
    password: str = air.AirField(type="password")


class UserRead(air.AirModel):
    """Public-facing user data. No password hash."""
    id: int
    username: str
    email: str
    is_active: bool
    is_staff: bool
```

`UserCreate` and `UserLogin` extend `AirModel`, so they get `.to_form()` for free. A registration page is:

```python
form = UserCreate.to_form()
```

### Password hashing

```python
# air/auth/passwords.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False
```

Two functions. No configuration. argon2 is the winner of the Password Hashing Competition and the current OWASP recommendation. The `argon2-cffi` package is pure Python with C bindings, works everywhere.

### Core auth functions

```python
# air/auth/core.py
from datetime import datetime, timezone

from .models import User
from .passwords import hash_password, verify_password


async def create_user(username: str, email: str, password: str) -> User:
    """Create a user with a hashed password."""
    return await User.create(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )


async def authenticate(username: str, password: str) -> User | None:
    """Verify credentials. Returns the user or None."""
    user = await User.get_or_none(username=username, is_active=True)
    if user and verify_password(password, user.password_hash):
        user.last_login = datetime.now(timezone.utc)
        await user.save(update_fields=["last_login"])
        return user
    return None


async def login(request, user: User) -> None:
    """Store user ID in session."""
    request.session["user_id"] = user.id


async def logout(request) -> None:
    """Clear session."""
    request.session.clear()
```

These mirror Django's `authenticate()`, `login()`, `logout()`. The session stores only the user ID (an int), keeping the cookie small and avoiding serialization issues.

### Auth middleware

```python
# air/auth/middleware.py
from starlette.types import ASGIApp, Receive, Scope, Send

from .models import User


class AuthMiddleware:
    """Load the current user from session on every request.

    After this middleware runs, request.state.user is either
    a User instance or None.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            session = scope.get("session", {})
            user_id = session.get("user_id")
            if user_id:
                scope["state"]["user"] = await User.get_or_none(
                    id=user_id, is_active=True
                )
            else:
                scope["state"]["user"] = None
        await self.app(scope, receive, send)
```

This runs after `SessionMiddleware` (middleware order is LIFO in Starlette, so add `AuthMiddleware` first). Every request gets `request.state.user` populated. No database query if there's no user ID in session.

### Dependencies

```python
# air/auth/dependencies.py
from fastapi import HTTPException

import air

from .models import User


def current_user(request: air.Request) -> User | None:
    """Return the logged-in user or None."""
    return getattr(request.state, "user", None)


def require_login(request: air.Request) -> User:
    """Dependency that redirects to /login if not authenticated."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user


def require_staff(request: air.Request) -> User:
    """Dependency that requires is_staff=True."""
    user = require_login(request)
    if not user.is_staff:
        raise HTTPException(status_code=403)
    return user
```

Usage:

```python
from fastapi import Depends
from air.auth import require_login, require_staff

@app.page
async def dashboard(user=Depends(require_login)):
    return air.H1(f"Welcome, {user.username}")

@app.page
async def admin_panel(user=Depends(require_staff)):
    return air.H1("Admin Panel")
```

### Setup helper

```python
# air/auth/setup.py
import air
from .middleware import AuthMiddleware


def init_auth(app: air.Air, secret_key: str) -> None:
    """Wire up session + auth middleware in the correct order."""
    app.add_middleware(AuthMiddleware)
    app.add_middleware(air.SessionMiddleware, secret_key=secret_key)
```

One call in main.py:

```python
import air
from air.auth import init_auth

app = air.Air()
init_auth(app, secret_key="change-me-in-production")
```

### Database setup (TortoiseORM + PostgreSQL)

```python
# air/auth/db.py
from tortoise import Tortoise


async def init_db(db_url: str = "postgres://localhost/myapp") -> None:
    """Initialize TortoiseORM with the auth models."""
    await Tortoise.init(
        db_url=db_url,
        modules={"auth": ["air.auth.models"]},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
```

Integrates with lifespan:

```python
from contextlib import asynccontextmanager
import air
from air.auth import init_auth
from air.auth.db import init_db, close_db

@asynccontextmanager
async def lifespan(app):
    await init_db("postgres://localhost/myapp")
    yield
    await close_db()

app = air.Air(lifespan=lifespan)
init_auth(app, secret_key="change-me-in-production")
```

## Complete example: login/register/dashboard

```python
from contextlib import asynccontextmanager

from fastapi import Depends, status

import air
from air.auth import (
    authenticate,
    create_user,
    init_auth,
    login,
    logout,
    require_login,
)
from air.auth.db import close_db, init_db
from air.auth.schemas import UserCreate, UserLogin


@asynccontextmanager
async def lifespan(app):
    await init_db("postgres://localhost/myapp")
    yield
    await close_db()


app = air.Air(lifespan=lifespan)
init_auth(app, secret_key="change-me-in-production")


@app.page
def register():
    form = UserCreate.to_form()
    return app.jinja(request, "register.html", form=form)


@app.post("/register")
async def do_register(request: air.Request):
    form = UserCreate.to_form()
    form_data = await request.form()

    if form.validate(form_data):
        user = await create_user(
            username=form.data.username,
            email=form.data.email,
            password=form.data.password,
        )
        await login(request, user)
        return air.RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    return app.jinja(request, "register.html", form=form)


@app.page
def sign_in():
    form = UserLogin.to_form()
    return app.jinja(request, "login.html", form=form)


@app.post("/sign-in")
async def do_sign_in(request: air.Request):
    form = UserLogin.to_form()
    form_data = await request.form()

    if form.validate(form_data):
        user = await authenticate(form.data.username, form.data.password)
        if user:
            await login(request, user)
            return air.RedirectResponse(
                "/dashboard", status_code=status.HTTP_303_SEE_OTHER
            )

    return app.jinja(request, "login.html", form=form, error="Invalid credentials")


@app.page
async def dashboard(request: air.Request, user=Depends(require_login)):
    return app.jinja(request, "dashboard.html", user=user)


@app.page
async def sign_out(request: air.Request):
    await logout(request)
    return air.RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
```

## Dependencies

```toml
[project]
dependencies = [
    "air>=0.47.0",
    "tortoise-orm[asyncpg]",
    "argon2-cffi",
]
```

TortoiseORM and argon2-cffi would be optional dependencies of Air (like `air[auth]`), not required for apps that don't use auth.

## What this doesn't cover (yet)

- **Email verification.** Requires an email sending service. Separate feature.
- **Password reset.** Requires email + token generation. Separate feature.
- **OAuth / social login.** FastAPI has `authlib` patterns. Separate feature.
- **API token auth.** Different mechanism (Bearer tokens, not sessions). Separate feature.
- **Role-based access control.** `is_staff` covers the simple case. A `Role` model with permissions is a separate feature.
- **CSRF protection.** Listed on the roadmap as a forms feature. Auth depends on it but doesn't implement it.
- **Rate limiting on login.** Important for production. Separate middleware.
- **Migrations.** TortoiseORM has Aerich for migrations. The spec uses `generate_schemas()` for simplicity. Production apps should use Aerich.

## Open questions

1. **Should `air.auth` be in core or a separate package?** Django puts it in core. FastAPI has no auth. Air could ship it as `air[auth]` (optional dependency group) so the base package stays light but auth is one `pip install` away.

2. **TortoiseORM vs SQLModel/SQLAlchemy?** The roadmap mentions SQLModel/SQLAlchemy for "Air ORM." If that's the direction, auth models should use the same ORM. TortoiseORM is simpler and async-native, but having two ORMs in the ecosystem is confusing.

3. **Custom User model.** Django's biggest auth mistake: making it hard to swap the User model after the first migration. Air should make this easy from the start. One approach: `air.auth.AbstractUser` as a base class, with `air.auth.User` as the concrete default. Apps that need custom fields subclass `AbstractUser`.

4. **Session backend.** Starlette's `SessionMiddleware` uses signed cookies. This means the session data (just a user ID int) is in the cookie, not on the server. Works fine for auth but limits session size. A Redis/database session backend would be a separate feature.
