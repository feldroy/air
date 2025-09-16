try:
    from ..ext.sql import (
        AsyncSession as AsyncSession,
        async_session_dependency as async_session_dependency,
        create_async_engine as create_async_engine,
        create_async_session as create_async_session,
        create_sync_engine as create_sync_engine,
        get_async_session as get_async_session,
    )
except ImportError:  # pragma: no cover
    msg = "air.ext.sql requires installing the sqlmodel and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    sql = NotImportable()

try:
    from ..ext.user.router import (
        GITHUB_CLIENT_ID as GITHUB_CLIENT_ID,
        GITHUB_CLIENT_SECRET as GITHUB_CLIENT_SECRET,
        user_router as user_router,
        login_github as login_github
    )
    from ..ext.user.models import (
        BaseUser as BaseUser,
        UserStatusEnum as UserStatusEnum
    )
except ImportError as exc:  # pragma: no cover
    msg = "air.ext.user requires installing the authlib, sqlmodel, and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    sql = NotImportable()
