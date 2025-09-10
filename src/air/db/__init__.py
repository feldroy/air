try:
    from .sql import (
        AsyncSession as AsyncSession,
        async_session_dependency as async_session_dependency,
        create_async_engine as create_async_engine,
        create_async_session as create_async_session,
        create_sync_engine as create_sync_engine,
        get_async_session as get_async_session,
    )
except ImportError:  # pragma: no cover
    msg = "air.db.sql requires installing the sqlmodel and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    sql = NotImportable()  # type: ignore [invalid-assignment]
