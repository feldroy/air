# Forms

Model utilities for Air.

Provides a thin wrapper around :class:`pydantic.BaseModel` that knows how to generate matching :class:`air.forms.AirForm` subclasses on demand.

## AirModel

Bases: `BaseModel`

Base class for models that integrate tightly with Air forms.

### to_form

```
to_form(*, name=None, includes=None, widget=None)
```

Return an :class:`AirForm` instance bound to `cls`.

Parameters:

| Name       | Type            | Description | Default                                                              |
| ---------- | --------------- | ----------- | -------------------------------------------------------------------- |
| `name`     | \`str           | None\`      | Optional explicit class name for the generated form.                 |
| `includes` | \`Sequence[str] | None\`      | Optional iterable of field names to render (defaults to all fields). |
| `widget`   | \`Callable      | None\`      | Optional custom rendering callable.                                  |

Returns:

| Type      | Description                                               |
| --------- | --------------------------------------------------------- |
| `AirForm` | An instance of :class:AirForm that validates against cls. |

Source code in `src/air/models.py`

```
@classmethod
def to_form(
    cls,
    *,
    name: str | None = None,
    includes: Sequence[str] | None = None,
    widget: Callable | None = None,
) -> AirForm:
    """Return an :class:`AirForm` instance bound to ``cls``.

    Args:
        name: Optional explicit class name for the generated form.
        includes: Optional iterable of field names to render (defaults to all fields).
        widget: Optional custom rendering callable.

    Returns:
        An instance of :class:`AirForm` that validates against ``cls``.
    """

    return to_form(cls, name=name, includes=includes, widget=widget)
```
