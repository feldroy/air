# ext.sql

This module includes utility functions for using SQL with AIR.

## Package requirements

Using this module rquires additional dependencies installable in `air[sql]`, which can be installed with `uv add "air[sql]"`:

- SQLModel
- greenlet

## Database-specific Connection libraries

Depending on your database, you may also need to install sync and async drivers, for example:

|Database | Connection Libraries |
| --- | --- |
| PostgreSQL | `psycopg2-binary`, `asyncpg` |
| SQLite | `aiosqlite` |


!!! warning

    Persistent database connections require a lifespan object, otherwise you may receive timeout exceptions when the server is idle for even brief periods. To prevent this from happening, when using SQL connections in air views we strong recommend using the `air.ext.sql.async_db_lifespan` lifespan function.

    ```python
    import air

    app = air.Air(lifespan=air.ext.sql.async_db_lifespan)
    ```

## Configuration

This module introduces two environment variables:

::: air.ext.sql
    options:
      group_by_category: false
      members:
        - DATABASE_URL      
        - DEBUG
        - async_db_lifespan
        - create_sync_engine
        - create_async_engine
        - create_async_session
        - get_async_session
        - async_session_dependency
        - get_object_or_404