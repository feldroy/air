# SQLModel
[SQLModel](https://sqlmodel.tiangolo.com/) is a wrapper around the venerable and proven SQLAlchemy library. Like Typer, FastAPI, pydantic, and Air, SQLModel allows for definition of critical objects with type annotations - in this case database tables. SQLModel makes SQLAlchemy a bit easier to use, although it's possible to drop down to the raw power of SQLAlchemy at any time.

Using the [AirSQLModel](https://github.com/pydanny/airsqlmodel) package requires an understanding of SQLModel. Fortunately, it's an easy library to learn.

## Installing AirSQLModel

```bash
uv add airsqlmodel
```

Or if you are on pip:

```bash
pip install airsqlmodel
```


## Configuring Air for SQL

While not strictly required, it's highly recommended to use the `DATABASE_URL` environment variable to configure your database connection. This is a common convention used by many web frameworks and libraries.

To ensure the database remains connected to Air, we configure a `lifespan` function, and pass that to the Air app upon instantiation. If you don't do this, then the connection will eventually expire and your application will start throwing errors.

So when instantiating your project's root 'app':

```python title="main.py"
import air
import airsqlmodel as sql

app = air.Air(lifespan=sql.async_db_lifespan)
```

## Making SQL Queries inside Air Views

Most of the time, you'll be using SQLModel inside your Air views. The easiest way to do this is to use the `airsqlmodel.async_session_dependency` dependency, which requires that the `DATABASE_URL` environment variable be set. This will provide you with an asynchronous session connected to your database.

```python title="main.py"
import air
import airsqlmodel as sql
from sqlmodel import SQLModel, Field, select

app = air.Air(lifespan=sql.async_db_lifespan)


@app.page
async def index(
    request: Request,
    session: sql.AsyncSession = air.Depends(sql.async_session_dependency),
):
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
import airsqlmodel as sql
from sqlmodel import SQLModel, Field, select


async def some_background_task():
    async with sql.get_async_session() as session:
        result = await session.execute(select(User).where(User.active == True))
        active_users = result.scalars().all()
        # Do something with active_users
```
