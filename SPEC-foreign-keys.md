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
    maker_id: int = AirField(foreign_key=Maker, label="Maker")
    flavor: str
    order_id: int | None = AirField(default=None, foreign_key=Order)
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
    parent_id: int | None = AirField(default=None, foreign_key="Category")
```

Self-references must use a string to avoid `NameError` (the class doesn't exist yet when its body executes). The topological sort skips self-references when building the dependency graph (a model is not a dependency of itself).

### What changes

#### 1. ForeignKey metadata class

In `src/air/field/types.py`:

```python
@dataclass(frozen=True, slots=True)
class ForeignKey(BasePresentation):
    """Marks this field as a foreign key to another AirModel.

    Affects DDL (emits REFERENCES constraint) and form rendering
    (renders as <select> with options fetched from the target).
    """
    to: type[AirModel] | str  # Class or string name for forward refs
```

`ForeignKey` inherits `BasePresentation` like `PrimaryKey` does. Both are structural in nature, but every consumer in the codebase checks for specific types (`isinstance(m, PrimaryKey)`, `isinstance(m, ForeignKey)`), not the base class. Introducing a second base class would add a classification decision for every future metadata type without a concrete consumer. If that changes, the base class split is a single-commit refactor.

**Resolution.** `resolve()` accepts the registry as a parameter to avoid circular imports between `field/types.py` and `model/main.py`:

```python
def resolve(self, registry: list[type]) -> type:
    """Return the resolved AirModel class.

    Args:
        registry: The model registry (_table_registry from model/main.py).

    Raises:
        ValueError: If the string target is not found in the registry.
    """
    if isinstance(self.to, str):
        for cls in registry:
            if cls.__name__ == self.to:
                object.__setattr__(self, 'to', cls)
                return cls
        msg = f"ForeignKey target '{self.to}' not found in registered models"
        raise ValueError(msg)
    return self.to
```

The `object.__setattr__` on a frozen dataclass is the standard Python pattern for lazy initialization on immutable objects (`functools.cached_property` does the same thing). `ForeignKey` instances live in `field_info.metadata` and are shared across all uses of a model class, so this is effectively a one-time class-level cache.

Callers pass the registry explicitly:

```python
# In _column_defs, _add_column_sql, _topological_sort:
from air.model.main import _table_registry
target = fk.resolve(_table_registry)
```

#### 2. AirField: new `foreign_key` parameter

In `src/air/field/main.py`:

```python
def AirField(
    default: Any = ...,
    *,
    primary_key: bool = False,
    foreign_key: type | str | None = None,   # NEW
    type: str | None = None,
    label: str | None = None,
    ...
) -> Any:
```

Validation at call time:
- `foreign_key` and `choices` are mutually exclusive (raise `ValueError`)
- `foreign_key` and `primary_key` are mutually exclusive (raise `ValueError`)
- If `foreign_key` is a class (not a string), validate `issubclass(foreign_key, AirModel)` immediately. This catches `AirField(foreign_key=str)` or `AirField(foreign_key=42)` at definition time rather than at SQL generation.

```python
if foreign_key is not None:
    if choices:
        msg = "foreign_key and choices are mutually exclusive"
        raise ValueError(msg)
    if primary_key:
        msg = "foreign_key and primary_key are mutually exclusive"
        raise ValueError(msg)
    if isinstance(foreign_key, str):
        # String forward reference, validated lazily at resolve() time
        field_info.metadata.append(ForeignKey(to=foreign_key))
    else:
        if not (isinstance(foreign_key, type) and issubclass(foreign_key, AirModel)):
            msg = f"foreign_key must be an AirModel subclass or string, got {foreign_key!r}"
            raise TypeError(msg)
        field_info.metadata.append(ForeignKey(to=foreign_key))
```

#### 3. SQL generation: REFERENCES constraint

In `_column_defs()`, when a field has `ForeignKey` metadata, append the constraint:

```python
# After determining pg_type and constraint...
fk = next((m for m in field_info.metadata if isinstance(m, ForeignKey)), None)
if fk:
    target = fk.resolve(_table_registry)
    target_table = target._table_name()
    target_pk = target._pk_field()
    constraint += f' REFERENCES "{target_table}"("{target_pk}")'
```

Produces:
```sql
-- Required FK
"maker_id" INTEGER NOT NULL REFERENCES "mochi_maker"("id")

-- Optional FK (int | None)
"order_id" INTEGER REFERENCES "mochi_order"("id")
```

PostgreSQL enforces these constraints by default (no PRAGMA needed, unlike SQLite).

#### 4. Table creation order: topological sort

`create_tables()` currently iterates `_table_registry` in registration order. If `Dango` registers before `Maker`, the `REFERENCES` clause targets a table that doesn't exist yet. PostgreSQL rejects this.

Add topological sorting in `create_tables()`:

```python
async def create_tables(self) -> None:
    ordered = _topological_sort(_table_registry)
    for table_cls in ordered:
        sql = table_cls._create_table_sql()
        await self.pool.execute(sql)
        # ... existing migration logic
```

The sort function skips self-references (a model is not a dependency of itself):

```python
def _topological_sort(classes: list[type[AirModel]]) -> list[type[AirModel]]:
    """Sort model classes so that FK targets come before dependents.

    Self-referential FKs (e.g., Category -> Category) are skipped
    when building the dependency graph. PostgreSQL allows a table's
    REFERENCES to point to itself within the same CREATE TABLE.
    """
    # Build adjacency: cls -> set of classes it depends on
    deps: dict[type, set[type]] = {}
    for cls in classes:
        deps[cls] = set()
        for field_info in cls.model_fields.values():
            for m in field_info.metadata:
                if isinstance(m, ForeignKey):
                    target = m.resolve(_table_registry)
                    if target in classes and target is not cls:
                        deps[cls].add(target)

    # Kahn's algorithm
    result: list[type[AirModel]] = []
    in_degree = {cls: len(d) for cls, d in deps.items()}
    queue = [cls for cls, deg in in_degree.items() if deg == 0]
    while queue:
        cls = queue.pop(0)
        result.append(cls)
        for other, other_deps in deps.items():
            if cls in other_deps:
                in_degree[other] -= 1
                if in_degree[other] == 0:
                    queue.append(other)

    if len(result) != len(classes):
        msg = "Circular foreign key dependency detected"
        raise ValueError(msg)
    return result
```

#### 5. `_add_column_sql`: REFERENCES for new FK columns

`_add_column_sql()` currently emits bare `ALTER TABLE ADD COLUMN "x" TYPE`. When the new column has `ForeignKey` metadata, append the constraint:

```python
@classmethod
def _add_column_sql(cls, field_name: str) -> str:
    field_info = cls.model_fields[field_name]
    annotation = field_info.annotation
    base_type = _unwrap_optional(annotation) if _is_optional(annotation) else annotation
    pg_type = _pg_type(base_type)
    sql = f'ALTER TABLE "{cls._table_name()}" ADD COLUMN "{field_name}" {pg_type}'

    fk = next((m for m in field_info.metadata if isinstance(m, ForeignKey)), None)
    if fk:
        target = fk.resolve(_table_registry)
        sql += f' REFERENCES "{target._table_name()}"("{target._pk_field()}")'
    return sql
```

Note: `NOT NULL` is still omitted for ALTER TABLE (existing rows have no value). This is the existing behavior and correct for migrations.

#### 6. `_meta_dict` update for ForeignKey visibility

The form's `_meta_dict` helper (`form/main.py:69`) builds a metadata lookup dict filtered by `isinstance(m, BasePresentation)`. Since `ForeignKey` inherits `BasePresentation`, it will be visible to the form rendering pipeline. `pydantic_type_to_html_type()` and `_get_options()` can find it via the existing `_meta_dict` and `_get_meta` helpers with no changes to the lookup function.

#### 7. AirForm: render FK fields as `<select>`

This is the hardest part. `render()` is sync. Fetching FK options requires a database query (async). Two clean options exist:

**Option A: Make `render()` async.** `render()` becomes `async def render(self)`, callers write `await form.render()`. This is the honest approach (fetching rows is I/O), but breaks every existing `form.render()` call.

**Option B: Accept choices from the view.** Keep `render()` sync. The view pre-fetches FK options and passes them in:

```python
# In the view (already async)
makers = await Maker.all()
form = DangoForm(
    choices={"maker_id": [(m.id, str(m)) for m in makers]}
)
html = form.render()  # stays sync
```

**Decision: Option B.** It keeps `render()` sync, puts async I/O in the view where it belongs, and gives users control over queries (filtering, limits, ordering). The form shouldn't hide database queries.

Implementation:

1. `AirForm.__init__` accepts an optional `choices: dict[str, list[tuple[Any, str]]]` parameter for dynamic choice overrides. This works for FK fields and for any field where choices need to be computed at render time. One mechanism, not two.

2. On `__init__`, validate that every key in `choices` corresponds to an actual field on the model. Raise `ValueError` on unknown keys so typos like `choices={"maker_di": [...]}` fail immediately instead of rendering an empty select.

3. In `render()`, before calling the widget, inject `Choices` metadata for fields that have dynamic choices:

```python
def render(self) -> str:
    # ... existing CSRF logic ...

    # Inject dynamic choices as Choices metadata
    effective_model = self.model
    if self._choices:
        effective_model = self._inject_choices()

    fields_html = self.widget(
        model=effective_model,
        data=render_data,
        errors=self.errors,
        excludes=self._display_excludes or None,
    )
    return SafeHTML(f"{csrf_html}\n{fields_html}")
```

4. `pydantic_type_to_html_type()`: when `ForeignKey` metadata is present, return `"select"`. This makes FK fields render as selects. If no dynamic choices were provided, the select renders with just the "Select..." placeholder, signaling a missing `choices` argument.

5. `_get_options()`: when `Choices` metadata is present (injected from dynamic choices), use it. This is already the existing code path. No changes needed.

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

    Uses str(record) for the label. Define __str__ on the model
    to control the display. Falls back to "ClassName #pk".

    Args:
        order_by: Optional field name to sort by. Prefix with "-"
            for descending.
        limit: Maximum number of options to return.
    """
    rows = await cls.all(order_by=order_by, limit=limit)
    pk = cls._pk_field()
    return [(getattr(r, pk), str(r)) for r in rows]
```

Usage in a view:

```python
async def dango_form_view(request):
    form = DangoForm(
        choices={"maker_id": await Maker.as_choices(order_by="name")}
    )
    return templates.TemplateResponse(request, "form.html", {"form": form})
```

#### 8. Display labels for FK options

AirModel gets an optional `__str__` convention. If the referenced model defines `__str__`, use it for the option label. Otherwise fall back to `f"{model.__name__} #{pk}"`.

```python
class Maker(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

    def __str__(self):
        return self.name
```

The `<select>` renders:

```html
<select name="maker_id">
    <option value="" disabled selected hidden>Select...</option>
    <option value="1">Kuma-san</option>
    <option value="2">Tanuki Mochi Co</option>
</select>
```

#### 9. FK indexes

PostgreSQL does not automatically create indexes on FK columns. Without an index, filtering or joining on a FK column does a sequential scan, and deleting a parent row scans the child table to check for references.

`_column_defs()` and `_add_column_sql()` should record FK columns, and `create_tables()` should emit `CREATE INDEX IF NOT EXISTS` for each:

```sql
CREATE INDEX IF NOT EXISTS "idx_mochi_dango_maker_id" ON "mochi_dango"("maker_id")
```

The index name follows the pattern `idx_{table}_{column}`.

## Deletion behavior

The spec explicitly does not include cascading deletes. PostgreSQL's default FK enforcement is `NO ACTION` (equivalent to `RESTRICT` at end-of-statement). This means:

- Deleting a parent row that is still referenced by child rows raises `asyncpg.ForeignKeyViolationError`
- Users must delete or reassign child rows before deleting the parent
- Air does not catch or wrap this error; it propagates as a database error with PostgreSQL's native message

A future `on_delete` parameter can change this behavior (e.g., `CASCADE`, `SET NULL`). That is a separate feature.

## Migration limitations

Adding `foreign_key=Maker` to an existing column that already has data requires care:

- **New column:** `_add_column_sql()` emits `REFERENCES` in the `ALTER TABLE ADD COLUMN` statement. Works automatically.
- **Existing column:** If `maker_id` already exists in the database, `create_tables()` skips it (column already present). The `REFERENCES` constraint is never applied. Users must add the constraint manually:

```sql
ALTER TABLE "mochi_dango"
    ADD CONSTRAINT "fk_mochi_dango_maker_id"
    FOREIGN KEY ("maker_id") REFERENCES "mochi_maker"("id");
```

This is a known limitation. Air's migration system is additive (add columns, never drop or alter). Full schema migration (altering constraints, changing types, dropping columns) is out of scope and best handled by a dedicated migration tool.

## What this does NOT include

- **Cascading deletes:** handle at the application level or add later with `on_delete` parameter
- **Reverse relations** (e.g., `user.repos`): a separate feature
- **Join queries / select_related:** a separate feature
- **Composite foreign keys:** not needed, all PKs are single-column BIGSERIAL
- **Automatic option fetching in forms:** views pre-fetch FK choices explicitly. No hidden queries.
- **FK existence validation on form submit:** Pydantic validates the field as `int`. The database enforces the constraint. Air does not add a pre-INSERT query to check FK existence.
- **Constraint migration for existing columns:** see Migration limitations above

## Implementation plan

1. Add `ForeignKey` metadata class to `src/air/field/types.py` (with `resolve(registry)` and string support)
2. Add `foreign_key` parameter to `AirField()` in `src/air/field/main.py` (with mutual-exclusivity and `issubclass` validation)
3. Update `_column_defs()` in `src/air/model/main.py` to emit `REFERENCES`
4. Update `_add_column_sql()` to emit `REFERENCES` for FK columns
5. Add `_topological_sort()` (with self-reference handling) and use it in `create_tables()`
6. Emit `CREATE INDEX IF NOT EXISTS` for FK columns in `create_tables()`
7. Add `as_choices()` class method to `AirModel` (with `order_by` and `limit`)
8. Update `pydantic_type_to_html_type()` to return `"select"` for FK fields
9. Add `choices` parameter to `AirForm.__init__` with key validation, inject into rendering
10. Tests for each layer

## Test cases

```python
# --- SQL generation ---

class Maker(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker)

sql = Dango._create_table_sql()
assert 'REFERENCES' in sql
assert '"maker_id" INTEGER NOT NULL REFERENCES' in sql

# Optional FK
class DangoOptional(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order)

sql = DangoOptional._create_table_sql()
assert '"order_id" INTEGER REFERENCES' in sql
assert 'NOT NULL' not in sql.split('order_id')[1].split('\n')[0]

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
    parent_id: int | None = AirField(default=None, foreign_key="Category")

sql = Category._create_table_sql()
assert 'REFERENCES' in sql
assert '"parent_id" INTEGER REFERENCES' in sql

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

# --- Topological sort ---

sorted_classes = _topological_sort([Dango, Maker])
assert sorted_classes.index(Maker) < sorted_classes.index(Dango)

# Self-referential FK does not cause circular dependency error
sorted_classes = _topological_sort([Category])
assert sorted_classes == [Category]

# --- ALTER TABLE ---

sql = Dango._add_column_sql("maker_id")
assert 'REFERENCES' in sql

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
