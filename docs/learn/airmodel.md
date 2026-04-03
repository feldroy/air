# AirModel

Your Pydantic models just learned PostgreSQL.

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
import air
from airmodel import AirModel, AirField


class UnicornSighting(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    location: str
    sparkle_rating: int
    confirmed: bool = AirField(default=False)


app = air.Air()  # DATABASE_URL in env, that's it


@app.get("/")
async def index(request: air.Request):
    sightings = await UnicornSighting.filter(confirmed=True, order_by="-sparkle_rating")
    return app.jinja(request, "sightings.html", sightings=sightings)
```

That's a database-backed web app. Set `DATABASE_URL` in your environment, and Air auto-connects to PostgreSQL on startup. No pool setup, no lifespan wiring, no configuration file. You wrote a Pydantic model, added `primary_key=True` to one field, and now it talks to PostgreSQL.

## One class, one import

```python
from airmodel import AirModel
```

One import, one base class. Define your fields with type annotations, and AirModel handles validation, serialization, and async database operations.

## Zero-config database

Set the `DATABASE_URL` environment variable and Air handles the rest:

```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
```

```python title="main.py"
app = air.Air()  # reads DATABASE_URL, connects automatically
```

The asyncpg pool opens when your app starts, tables are created automatically for every AirModel subclass you've imported, and the pool closes on shutdown. If you add a field to a model, `create_tables()` auto-migrates the existing table with `ALTER TABLE ADD COLUMN`. `?sslmode=require` works for hosted databases like NeonDB.

If `DATABASE_URL` is not set, `app.db` is `None` and no database is configured. Your app still runs, it just can't do database operations.

## Your types become your schema

```python
from datetime import datetime
from uuid import UUID

from airmodel import AirModel, AirField


class BlogPost(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    title: str
    body: str
    published: bool = AirField(default=False)
    created_at: datetime = AirField(default_factory=datetime.now)
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
fruits = await DragonFruit.bulk_create(
    [
        {"name": "Pink Pitaya", "color": "magenta"},
        {"name": "Yellow Dragon", "color": "yellow"},
    ]
)

# Update all matching rows
count = await DragonFruit.bulk_update({"color": "red"}, name__contains="Dragon")

# Delete all matching rows
count = await DragonFruit.bulk_delete(confirmed=False)
```

No N+1 round trips. Each operation is one SQL statement.

## Transactions

Group multiple operations so they all succeed or all fail:

```python
async with app.db.transaction():
    user = await User.create(name="Audrey", email="audrey@feldroy.com")
    await Profile.create(user_id=user.id, bio="Builds things")
    # Both rows commit together, or both roll back
```

If an exception occurs inside the block, the transaction rolls back automatically.

## Forms and database, together or apart

AirModel and AirForm are independent. Use one without the other, or snap them together:

```python
from airmodel import AirModel, AirField

from air import AirForm


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
        return air.Html(air.H1("Message sent"))
    return air.Html(air.Form(form.render(), method="post", action="/contact"))
```

`AirForm[ContactMessage]` gives you type-safe validated data. `ContactMessage.create()` writes it to PostgreSQL. Your editor knows the types at every step.

## A complete app in 30 lines

<!-- blacken-docs:off -->
```python title="main.py"
import air
from air import AirForm
from airmodel import AirModel, AirField


class GuestBookEntry(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str
    message: str


class GuestBookForm(AirForm[GuestBookEntry]):
    pass


app = air.Air()


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
<!-- blacken-docs:on -->

Model, form, database, HTML, validation, pagination, and two routes. Set `DATABASE_URL` and run it.

## Manual connection setup

If the zero-config path doesn't work for your situation (custom pool sizes, non-standard connection strings, multiple databases), you can wire the pool yourself:

```python title="main.py"
from airmodel import AirDB

db = AirDB()
app = air.Air(lifespan=db.lifespan("postgresql://localhost/mydb", min_size=5, max_size=20))
```

You shouldn't need this for most apps.
