from collections.abc import Callable
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    GitHubOAuthRouterFactory: Callable

try:
    from . import auth as auth
except ImportError:  # pragma: no cover
    msg = "air.ext.auth requires installing the authlib package."

    class NotImportable:
        def __getattribute__(self, name: str) -> NoReturn:
            raise RuntimeError(msg)

        def __str__(self) -> str:
            return msg

        def __repr__(self) -> str:
            return msg

    auth = NotImportable()  # ty:ignore[invalid-assignment]


try:
    from . import sqlmodel as sqlmodel
except ImportError:  # pragma: no cover
    msg = "air.ext.sqlmodel requires installing the sqlmodel and greenlet packages. "
    msg += "It may also require the installation of database specific connectors."

    class NotImportable:
        def __getattribute__(self, name: str) -> NoReturn:
            raise RuntimeError(msg)

        def __str__(self) -> str:
            return msg

        def __repr__(self) -> str:
            return msg

    sqlmodel = NotImportable()  # ty:ignore[invalid-assignment]
