from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    GitHubOAuthRouterFactory: Callable

try:
    from . import auth as auth
except ImportError:  # pragma: no cover
    msg = "air.ext.auth requires installing the authlib package."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    auth = NotImportable()  # ty:ignore[invalid-assignment]


try:
    from . import sql as sql
except ImportError:  # pragma: no cover
    msg = "air.ext.sql requires installing the sqlmodel and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    sql = NotImportable()  # ty:ignore[invalid-assignment]
