try:
    from . import sql
except ImportError:
    msg = "air.db.sql requires installing the sqlmodel and greenlet packages."

    class NotImportable:
        def __getattribute__(self, name):
            raise RuntimeError(msg)

        def __str__(self):
            return msg

        def __repr__(self):
            return msg

    sql = NotImportable()  # type: ignore [invalid-assignment]
