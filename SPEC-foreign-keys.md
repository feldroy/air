# Foreign Key Support for AirModel, AirField, AirForm

## The problem

Foreign key fields are plain `int` with no relationship metadata. This means:

- `create_tables()` emits no `REFERENCES` constraint — the database can't enforce referential integrity
- `AirForm` renders FK fields as text inputs instead of `<select>` dropdowns
- There's no way to query related objects or validate that an FK value points to a real record

## Real use case (bear mochi dango shop)

```python
# Current — no FK metadata, just bare ints
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int                    # FK to Maker — but Air doesn't know that
    flavor: str
    order_id: int | None = None      # FK to Order — but Air doesn't know that

class Order(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    customer_id: int                 # FK to Customer
    total_cents: int
    placed_at: datetime
```

The `maker_id` and `customer_id` fields are plain integers. Forms render them as `<input type="number">`. The database has no constraints preventing orphaned rows.

## Proposed API

### Declaring a foreign key

```python
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker, label="Maker")
    flavor: str
    order_id: int | None = AirField(default=None, foreign_key=Order)
```

`foreign_key=Maker` means: this integer column references `Maker`'s primary key.

### What changes

#### 1. AirField — new `foreign_key` parameter

In `src/air/field/main.py`, add a `foreign_key` parameter:

```python
def AirField(
    default: Any = ...,
    *,
    primary_key: bool = False,
    foreign_key: type | None = None,   # NEW
    type: str | None = None,
    label: str | None = None,
    ...
) -> Any:
```

Creates a new `ForeignKey` metadata object stored on `field_info.metadata`.

#### 2. New metadata class

In `src/air/field/types.py`:

```python
@dataclass(frozen=True)
class ForeignKey(BasePresentation):
    to: type  # The referenced AirModel class
```

#### 3. SQL generation — `REFERENCES` constraint

In `_column_defs()`, when a field has `ForeignKey` metadata:

```sql
"maker_id" INTEGER NOT NULL REFERENCES "mochi_maker"("id")
```

The referenced table name comes from `fk.to._table_name()`, and the referenced column from `fk.to._pk_field()`.

For optional FKs (`int | None`), omit `NOT NULL`:

```sql
"order_id" INTEGER REFERENCES "mochi_order"("id")
```

#### 4. AirForm — render as `<select>`

In `pydantic_type_to_html_type()`, when `ForeignKey` metadata is present, return `"select"`.

In `default_form_widget()`, when rendering a FK field:

1. Call `await fk.to.all()` to fetch all possible values
2. Build `<option>` elements using each record's PK as value and `str(record)` as label
3. Render as `<select>`

This requires `default_form_widget` to become async (or the options must be pre-fetched). The cleanest approach: pre-fetch FK options in `AirForm.render()` before calling the widget function, and pass them as a `choices` override.

#### 5. Display label for FK options

AirModel gets an optional `__str__` convention. If the referenced model defines `__str__`, use it for the option label. Otherwise fall back to `f"{model.__name__} #{pk}"`.

```python
class Maker(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

    def __str__(self):
        return self.name
```

The `<select>` would render:

```html
<select name="maker_id">
    <option value="">Select...</option>
    <option value="1">Kuma-san</option>
    <option value="2">Tanuki Mochi Co</option>
</select>
```

## What this does NOT include

- **Cascading deletes** — handle at the application level or add later with `on_delete` parameter
- **Reverse relations** (e.g., `user.repos`) — a separate feature
- **Join queries / select_related** — a separate feature
- **Composite foreign keys** — not needed, all PKs are single-column BIGSERIAL

## Implementation plan

1. Add `ForeignKey` metadata class to `src/air/field/types.py`
2. Add `foreign_key` parameter to `AirField()` in `src/air/field/main.py`
3. Update `_column_defs()` in `src/air/model/main.py` to emit `REFERENCES`
4. Update `pydantic_type_to_html_type()` and `default_form_widget()` in `src/air/form/main.py` to render FK fields as `<select>` with fetched options
5. Tests for each layer

## Test cases

```python
# SQL generation
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker)

sql = Dango._create_table_sql()
assert 'REFERENCES "mochi_maker"("id")' in sql

# Optional FK
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order)

sql = Dango._create_table_sql()
assert '"order_id" INTEGER REFERENCES' in sql
assert 'NOT NULL' not in sql.split('order_id')[1].split('\n')[0]

# Form rendering
form = DangoForm()
html = form.render()
assert '<select' in html
assert 'name="maker_id"' in html
```
