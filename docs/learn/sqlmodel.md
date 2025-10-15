# SQLModel

!!! note "This feature is for Air 0.30.0 or later."

!!! info "air.ext.sqlmodel"
    The SQLModel support in Air is provided by the `air.ext.sqlmodel` module, which is an optional extension (currently in core Air but to be moved to an external package shortly). To use it, you need to install Air with the `sqlmodel` extra:

    ```bash
    pip install "air[sqlmodel]"
    ```

    The full reference for the tooling can be found at the [SQL API Reference](../api/ext/sqlmodel.md).

Thanks to the power of SQLModel and SQLAlchemy **Air** works with relational databases. Right now we have verified it supports PostgreSQL and SQLite. Our vision is for the community to build packages for all relational databases that allow for asynchronous connections through SQLAlchemy. 

## Air loves SQLModel

[SQLModel](https://sqlmodel.tiangolo.com/) is a wrapper around the venerable and proven SQLAlchemy library. Like Typer, FastAPI, pydantic, and Air, SQLModel allows for definition of critical objects with type annotations - in this case database tables. SQLModel makes SQLAlchemy a bit easier to use, although it's possible to drop down to the raw power of SQLAlchemy at any time.

Using Air's SQL module requires an understanding of SQLModel. Fortunately, it's an easy library to learn.

## Configuring Air for SQL

While not strictly required, it's highly recommended to use the `DATABASE_URL` environment variable to configure your database connection. This is a common convention used by many web frameworks and libraries.

To ensure the database remains connected to Air, we configure a `lifespan` function, and pass that to the Air app upon instantiation. If you don't do this, then the connection will eventually expire and your application will start throwing errors.

So when instantiating your project's root 'app':

```python title="main.py"
import air

app = air.Air(lifespan=air.ext.sqlmodel.async_db_lifespan)
```

## Making SQL Queries inside Air Views

Most of the time, you'll be using SQLModel inside your Air views. The easiest way to do this is to use the `air.ext.sqlmodel.async_session_dependency` dependency, which requires that the `DATABASE_URL` environment variable be set. This will provide you with an asynchronous session connected to your database.

```python title="main.py"
import air
sql = air.ext.sqlmodel

app = air.Air(lifespan=air.ext.sqlmodel.async_db_lifespan)

@app.page
async def index(request: Request, session: sql.AsyncSession = air.Depends(sql.async_session_dependency)):
    # Use the session to interact with the database
    result = await session.execute(select(User).where(User.name == "John"))
    user = result.scalars().first()
    
    return air.Main(
        air.H1("User Info"),
        air.P(f"Name: {user.name}"),
        air.P(f"Email: {user.email}"),
    )
```

## Making SQLModel Queries Outside Air Views

Sometimes you may want to make SQL queries outside of Air views, for example in background tasks or other parts of your application. In these cases, you can use the `air.ext.sqlmodel.get_async_session` function to get an asynchronous session.

```python title="tasks.py"
import air
sql = air.ext.sqlmodel

async def some_background_task():
    async with sql.get_async_session() as session:
        result = await session.execute(select(User).where(User.active == True))
        active_users = result.scalars().all()
        # Do something with active_users
```
