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
    on_delete: str = "restrict"  # "cascade", "set_null", or "restrict"
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

#### 2. AirField: new `foreign_key` and `on_delete` parameters

In `src/air/field/main.py`:

```python
def AirField(
    default: Any = ...,
    *,
    primary_key: bool = False,
    foreign_key: type | str | None = None,   # NEW
    on_delete: str | None = None,            # NEW
    type: str | None = None,
    label: str | None = None,
    ...
) -> Any:
```

Validation at call time:
- `foreign_key` and `choices` are mutually exclusive (raise `ValueError`)
- `foreign_key` and `primary_key` are mutually exclusive (raise `ValueError`)
- If `foreign_key` is a class (not a string), validate `issubclass(foreign_key, AirModel)` immediately. This catches `AirField(foreign_key=str)` or `AirField(foreign_key=42)` at definition time rather than at SQL generation.
- `on_delete` requires `foreign_key` (raise `ValueError` if `on_delete` is set without `foreign_key`)
- `on_delete` must be one of `"cascade"`, `"set_null"`, `"restrict"` (raise `ValueError` otherwise)
- `on_delete="set_null"` requires a nullable field; validated at `_column_defs()` time when the annotation is available

```python
_VALID_ON_DELETE = {"cascade", "set_null", "restrict"}

if foreign_key is not None:
    if choices:
        msg = "foreign_key and choices are mutually exclusive"
        raise ValueError(msg)
    if primary_key:
        msg = "foreign_key and primary_key are mutually exclusive"
        raise ValueError(msg)
    delete_rule = on_delete or "restrict"
    if delete_rule not in _VALID_ON_DELETE:
        msg = f"on_delete must be one of {_VALID_ON_DELETE}, got {delete_rule!r}"
        raise ValueError(msg)
    if isinstance(foreign_key, str):
        field_info.metadata.append(ForeignKey(to=foreign_key, on_delete=delete_rule))
    else:
        if not (isinstance(foreign_key, type) and issubclass(foreign_key, AirModel)):
            msg = f"foreign_key must be an AirModel subclass or string, got {foreign_key!r}"
            raise TypeError(msg)
        field_info.metadata.append(ForeignKey(to=foreign_key, on_delete=delete_rule))
elif on_delete is not None:
    msg = "on_delete requires foreign_key"
    raise ValueError(msg)
```

#### 3. SQL generation: REFERENCES constraint with ON DELETE

In `_column_defs()`, when a field has `ForeignKey` metadata, append the constraint:

```python
_ON_DELETE_SQL = {
    "cascade": "CASCADE",
    "set_null": "SET NULL",
    "restrict": "RESTRICT",
}

# After determining pg_type and constraint...
fk = next((m for m in field_info.metadata if isinstance(m, ForeignKey)), None)
if fk:
    target = fk.resolve(_table_registry)
    target_table = target._table_name()
    target_pk = target._pk_field()
    on_delete_sql = _ON_DELETE_SQL[fk.on_delete]
    constraint += f' REFERENCES "{target_table}"("{target_pk}") ON DELETE {on_delete_sql}'
    if fk.on_delete == "set_null" and not nullable:
        msg = f'on_delete="set_null" requires {field_name} to be nullable (int | None)'
        raise ValueError(msg)
```

Produces:
```sql
-- Required FK with cascade
"maker_id" INTEGER NOT NULL REFERENCES "mochi_maker"("id") ON DELETE CASCADE

-- Optional FK with set_null
"order_id" INTEGER REFERENCES "mochi_order"("id") ON DELETE SET NULL

-- Default (restrict)
"sponsor_id" INTEGER NOT NULL REFERENCES "mochi_sponsor"("id") ON DELETE RESTRICT
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

`_add_column_sql()` currently emits bare `ALTER TABLE ADD COLUMN "x" TYPE`. When the new column has `ForeignKey` metadata, append the constraint including ON DELETE:

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
        on_delete_sql = _ON_DELETE_SQL[fk.on_delete]
        sql += f' REFERENCES "{target._table_name()}"("{target._pk_field()}") ON DELETE {on_delete_sql}'
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

#### 10. Reverse relations

A parent model can query its children through FK metadata. This uses the FK declarations that already exist on the child models, so no new declarations are needed on the parent.

```python
# Get all dangos for a specific maker
maker = await Maker.get(id=1)
dangos = await maker.related(Dango)

# Equivalent to:
dangos = await Dango.filter(maker_id=1)
```

Implementation as an instance method on `AirModel`:

```python
async def related(
    self,
    child_model: type[AirModel],
    *,
    order_by: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[AirModel]:
    """Fetch child records that reference this instance via a foreign key.

    Discovers which field on child_model points to this model's class
    via ForeignKey metadata, then filters by this instance's PK value.

    Args:
        child_model: The AirModel subclass that has a FK to this model.
        order_by: Optional sort field. Prefix with "-" for descending.
        limit: Maximum number of rows.
        offset: Number of rows to skip.

    Raises:
        ValueError: If child_model has no FK pointing to this model,
            or if this instance has no PK value.
        ValueError: If child_model has multiple FKs to this model
            (use filter() directly with the specific field name).
    """
    my_cls = type(self)
    pk = self._pk_field()
    pk_value = getattr(self, pk)
    if pk_value is None:
        msg = "Cannot query related objects without a primary key value."
        raise ValueError(msg)

    # Find FK fields on child_model that point to my class
    fk_fields = []
    for field_name, field_info in child_model.model_fields.items():
        for m in field_info.metadata:
            if isinstance(m, ForeignKey):
                target = m.resolve(_table_registry)
                if target is my_cls:
                    fk_fields.append(field_name)

    if not fk_fields:
        msg = f"{child_model.__name__} has no foreign key to {my_cls.__name__}"
        raise ValueError(msg)
    if len(fk_fields) > 1:
        msg = (
            f"{child_model.__name__} has multiple foreign keys to {my_cls.__name__} "
            f"({', '.join(fk_fields)}). Use {child_model.__name__}.filter() with "
            f"the specific field name instead."
        )
        raise ValueError(msg)

    return await child_model.filter(
        order_by=order_by, limit=limit, offset=offset,
        **{fk_fields[0]: pk_value},
    )
```

When a child model has multiple FKs to the same parent (e.g., `created_by` and `updated_by` both pointing to `User`), `related()` raises an error directing the user to `filter()` with the specific field name:

```python
# Ambiguous: Document has created_by and updated_by, both FK to User
# This raises ValueError with a helpful message:
docs = await user.related(Document)

# Use filter() instead:
created = await Document.filter(created_by=user.id)
updated = await Document.filter(updated_by=user.id)
```

#### 11. Select related (eager loading)

Fetching a list of dangos and then querying each one's maker is N+1 queries. `select_related` fetches parent records in a single extra query per FK field and attaches them to each instance.

```python
dangos = await Dango.all(select_related=["maker_id"])
# Each dango now has dango.maker_ as a Maker instance
print(dangos[0].maker_.name)  # "Kuma-san"
```

The attribute name is the FK field name with `_id` stripped and `_` appended: `maker_id` becomes `maker_`. The trailing underscore avoids colliding with fields the model might already have (e.g., a `maker` field of a different type). If the FK field doesn't end in `_id`, the attribute is `{field_name}_rel` (e.g., `sponsor` becomes `sponsor_rel`).

**Implementation strategy: batch query, not JOIN.**

JOINs change the shape of the result set and complicate the ORM's row-to-model mapping. Instead, use a separate query per FK field:

```python
@classmethod
async def all(
    cls,
    *,
    order_by: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    select_related: list[str] | None = None,
) -> list[Self]:
    # ... existing query logic to get rows ...
    instances = [cls.model_validate(dict(r)) for r in rows]

    if select_related:
        await cls._load_related(instances, select_related)

    return instances
```

The `_load_related` class method:

```python
@classmethod
async def _load_related(cls, instances: list[Self], fields: list[str]) -> None:
    """Eagerly load related objects for FK fields.

    For each FK field, collects all unique FK values from instances,
    fetches the referenced records in one query, and attaches them.
    """
    for field_name in fields:
        field_info = cls.model_fields.get(field_name)
        if field_info is None:
            msg = f"Unknown field '{field_name}' in select_related"
            raise ValueError(msg)
        fk = next((m for m in field_info.metadata if isinstance(m, ForeignKey)), None)
        if fk is None:
            msg = f"Field '{field_name}' is not a foreign key"
            raise ValueError(msg)

        target = fk.resolve(_table_registry)
        target_pk = target._pk_field()

        # Collect unique FK values (skip None for optional FKs)
        fk_values = list({getattr(inst, field_name) for inst in instances
                         if getattr(inst, field_name) is not None})
        if not fk_values:
            continue

        # One query for all referenced records
        related_records = await target.filter(**{f"{target_pk}__in": fk_values})
        lookup = {getattr(r, target_pk): r for r in related_records}

        # Determine attribute name
        if field_name.endswith("_id"):
            attr = field_name[:-3] + "_"
        else:
            attr = field_name + "_rel"

        # Attach to each instance
        for inst in instances:
            fk_val = getattr(inst, field_name)
            object.__setattr__(inst, attr, lookup.get(fk_val))
```

This produces at most N+1 queries where N is the number of `select_related` fields (typically 1-3), not N+1 where N is the number of rows.

`filter()` and `get()` also accept `select_related`:

```python
dangos = await Dango.filter(flavor="matcha", select_related=["maker_id"])
dango = await Dango.get(id=1, select_related=["maker_id"])
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

1. Add `ForeignKey` metadata class to `src/air/field/types.py` (with `resolve(registry)`, string support, and `on_delete`)
2. Add `foreign_key` and `on_delete` parameters to `AirField()` in `src/air/field/main.py` (with mutual-exclusivity, `issubclass`, and `on_delete` validation)
3. Update `_column_defs()` in `src/air/model/main.py` to emit `REFERENCES ... ON DELETE`
4. Update `_add_column_sql()` to emit `REFERENCES ... ON DELETE` for FK columns
5. Add `_topological_sort()` (with self-reference handling) and use it in `create_tables()`
6. Emit `CREATE INDEX IF NOT EXISTS` for FK columns in `create_tables()`
7. Add `as_choices()` class method to `AirModel` (with `order_by` and `limit`)
8. Add `related()` instance method to `AirModel`
9. Add `select_related` parameter to `all()`, `filter()`, and `get()` with `_load_related()` helper
10. Update `pydantic_type_to_html_type()` to return `"select"` for FK fields
11. Add `choices` parameter to `AirForm.__init__` with key validation, inject into rendering
12. Tests for each layer

## Test cases

```python
# --- SQL generation ---

class Maker(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    maker_id: int = AirField(foreign_key=Maker, on_delete="cascade")

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

# Invalid on_delete value
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

# Eagerly load maker for each dango
dangos = await Dango.all(select_related=["maker_id"])
assert hasattr(dangos[0], "maker_")
assert dangos[0].maker_.name == "Kuma-san"

# select_related with filter
dangos = await Dango.filter(flavor="matcha", select_related=["maker_id"])
assert dangos[0].maker_.name == "Kuma-san"

# select_related with get
dango = await Dango.get(id=d1.id, select_related=["maker_id"])
assert dango.maker_.name == "Kuma-san"

# select_related with optional FK (None value)
class DangoWithOptional(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order, on_delete="set_null")

d = await DangoWithOptional.create()
results = await DangoWithOptional.all(select_related=["order_id"])
assert results[0].order_rel is None  # no _id suffix, so attr is order_rel... wait

# Attribute naming: maker_id -> maker_, order_id -> order_, sponsor -> sponsor_rel
assert hasattr(dangos[0], "maker_")  # maker_id -> maker_

# Invalid field in select_related
with pytest.raises(ValueError, match="Unknown field"):
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
