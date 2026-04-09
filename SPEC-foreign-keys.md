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

### What changes

#### 1. New base class for structural metadata

`ForeignKey` is a structural constraint (affects SQL generation and referential integrity), not presentation metadata. `BasePresentation` is the wrong base.

In `src/air/field/types.py`, add a new base class above `BasePresentation`:

```python
class BaseStructure:
    """Base class for structural metadata that affects storage/schema.

    Distinct from BasePresentation, which affects rendering only.
    Consumers can check isinstance(m, BaseStructure) to find
    metadata that changes DDL or database behavior.
    """
    __slots__ = ()
```

Move `PrimaryKey` from `BasePresentation` to `BaseStructure` (it's structural too). This is backwards-compatible: code checking `isinstance(m, BasePresentation)` should also check `isinstance(m, BaseStructure)`, or better, check for the specific type directly (which existing code already does).

#### 2. ForeignKey metadata class

In `src/air/field/types.py`:

```python
@dataclass(frozen=True, slots=True)
class ForeignKey(BaseStructure):
    """Marks this field as a foreign key to another AirModel.

    Affects DDL (emits REFERENCES constraint) and form rendering
    (renders as <select> with options fetched from the target).
    """
    to: type[AirModel] | str  # Class or string name for forward refs
```

When `to` is a string, it resolves against `_table_registry` on first access. A `resolve()` method handles this:

```python
def resolve(self) -> type[AirModel]:
    """Return the resolved AirModel class. Raises if not found."""
    if isinstance(self.to, str):
        for cls in _table_registry:
            if cls.__name__ == self.to:
                # Cache the resolved class
                object.__setattr__(self, 'to', cls)
                return cls
        msg = f"ForeignKey target '{self.to}' not found in registered models"
        raise ValueError(msg)
    return self.to
```

Note: `_table_registry` is in `src/air/model/main.py`. To avoid circular imports, `ForeignKey.resolve()` imports it lazily or accepts the registry as a parameter.

#### 3. AirField: new `foreign_key` parameter

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

When `foreign_key` is provided:
```python
if foreign_key is not None:
    if choices:
        msg = "foreign_key and choices are mutually exclusive"
        raise ValueError(msg)
    if primary_key:
        msg = "foreign_key and primary_key are mutually exclusive"
        raise ValueError(msg)
    field_info.metadata.append(ForeignKey(to=foreign_key))
```

#### 4. SQL generation: REFERENCES constraint

In `_column_defs()`, when a field has `ForeignKey` metadata, append the constraint:

```python
# After determining pg_type and constraint...
fk = next((m for m in field_info.metadata if isinstance(m, ForeignKey)), None)
if fk:
    target = fk.resolve()
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

#### 5. Table creation order: topological sort

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

The sort function:

```python
def _topological_sort(classes: list[type[AirModel]]) -> list[type[AirModel]]:
    """Sort model classes so that FK targets come before dependents."""
    # Build adjacency: cls -> set of classes it depends on
    deps: dict[type, set[type]] = {}
    for cls in classes:
        deps[cls] = set()
        for field_info in cls.model_fields.values():
            for m in field_info.metadata:
                if isinstance(m, ForeignKey):
                    target = m.resolve()
                    if target in classes:
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

#### 6. `_add_column_sql`: REFERENCES for new FK columns

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
        target = fk.resolve()
        sql += f' REFERENCES "{target._table_name()}"("{target._pk_field()}")'
    return sql
```

Note: `NOT NULL` is still omitted for ALTER TABLE (existing rows have no value). This is the existing behavior and correct for migrations.

#### 7. AirForm: render FK fields as `<select>`

This is the hardest part. `render()` is sync. Fetching FK options requires a database query (async). Two clean options exist:

**Option A: Make `render()` async.** `render()` becomes `async def render(self)`, callers write `await form.render()`. This is the honest approach (fetching rows is I/O), but breaks every existing `form.render()` call.

**Option B: Accept choices from the view.** Keep `render()` sync. The view pre-fetches FK options and passes them in:

```python
# In the view (already async)
makers = await Maker.all()
form = DangoForm(
    fk_choices={"maker_id": [(m.id, str(m)) for m in makers]}
)
html = form.render()  # stays sync
```

**Decision: Option B.** It keeps `render()` sync, puts async I/O in the view where it belongs, and gives users control over queries (filtering, limits, ordering). The form shouldn't hide database queries.

Implementation:

1. `AirForm.__init__` accepts an optional `fk_choices: dict[str, list[tuple[Any, str]]]` parameter.

2. In `render()`, before calling the widget, inject `Choices` metadata for FK fields that have pre-fetched options:

```python
def render(self) -> str:
    # ... existing CSRF logic ...

    # Inject FK choices as Choices metadata
    effective_model = self.model
    if self._fk_choices:
        effective_model = self._inject_fk_choices()

    fields_html = self.widget(
        model=effective_model,
        data=render_data,
        errors=self.errors,
        excludes=self._display_excludes or None,
    )
    return SafeHTML(f"{csrf_html}\n{fields_html}")
```

3. `pydantic_type_to_html_type()`: when `ForeignKey` metadata is present, return `"select"`. This makes FK fields render as selects even without pre-fetched choices (the select will just be empty, signaling a missing `fk_choices`).

4. `_get_options()`: check for `ForeignKey` metadata. If `Choices` was injected (from pre-fetching), use those. Otherwise return an empty list.

**Convenience helper** (on AirModel, not AirForm):

```python
@classmethod
async def as_choices(cls, *, label_field: str | None = None) -> list[tuple[Any, str]]:
    """Fetch all rows and return as (pk_value, label) pairs for form selects."""
    rows = await cls.all()
    pk = cls._pk_field()
    return [(getattr(r, pk), str(r)) for r in rows]
```

Usage in a view:

```python
async def dango_form_view(request):
    form = DangoForm(
        fk_choices={"maker_id": await Maker.as_choices()}
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

## What this does NOT include

- **Cascading deletes:** handle at the application level or add later with `on_delete` parameter
- **Reverse relations** (e.g., `user.repos`): a separate feature
- **Join queries / select_related:** a separate feature
- **Composite foreign keys:** not needed, all PKs are single-column BIGSERIAL
- **Automatic option fetching in forms:** views pre-fetch FK choices explicitly. No hidden queries.

## Implementation plan

1. Add `BaseStructure` base class to `src/air/field/types.py`
2. Move `PrimaryKey` from `BasePresentation` to `BaseStructure`
3. Add `ForeignKey` metadata class to `src/air/field/types.py` (with `resolve()` and string support)
4. Add `foreign_key` parameter to `AirField()` in `src/air/field/main.py` (with mutual-exclusivity validation)
5. Update `_column_defs()` in `src/air/model/main.py` to emit `REFERENCES`
6. Update `_add_column_sql()` to emit `REFERENCES` for FK columns
7. Add `_topological_sort()` and use it in `create_tables()`
8. Add `as_choices()` class method to `AirModel`
9. Update `pydantic_type_to_html_type()` to return `"select"` for FK fields
10. Add `fk_choices` parameter to `AirForm.__init__` and inject into rendering
11. Tests for each layer

## Test cases

```python
# SQL generation
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
class Dango(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    order_id: int | None = AirField(default=None, foreign_key=Order)

sql = Dango._create_table_sql()
assert '"order_id" INTEGER REFERENCES' in sql
assert 'NOT NULL' not in sql.split('order_id')[1].split('\n')[0]

# String forward reference
class Child(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    parent_id: int = AirField(foreign_key="Parent")

class Parent(AirModel):
    id: int | None = AirField(default=None, primary_key=True)
    name: str

# Resolves at SQL generation time, not definition time
sql = Child._create_table_sql()
assert 'REFERENCES' in sql

# Mutual exclusivity
with pytest.raises(ValueError, match="mutually exclusive"):
    AirField(foreign_key=Maker, choices=[(1, "a")])

# Topological sort
sorted_classes = _topological_sort([Dango, Maker])
assert sorted_classes.index(Maker) < sorted_classes.index(Dango)

# ALTER TABLE includes REFERENCES
sql = Dango._add_column_sql("maker_id")
assert 'REFERENCES' in sql

# Form rendering
form = DangoForm(fk_choices={"maker_id": [(1, "Kuma-san"), (2, "Tanuki")]})
html = form.render()
assert '<select' in html
assert 'name="maker_id"' in html
assert 'Kuma-san' in html

# as_choices helper
choices = await Maker.as_choices()
assert choices == [(1, "Kuma-san"), (2, "Tanuki Mochi Co")]
```
