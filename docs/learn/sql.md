# SQL

> Note: This feature is for Air 0.28.0 or later. 

Thanks to the power of SQLModel and SQLAlchemy **Air** works with relational databases. Right now it just supports PostgreSQL and SQLite. Fortunately the project will soon expand to support all relational databases that allow for asynchronous connections through SQLAlchemy. 

## Air loves SQLModel

[SQLModel](https://sqlmodel.tiangolo.com/) is a wrapper around the venerable and proven SQLAlchemy library. Like Typer, FastAPI, pydantic, and Air, SQLModel allows for definition of critical objects with type annotations - in this case database tables. SQLModel makes SQLAlchemy a bit easier to use, although it's possible to drop down to the raw power of SQLAlchemy at any time.

Using Air's SQL module requires an understanding of SQLModel. Fortunately, it's an easy library to learn.

## Configuring Air for SQL

To ensure the database remains connected to Air, we configure a `lifespan` function, and pass that to the Air app upon instantiation. If you don't do this, then the connection will eventually expire and your application will start throwing errors.

So when instantiating your project's root 'app':

```python
import air

app = air.Air(lifespan=air.ext.sql.async_db_lifespan)
```