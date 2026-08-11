# AirModel

Your Pydantic models get one async API with swappable persistence backends.

```jinja title="templates/sightings.html"
<!DOCTYPE html>
<html>
  <head><link rel="stylesheet" href="https://unpkg.com/mvp.css"></head>
  <body>
    <main>
      <h1>Confirmed Unicorn Sightings</h1>
      <ul>
        {% for s in sightings %}
          <li>{{ s.location }} ({{ s.sparkle_rating }} sparkles)</li>
        {% endfor %}
      </ul>
    </main>
  </body>
</html>
```

```python title="main.py"
from contextlib import asynccontextmanager
from os import getenv

import air
from air import AirField, AirModel
from airpostgres import AirPostgres


class UnicornSighting(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    location: str
    sparkle_rating: int
    confirmed: bool = AirField(default=False)


database = AirPostgres()


@asynccontextmanager
async def lifespan(app):
    async with database.lifespan(getenv("DATABASE_URL", ""))(app):
        await database.create_tables()
        yield


app = air.Air(lifespan=lifespan)


@app.get("/")
async def index(request: air.Request):
    sightings = await UnicornSighting.filter(confirmed=True, order_by="-sparkle_rating")
    return app.jinja(request, "sightings.html", sightings=sightings)
```

`AirModel` and `AirField` live in Air core. The separate AirPostgres package
handles asyncpg pooling, PostgreSQL SQL, transactions, and schema creation.
Choosing a different backend does not change the model class or its CRUD calls.

## One class, one import

```python
from air import AirModel
```

One import, one base class. Define your fields with type annotations, and
AirModel handles validation, serialization, and the async persistence API.

## Choose a persistence backend

Install the PostgreSQL backend:

```bash
uv add "AirPostgres>=0.2.0"
```

```python title="main.py"
from airpostgres import AirPostgres

database = AirPostgres()
```

Connect it in the application's lifespan, as shown above. AirPostgres opens the
asyncpg pool on startup and closes it on shutdown. `create_tables()` creates
tables for imported AirModel subclasses and non-destructively adds new columns.
The model API raises a clear error if no backend has been configured.

## Your types become your schema

```python
from datetime import datetime
from uuid import UUID

from air import AirField, AirModel


class BlogPost(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    title: str
    body: str
    published: bool = AirField(default=False)
    created_at: datetime = AirField(default_factory=datetime.now)
    author_id: UUID
```

With AirPostgres, every type annotation maps directly to a PostgreSQL column:

| Python type | PostgreSQL type |
|---|---|
| `str` | TEXT |
| `int` | INTEGER |
| `float` | DOUBLE PRECISION |
| `bool` | BOOLEAN |
| `datetime` | TIMESTAMP WITH TIME ZONE |
| `UUID` | UUID |

Required fields get `NOT NULL`. Optional fields (`str | None = None`) allow NULL.
Primary keys use BIGSERIAL. Unsupported PostgreSQL field types produce a clear
`TypeError` when AirPostgres builds the table schema.

## Table names just work

Class names are converted from CamelCase to snake_case and prefixed to avoid
collisions between applications. Models in a top-level package use that package
name. Models in generic modules such as `main`, `app`, or `models` use the
normalized project name from `pyproject.toml`:

| Model location | Project name | Class name | Table name |
|---|---|---|---|
| `main.py` | `my-app` | `BlogPost` | `my_app_blog_post` |
| `blog/models.py` | any | `BlogPost` | `blog_blog_post` |
| `sightings.py` | any | `UnicornSighting` | `sightings_unicorn_sighting` |

Set `table_name` when an existing schema or integration requires an exact name:

```python
class BlogPost(AirModel):
    table_name = "blog_post"

    id: int | None = AirField(default=None, primary_key=True)
    title: str
```

## Seven async methods that cover 90% of database work

### Create a row

```python
post = await BlogPost.create(
    title="Why Unicorns Prefer PostgreSQL",
    body="It's the rainbow cursors.",
    author_id=some_uuid,
)
# post.id is now set by the database
```

`create()` inserts, returns a fully populated instance with the database-generated primary key, and your editor knows `post.title` is a `str`. No refresh needed.

### Fetch exactly one row

```python
post = await BlogPost.get(id=42)
```

Returns the instance, or `None` if nothing matches. And if your query accidentally matches two rows, it raises `MultipleObjectsReturned` instead of silently returning the first one. That catches data integrity bugs the moment they happen, not three months later in production.

### Filter with sorting and pagination

```python
# All published posts, newest first
posts = await BlogPost.filter(published=True, order_by="-created_at")

# Page 3 of results
page = await BlogPost.filter(published=True, order_by="-created_at", limit=10, offset=20)
```

Prefix a field name with `-` for descending. Pagination without ordering is undefined in PostgreSQL (the rows come back in whatever order the database feels like), so `order_by` is right there next to `limit` and `offset` where you need it.

### Lookup operators

Go beyond equality with Django-style double-underscore suffixes:

```python
# Ratings above 8
await UnicornSighting.filter(sparkle_rating__gte=8)

# Location contains "Falls"
await UnicornSighting.filter(location__contains="Falls")

# Rating is one of these values
await UnicornSighting.filter(sparkle_rating__in=[5, 8, 11])

# Confirmed is not null
await UnicornSighting.filter(confirmed__isnull=False)
```

Supported: `__gt`, `__gte`, `__lt`, `__lte`, `__contains`, `__icontains`, `__in`, `__isnull`. These work in `filter()`, `get()`, and `count()`.

### Fetch everything

```python
every_post = await BlogPost.all(order_by="title", limit=100)
```

Same `order_by`, `limit`, and `offset` support.

### Count rows

```python
total = await BlogPost.count()
published = await BlogPost.count(published=True)
```

Returns an integer. Pass keyword arguments to count with a WHERE clause.

### Update in place

```python
post = await BlogPost.get(id=42)
post.title = "Updated Title"
await post.save()
```

`save()` uses `UPDATE ... RETURNING *`, so if your database has triggers or generated columns, the instance picks up those changes immediately. No stale data.

To update only specific fields (avoiding lost-update bugs when two requests edit different columns):

```python
await post.save(update_fields=["title"])
```

### Delete and forget

```python
post = await BlogPost.get(id=42)
await post.delete()
# post.id is now None
```

After deletion, the primary key is cleared. Try to `save()` or `delete()` the same instance again and you get a clear `ValueError` instead of a silent no-op against a missing row.

## Bulk operations

Insert, update, or delete hundreds of rows in a single SQL statement:

```python
# Insert multiple rows at once
fruits = await DragonFruit.bulk_create([
    {"name": "Pink Pitaya", "color": "magenta"},
    {"name": "Yellow Dragon", "color": "yellow"},
])

# Update all matching rows
count = await DragonFruit.bulk_update({"color": "red"}, name__contains="Dragon")

# Delete all matching rows
count = await DragonFruit.bulk_delete(confirmed=False)
```

No N+1 round trips. Each operation is one SQL statement.

## Transactions

Group multiple operations so they all succeed or all fail:

```python
async with database.transaction():
    user = await User.create(name="Audrey", email="audrey@feldroy.com")
    await Profile.create(user_id=user.id, bio="Builds things")
    # Both rows commit together, or both roll back
```

If an exception occurs inside the block, the transaction rolls back automatically.

## Forms and database, together or apart

AirModel and AirForm are independent. Use one without the other, or snap them together:

```python
from air import AirField, AirForm, AirModel


class ContactMessage(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str
    email: str
    body: str


class ContactForm(AirForm[ContactMessage]):
    pass


@app.post("/contact")
async def submit_contact(request: air.Request):
    form = await ContactForm.from_request(request)
    if form.is_valid:
        await ContactMessage.create(**form.save_data())
        return air.Html(
            air.H1("Message sent"),
        )
    return air.Html(
        air.Form(
            form.render(),
            method="post",
            action="/contact"
        ),
    )
```

`AirForm[ContactMessage]` gives you type-safe validated data. `ContactMessage.create()` writes it to PostgreSQL. Your editor knows the types at every step.

## A complete app in 30 lines

```python title="main.py"
from contextlib import asynccontextmanager
from os import getenv

import air
from air import AirField, AirForm, AirModel
from airpostgres import AirPostgres


class GuestBookEntry(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str
    message: str


class GuestBookForm(AirForm[GuestBookEntry]):
    pass


database = AirPostgres()


@asynccontextmanager
async def lifespan(app):
    async with database.lifespan(getenv("DATABASE_URL", ""))(app):
        await database.create_tables()
        yield


app = air.Air(lifespan=lifespan)


@app.page
async def index():
    entries = await GuestBookEntry.all(order_by="-id", limit=50)
    form = GuestBookForm()
    return air.layouts.mvpcss(
        air.H1("Guest Book"),
        air.Form(
            form.render(),
            air.Button("Sign", type_="submit"),
            method="post",
            action="/sign",
        ),
        air.Hr(),
        *[air.Article(air.Strong(e.name), air.P(e.message))
          for e in entries],
    )


@app.post("/sign")
async def sign(request: air.Request):
    form = await GuestBookForm.from_request(request)
    if form.is_valid:
        await GuestBookEntry.create(name=form.data.name, message=form.data.message)
    return air.RedirectResponse("/")
```

Model, form, database, HTML, validation, pagination, and two routes use the same
AirModel API.

## Swap the backend

Application models import only from Air:

```python title="main.py"
from air import AirField, AirModel

class Note(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    body: str
```

The application lifespan chooses AirPostgres, AirD1, or another implementation
of `AirModelBackend`. AirModel translates CRUD calls into backend-neutral
queries and validates models; each backend owns its driver, SQL dialect, and
schema lifecycle. Model definitions, forms, and CRUD call sites remain the
same.
