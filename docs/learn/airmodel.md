# AirModel

Your Pydantic models just learned PostgreSQL.

```python title="main.py"
from air import AirDB, AirModel, Field

import air


class UnicornSighting(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    location: str
    sparkle_rating: int
    confirmed: bool = Field(default=False)


db = AirDB()
app = air.Air(lifespan=db.lifespan("postgresql://localhost/mydb"))


@app.page
async def index():
    sightings = await UnicornSighting.filter(confirmed=True, order_by="-sparkle_rating")
    return air.layouts.mvpcss(
        air.H1("Confirmed Unicorn Sightings"),
        air.Ul(*[air.Li(f"{s.location} ({s.sparkle_rating} sparkles)") for s in sightings]),
    )
```

That's a database-backed web app. No SQLAlchemy. No migrations framework. No session management. You wrote a Pydantic model, added `primary_key=True` to one field, and now it talks to PostgreSQL. Every query is async, every result is a type-checked Pydantic instance, and your editor knows the shape of every row.

## One class, one import

```python
from air import AirModel
```

One import, one base class. Define your fields with type annotations, and AirModel handles validation, serialization, and async database operations.

## Connecting takes two lines

```python title="main.py"
db = AirDB()
app = air.Air(lifespan=db.lifespan(os.environ["DATABASE_URL"]))
```

AirDB wraps an asyncpg connection pool. It opens when your app starts, closes when it shuts down, and handles `?sslmode=require` for hosted databases like NeonDB. To create your tables:

```python
await db.create_tables()
```

Every AirModel subclass you've imported gets a `CREATE TABLE IF NOT EXISTS`. That's it.

## Your types become your schema

```python
from datetime import datetime
from uuid import UUID

from air import AirModel, Field


class BlogPost(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    author_id: UUID
```

Every type annotation maps directly to a PostgreSQL column:

| Python type | PostgreSQL type |
|---|---|
| `str` | TEXT |
| `int` | INTEGER |
| `float` | DOUBLE PRECISION |
| `bool` | BOOLEAN |
| `datetime` | TIMESTAMP WITH TIME ZONE |
| `UUID` | UUID |

Required fields get `NOT NULL`. Optional fields (`str | None = None`) allow NULL. Primary keys use BIGSERIAL so you never hit the 2-billion row ceiling. And if you use a type that's not supported, you get a clear `TypeError` at class definition time, not a confusing failure at query time.

## Table names just work

Class names are auto-converted from CamelCase to snake_case, the way every PostgreSQL user expects:

| Class name | Table name |
|---|---|
| `BlogPost` | `blog_post` |
| `UnicornSighting` | `unicorn_sighting` |
| `DragonFruit` | `dragon_fruit` |

No `__tablename__` to remember. Open psql and everything looks right.

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

### Delete and forget

```python
post = await BlogPost.get(id=42)
await post.delete()
# post.id is now None
```

After deletion, the primary key is cleared. Try to `save()` or `delete()` the same instance again and you get a clear `ValueError` instead of a silent no-op against a missing row.

## Forms and database, together or apart

AirModel and AirForm are independent. Use one without the other, or snap them together:

```python
class ContactMessage(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    body: str


class ContactForm(air.AirForm[ContactMessage]):
    pass


@app.post("/contact")
async def submit_contact(request: air.Request):
    form = await ContactForm.from_request(request)
    if form.is_valid:
        await ContactMessage.create(
            name=form.data.name,
            email=form.data.email,
            body=form.data.body,
        )
        return air.Html(air.H1("Message sent"))
    return air.Html(air.Form(form.render(), method="post", action="/contact"))
```

`AirForm[ContactMessage]` gives you type-safe validated data. `ContactMessage.create()` writes it to PostgreSQL. Your editor knows the types at every step.

## A complete app in 30 lines

```python title="main.py"
import os

import air
from air import AirDB, AirModel, Field


class GuestBookEntry(AirModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    message: str


class GuestBookForm(air.AirForm[GuestBookEntry]):
    pass


db = AirDB()
app = air.Air(lifespan=db.lifespan(os.environ["DATABASE_URL"]))


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
        *[air.Article(air.Strong(e.name), air.P(e.message)) for e in entries],
    )


@app.post("/sign")
async def sign(request: air.Request):
    form = await GuestBookForm.from_request(request)
    if form.is_valid:
        await GuestBookEntry.create(name=form.data.name, message=form.data.message)
    return air.RedirectResponse("/")
```

Model, form, database, HTML, validation, pagination, and two routes. Everything from one framework.
