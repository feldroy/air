# Foreign Key Support for AirModel, AirField, and AirForm

## The problem

Foreign key fields are plain `int` with no relationship metadata. This means:

- `create_tables()` emits no `REFERENCES` constraint, so the database can't enforce referential integrity
- `AirForm` renders FK fields as text inputs instead of `<select>` dropdowns
- There's no way to validate that an FK value points to a real record

## Real use case (bear mochi dango shop)

```python
# Current — no FK metadata, just bare ints
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int                    # FK to Maker, but Air doesn't know that
    flavor: str
    order_id: int | None = None      # FK to Order, but Air doesn't know that

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
    maker_id: int = AirField(foreign_key=Maker, on_delete="cascade", label="Maker")
    flavor: str
    order_id: int | None = AirField(default=None, foreign_key=Order, on_delete="set_null")
```

`foreign_key=Maker` means: this integer column references `Maker`'s primary key.

#### Forward references

When models reference each other, the target may not be defined yet. Accept either the class or a string name:

```python
# Class reference (target already defined)
maker_id: int = AirField(foreign_key=Maker)

# String reference (target defined later or circular)
maker_id: int = AirField(foreign_key="Maker")
```

String references resolve lazily against `_table_registry` at first use (SQL generation or form rendering), not at class definition time. Resolution searches by class name, not table name.

#### Self-referential foreign keys

A model can reference itself. This is common for tree structures:

```python
class Category(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str
    parent_id: int | None = AirField(default=None, foreign_key="Category", on_delete="cascade")
```

Self-references must use a string to avoid `NameError` (the class doesn't exist yet when its body executes). The topological sort skips self-references when building the dependency graph (a model is not a dependency of itself).

### Reverse relations

A parent model can query its children through FK metadata. No new declarations are needed on the parent.

```python
maker = await Maker.get(id=1)
dangos = await maker.related(Dango)

# Equivalent to:
dangos = await Dango.filter(maker_id=1)
```

`related()` discovers which field on the child model points to this model's class via ForeignKey metadata, then calls `filter()` with this instance's PK value. It accepts `order_by`, `limit`, and `offset`.

When a child model has multiple FKs to the same parent (e.g., `created_by` and `updated_by` both pointing to `User`), `related()` raises `ValueError` directing the user to `filter()` with the specific field name:

```python
# Ambiguous: raises ValueError with a helpful message
docs = await user.related(Document)

# Use filter() instead:
created = await Document.filter(created_by=user.id)
updated = await Document.filter(updated_by=user.id)
```

Calling `related()` on an unsaved instance (PK is None) raises `ValueError`.

### Eager loading (select_related)

Fetching a list of dangos and then querying each one's maker is N+1 queries. `select_related` fetches parent records in a single extra query per FK field and attaches them to each instance.

```python
dangos = await Dango.all(select_related=["maker"])
print(dangos[0].maker.name)  # "Kuma-san"

dangos = await Dango.filter(flavor="matcha", select_related=["maker"])
dango = await Dango.get(id=1, select_related=["maker"])
```

`select_related` accepts relation names, not field names. The relation name is the FK field name with `_id` stripped: `maker_id` becomes `maker`. For FK fields that don't end in `_id`, the relation name is the field name itself. The resolved object is attached as an attribute with the relation name.

If a model has both a declared field and a FK that would produce the same relation name, that is a modeling error and raises `ValueError` at definition time.

**Implementation strategy: batch query, not JOIN.** For each FK field in `select_related`, collect all unique FK values from the result set, fetch the referenced records in one `__in` query, and attach them. This produces at most N+1 queries where N is the number of `select_related` fields (typically 1-3), not N+1 where N is the number of rows.

Eagerly-loaded attributes are transient, read-only, and not part of the Pydantic model. `model_dump()` excludes them. They are set via `object.__setattr__` (the same pattern `save()` and `delete()` already use). Optional FK fields with a NULL value get `None` as the attached attribute.

### Form rendering

`render()` is sync. Fetching FK options requires a database query (async). Two options:

**Option A: Make `render()` async.** Honest about the I/O, but breaks every existing `form.render()` call.

**Option B: Accept choices from the view.** Keep `render()` sync. Views pre-fetch FK options and pass them in.

**Decision: Option B.** It keeps `render()` sync, puts async I/O in the view where it belongs, and gives users control over queries (filtering, limits, ordering). The form shouldn't hide database queries.

```python
async def dango_form_view(request):
    form = DangoForm(
        choices={"maker_id": await Maker.as_choices(order_by="name")}
    )
    return templates.TemplateResponse(request, "form.html", {"form": form})
```

`AirForm.__init__` accepts an optional `choices: dict[str, list[tuple[Any, str]]]` parameter for dynamic choice overrides. This works for FK fields and for any field where choices need to be computed at render time. One mechanism, not two.

On `__init__`, validate that every key in `choices` corresponds to an actual field on the model. Raise `ValueError` on unknown keys so typos like `choices={"maker_di": [...]}` fail immediately.

When `ForeignKey` metadata is present on a field, `pydantic_type_to_html_type()` returns `"select"`. If no dynamic choices were provided, the select renders with just the "Select..." placeholder.

`ForeignKey` inherits `BasePresentation`, so it is visible to the form's `_meta_dict` helper with no changes to the lookup function.

**Plumbing dynamic choices to the renderer.** `AirForm.render()` passes `self._choices` to the widget. The widget callable protocol grows one parameter:

```python
# Before:
Callable[*, model, data, errors, excludes] -> str

# After:
Callable[*, model, data, errors, excludes, choices] -> str
```

`default_form_widget` accepts `choices` and passes it through to `_get_options`, which checks `choices.get(field_name)` before falling back to the existing metadata/Enum/Literal sources.

This is the only approach that avoids shared-state mutation. The alternatives were:
- **Mutate `field_info.metadata` at render time** to inject `Choices`. Rejected: `model_fields` is class-level state shared across every form instance and every request. Mutation during render, even with try/finally, makes the render path non-reentrant and creates thread-safety bugs under concurrent async requests.
- **Synthesize a per-render model subclass** via `create_model()` with `Choices` metadata injected. Rejected: creates a new Pydantic class on every render, and if it inherits from `AirModel` it pollutes `_table_registry`.
- **Stuff choices into the `data` dict.** Rejected: `data` means "the current value of each field." Overloading it with "the set of allowable values" conflates two concerns.

Growing the widget protocol by one parameter is a documented contract change. Custom widgets that don't care about dynamic choices can accept `**kwargs` and ignore it.

**Convenience helper** (on AirModel, not AirForm):

```python
@classmethod
async def as_choices(
    cls,
    *,
    order_by: str | None = None,
    limit: int | None = None,
) -> list[tuple[Any, str]]:
    """Fetch rows and return as (pk_value, label) pairs for form selects.

    Uses str(record) for the label when the model defines __str__.
    Falls back to "ClassName #pk" when the model relies on Pydantic's
    default string representation.
    """
    rows = await cls.all(order_by=order_by, limit=limit)
    pk = cls._pk_field()
    has_custom_str = cls.__str__ is not BaseModel.__str__
    return [
        (getattr(r, pk), str(r) if has_custom_str else f"{cls.__name__} #{getattr(r, pk)}")
        for r in rows
    ]
```

**Display labels.** Pydantic's default `__str__` produces a verbose representation like `Maker(id=1, name='Kuma-san')`, which makes for terrible dropdown options. `as_choices()` detects whether the model overrides `__str__` (by comparing against `BaseModel.__str__`) and falls back to `f"{ClassName} #{pk}"` when it doesn't. Users who want nice labels define `__str__`; users who don't still get a sensible default.

```html
<select name="maker_id">
    <option value="" disabled selected hidden>Select...</option>
    <option value="1">Kuma-san</option>
    <option value="2">Tanuki Mochi Co</option>
</select>
```

## What changes

#### 1. ForeignKey metadata class

In `src/air/field/types.py`:

```python
@dataclass(frozen=True, slots=True)
class ForeignKey(BasePresentation):
    """Marks this field as a foreign key to another AirModel.

    Affects DDL (emits REFERENCES constraint) and form rendering
    (renders as <select> with options fetched from the target).
    """
    to: type[AirModel] | str
    on_delete: Literal["cascade", "set_null", "restrict"] = "restrict"
```

`ForeignKey` inherits `BasePresentation` like `PrimaryKey` does. Both are structural in nature, but every consumer in the codebase checks for specific types (`isinstance(m, PrimaryKey)`, `isinstance(m, ForeignKey)`), not the base class. Introducing a second base class would add a classification decision for every future metadata type without a concrete consumer. If that changes, the base class split is a single-commit refactor.

**Resolution.** `resolve()` accepts the registry as a parameter to avoid circular imports between `field/types.py` and `model/main.py`. It searches the registry by class name (`cls.__name__`), not table name. When a string target is resolved, the result is cached on the instance via `object.__setattr__` (the standard Python pattern for lazy initialization on frozen objects). This is effectively a one-time class-level cache since `ForeignKey` instances are shared via `field_info.metadata`.

#### 2. AirField: new `foreign_key` and `on_delete` parameters

In `src/air/field/main.py`:

```python
def AirField(
    default: Any = ...,
    *,
    primary_key: bool = False,
    foreign_key: type | str | None = None,
    on_delete: Literal["cascade", "set_null", "restrict"] | None = None,
    type: str | None = None,
    label: str | None = None,
    ...
) -> Any:
```

Validation at call time:
- `foreign_key` and `choices` are mutually exclusive (raise `ValueError`)
- `foreign_key` and `primary_key` are mutually exclusive (raise `ValueError`)
- If `foreign_key` is a class (not a string), validate `issubclass(foreign_key, AirModel)` immediately. This catches `AirField(foreign_key=str)` or `AirField(foreign_key=42)` at definition time rather than at SQL generation.
- `on_delete` requires `foreign_key` (raise `ValueError` if set without it)
- `on_delete` defaults to `"restrict"` when `foreign_key` is provided without an explicit `on_delete`
- `on_delete="set_null"` requires a nullable field; validated at `_column_defs()` time when the annotation is available

#### 3. SQL generation

When a field has `ForeignKey` metadata, `_column_defs()` appends the `REFERENCES` and `ON DELETE` clause:

```sql
-- Required FK with cascade
"maker_id" INTEGER NOT NULL REFERENCES "mochi_maker"("id") ON DELETE CASCADE

-- Optional FK with set_null
"order_id" INTEGER REFERENCES "mochi_order"("id") ON DELETE SET NULL

-- Default (restrict)
"sponsor_id" INTEGER NOT NULL REFERENCES "mochi_sponsor"("id") ON DELETE RESTRICT
```

PostgreSQL enforces these constraints by default (no PRAGMA needed, unlike SQLite).

`_add_column_sql()` emits the same `REFERENCES ... ON DELETE` clause for new FK columns added via migration. `NOT NULL` is still omitted for ALTER TABLE (existing rows have no value for the new column).

#### 4. Table creation order

`create_tables()` currently iterates `_table_registry` in registration order. If `Dango` registers before `Maker`, the `REFERENCES` clause targets a table that doesn't exist yet. PostgreSQL rejects this.

`create_tables()` uses topological sort (Kahn's algorithm) to order models so FK targets are created before their dependents. Self-referential FKs are skipped when building the dependency graph (PostgreSQL allows a table's REFERENCES to point to itself within the same CREATE TABLE). Mutual FK cycles between two different models raise `ValueError`.

#### 5. FK indexes

PostgreSQL does not automatically create indexes on FK columns. Without an index, filtering or joining on a FK column does a sequential scan, and deleting a parent row scans the child table to check for references.

`create_tables()` emits `CREATE INDEX IF NOT EXISTS` for each FK column. The index name follows the pattern `idx_{table}_{column}`.

```sql
CREATE INDEX IF NOT EXISTS "idx_mochi_dango_maker_id" ON "mochi_dango"("maker_id")
```

## Deletion behavior

PostgreSQL's FK enforcement behavior is controlled by the `on_delete` parameter:

| `on_delete` | SQL clause | Behavior |
|---|---|---|
| `"restrict"` (default) | `ON DELETE RESTRICT` | Raises `asyncpg.ForeignKeyViolationError` if child rows exist |
| `"cascade"` | `ON DELETE CASCADE` | Deletes all child rows when the parent is deleted |
| `"set_null"` | `ON DELETE SET NULL` | Sets the FK column to NULL on child rows (field must be nullable) |

Air does not catch or wrap `ForeignKeyViolationError`; it propagates as a database error with PostgreSQL's native message.

```python
# Cascade: deleting a maker deletes all their dangos
maker_id: int = AirField(foreign_key=Maker, on_delete="cascade")

# Set null: deleting an order leaves dangos but clears the reference
order_id: int | None = AirField(default=None, foreign_key=Order, on_delete="set_null")

# Restrict (default): can't delete a maker with existing dangos
sponsor_id: int = AirField(foreign_key=Sponsor)
```

## Migration limitations

Adding `foreign_key=Maker` to an existing column that already has data requires care:

- **New column:** `_add_column_sql()` emits `REFERENCES` and `ON DELETE` in the `ALTER TABLE ADD COLUMN` statement. Works automatically.
- **Existing column:** If `maker_id` already exists in the database, `create_tables()` skips it (column already present). The `REFERENCES` constraint is never applied. Users must add the constraint manually:

```sql
ALTER TABLE "mochi_dango"
    ADD CONSTRAINT "fk_mochi_dango_maker_id"
    FOREIGN KEY ("maker_id") REFERENCES "mochi_maker"("id")
    ON DELETE CASCADE;
```

This is a known limitation. Air's migration system is additive (add columns, never drop or alter). Full schema migration (altering constraints, changing types, dropping columns) is out of scope and best handled by a dedicated migration tool.

## What this does NOT include

- **Composite foreign keys:** not needed, all PKs are single-column BIGSERIAL
- **Automatic option fetching in forms:** views pre-fetch FK choices explicitly. No hidden queries.
- **FK existence validation on form submit:** Pydantic validates the field as `int`. The database enforces the constraint. Air does not add a pre-INSERT query to check FK existence.
- **Constraint migration for existing columns:** see Migration limitations above
- **JOIN-based eager loading:** `select_related` uses batch queries (one per FK field), not SQL JOINs. JOINs change the result set shape and complicate row-to-model mapping. The batch approach is simpler and sufficient for typical use cases.

## Implementation plan

1. Add `ForeignKey` metadata class to `src/air/field/types.py` (with `resolve(registry)`, string support, `Literal` on_delete)
2. Add `foreign_key` and `on_delete` parameters to `AirField()` in `src/air/field/main.py` (with mutual-exclusivity, `issubclass`, and `on_delete` validation)
3. Update `_column_defs()` in `src/air/model/main.py` to emit `REFERENCES ... ON DELETE`
4. Update `_add_column_sql()` to emit `REFERENCES ... ON DELETE` for FK columns
5. Add `_topological_sort()` (with self-reference handling) and use it in `create_tables()`
6. Emit `CREATE INDEX IF NOT EXISTS` for FK columns in `create_tables()`
7. Add `as_choices()` class method to `AirModel` (with `order_by` and `limit`)
8. Add `related()` instance method to `AirModel`
9. Add `select_related` parameter to `all()`, `filter()`, and `get()` with `_load_related()` helper. **Remove the empty-kwargs delegation** at `filter()` (currently `if not kwargs: return await cls.all(...)`) so `select_related` is handled in one path. The delegation silently drops any new parameter that isn't explicitly forwarded, which is how a parameter like `select_related` can get lost. Each method handles its own query building.
10. Update `pydantic_type_to_html_type()` to return `"select"` for FK fields
11. Add `choices` parameter to `AirForm.__init__` with key validation. Grow the widget callable protocol to accept `choices`, thread it through `default_form_widget` to `_get_options` so dynamic choices take precedence over metadata.
12. Tests for each layer

## Test cases

```python
# --- Test fixtures ---

class Maker(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

    def __str__(self):
        return self.name

class Order(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    total_cents: int

class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker, on_delete="cascade")
    flavor: str

# --- SQL generation ---

sql = Dango._create_table_sql()
assert 'REFERENCES' in sql
assert '"maker_id" INTEGER NOT NULL REFERENCES' in sql
assert 'ON DELETE CASCADE' in sql

# Default on_delete is restrict
class DangoDefault(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker)

sql = DangoDefault._create_table_sql()
assert 'ON DELETE RESTRICT' in sql

# Optional FK with set_null
class DangoOptional(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order, on_delete="set_null")

sql = DangoOptional._create_table_sql()
assert '"order_id" INTEGER REFERENCES' in sql
assert 'NOT NULL' not in sql.split('order_id')[1].split('\n')[0]
assert 'ON DELETE SET NULL' in sql

# set_null on non-nullable field raises
class Bad(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker, on_delete="set_null")

with pytest.raises(ValueError, match="nullable"):
    Bad._create_table_sql()

# Multiple FKs to the same target
class User(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

class Document(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    created_by: int = AirField(foreign_key=User)
    updated_by: int = AirField(foreign_key=User)

sql = Document._create_table_sql()
assert sql.count('REFERENCES') == 2
assert '"created_by" INTEGER NOT NULL REFERENCES' in sql
assert '"updated_by" INTEGER NOT NULL REFERENCES' in sql

# Self-referential FK
class Category(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str
    parent_id: int | None = AirField(default=None, foreign_key="Category", on_delete="cascade")

sql = Category._create_table_sql()
assert 'REFERENCES' in sql
assert '"parent_id" INTEGER REFERENCES' in sql
assert 'ON DELETE CASCADE' in sql

# --- Forward references ---

class Child(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    parent_id: int = AirField(foreign_key="Parent")

class Parent(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

# Resolves at SQL generation time, not definition time
sql = Child._create_table_sql()
assert 'REFERENCES' in sql

# Unresolvable string reference
class Orphan(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    bad_id: int = AirField(foreign_key="DoesNotExist")

with pytest.raises(ValueError, match="not found in registered models"):
    Orphan._create_table_sql()

# --- Validation ---

# Mutual exclusivity: foreign_key + choices
with pytest.raises(ValueError, match="mutually exclusive"):
    AirField(foreign_key=Maker, choices=[(1, "a")])

# Mutual exclusivity: foreign_key + primary_key
with pytest.raises(ValueError, match="mutually exclusive"):
    AirField(foreign_key=Maker, primary_key=True)

# Non-AirModel class reference
with pytest.raises(TypeError, match="AirModel subclass"):
    AirField(foreign_key=str)

# Non-class, non-string reference
with pytest.raises(TypeError, match="AirModel subclass"):
    AirField(foreign_key=42)

# on_delete without foreign_key
with pytest.raises(ValueError, match="on_delete requires foreign_key"):
    AirField(on_delete="cascade")

# Invalid on_delete value (caught by Literal type at type-check time,
# validated at runtime as a belt-and-suspenders check)
with pytest.raises(ValueError, match="on_delete must be one of"):
    AirField(foreign_key=Maker, on_delete="destroy")

# --- Topological sort ---

sorted_classes = _topological_sort([Dango, Maker])
assert sorted_classes.index(Maker) < sorted_classes.index(Dango)

# Self-referential FK does not cause circular dependency error
sorted_classes = _topological_sort([Category])
assert sorted_classes == [Category]

# --- ALTER TABLE ---

sql = Dango._add_column_sql("maker_id")
assert 'REFERENCES' in sql
assert 'ON DELETE CASCADE' in sql

# --- Reverse relations ---

# maker.related(Dango) returns all dangos for this maker
maker = await Maker.create(name="Kuma-san")
d1 = await Dango.create(maker_id=maker.id, flavor="matcha")
d2 = await Dango.create(maker_id=maker.id, flavor="sakura")
dangos = await maker.related(Dango)
assert len(dangos) == 2

# related() with ordering and limit
dangos = await maker.related(Dango, order_by="flavor", limit=1)
assert len(dangos) == 1
assert dangos[0].flavor == "matcha"

# related() raises on no FK
with pytest.raises(ValueError, match="no foreign key"):
    await maker.related(Order)

# related() raises on ambiguous FK (multiple FKs to same target)
user = await User.create(name="Audrey")
with pytest.raises(ValueError, match="multiple foreign keys"):
    await user.related(Document)

# related() raises on unsaved instance
unsaved = Maker(name="test")
with pytest.raises(ValueError, match="primary key value"):
    await unsaved.related(Dango)

# --- Select related ---

# Eagerly load maker for each dango (relation name, not field name)
dangos = await Dango.all(select_related=["maker"])
assert dangos[0].maker.name == "Kuma-san"

# select_related with filter
dangos = await Dango.filter(flavor="matcha", select_related=["maker"])
assert dangos[0].maker.name == "Kuma-san"

# select_related with get
dango = await Dango.get(id=d1.id, select_related=["maker"])
assert dango.maker.name == "Kuma-san"

# select_related with optional FK (None value)
class DangoWithOptional(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order, on_delete="set_null")

d = await DangoWithOptional.create()
results = await DangoWithOptional.all(select_related=["order"])
assert results[0].order is None

# Eagerly-loaded attributes are excluded from model_dump()
dango = await Dango.get(id=d1.id, select_related=["maker"])
dumped = dango.model_dump()
assert "maker" not in dumped
assert "maker_id" in dumped

# Invalid relation name in select_related
with pytest.raises(ValueError, match="Unknown"):
    await Dango.all(select_related=["nonexistent"])

# Non-FK field in select_related
with pytest.raises(ValueError, match="not a foreign key"):
    await Dango.all(select_related=["flavor"])

# --- Form rendering ---

form = DangoForm(choices={"maker_id": [(1, "Kuma-san"), (2, "Tanuki")]})
html = form.render()
assert '<select' in html
assert 'name="maker_id"' in html
assert 'Kuma-san' in html

# Edit form pre-selects current value
form = DangoForm(
    initial_data={"maker_id": 2},
    choices={"maker_id": [(1, "Kuma-san"), (2, "Tanuki")]},
)
html = form.render()
assert 'value="2" selected' in html or 'value="2"selected' in html

# Misspelled choices key raises immediately
with pytest.raises(ValueError, match="maker_di"):
    DangoForm(choices={"maker_di": [(1, "Kuma-san")]})

# --- as_choices helper ---

choices = await Maker.as_choices()
assert choices == [(1, "Kuma-san"), (2, "Tanuki Mochi Co")]

# With ordering
choices = await Maker.as_choices(order_by="name")
assert choices[0][1] == "Kuma-san"  # alphabetical

# With limit
choices = await Maker.as_choices(limit=1)
assert len(choices) == 1
```
