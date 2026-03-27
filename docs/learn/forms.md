# Forms

Forms are how data is collected from users on web pages.

> ## Note
> This document covers how **Forms** work. The full reference for them is the [Forms reference](https://feldroy.github.io/air/api/forms/).

## A complete example

Here is a contact form that renders on GET, validates on POST, re-renders with errors if validation fails, and uses the typed data on success:

```python
from air import AirField, AirForm, AirModel

import air


class ContactModel(AirModel):
    name: str
    email: str = AirField(type="email", label="Email Address")


class ContactForm(AirForm[ContactModel]):
    pass


app = air.Air()


@app.page
def contact(request: air.Request) -> air.Html | air.Children:
    form = ContactForm()
    return air.layouts.mvpcss(
        air.H1("Contact us"),
        air.Form(
            form.render(),
            air.Button("Send message", type_="submit"),
            method="post",
            action="/submit",
        ),
    )


@app.post("/submit")
async def submit(request: air.Request) -> air.Html:
    form = await ContactForm.from_request(request)

    if form.is_valid:
        return air.Html(
            air.H1("Thank you!"),
            air.P(f"Name: {form.data.name}"),
            air.P(f"Email: {form.data.email}"),
        )

    return air.Html(
        air.H1("Please fix the errors below."),
        air.Form(
            form.render(),
            air.Button("Send message", type_="submit"),
            method="post",
            action="/submit",
        ),
    )
```

The rest of this page breaks down what each piece does.

## Defining a model

AirForm works with any Pydantic model. The example below uses AirModel, which extends `BaseModel` with async database methods, but a plain `BaseModel` works too. You define your data model once, and the form inherits its validation rules, field types, and constraints automatically.

```python
from air import AirModel


class JeepneyRouteModel(AirModel):
    route_name: str
    origin: str
    destination: str
```

## Defining a form

Pass your model as a type parameter to `AirForm`:

```python
from air import AirForm


class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    pass
```

Air reads the type parameter and sets the model automatically. The model is specified exactly once.

## Rendering a form

Call `render()` to get the form HTML:

```python
form = JeepneyRouteForm()
form.render()
```

```html
<div class="air-field">
  <label for="route_name">route_name</label>
  <input name="route_name" id="route_name" type="text" required>
</div>
<div class="air-field">
  <label for="origin">origin</label>
  <input name="origin" id="origin" type="text" required>
</div>
<div class="air-field">
  <label for="destination">destination</label>
  <input name="destination" id="destination" type="text" required>
</div>
```

Each field is wrapped in a `<div class="air-field">` with a label, input, and (after validation) error messages. HTML5 validation attributes (`required`, `minlength`, `maxlength`) are derived from Pydantic constraints. CSRF protection is automatic.

## Validating a form

### From a request

The most common pattern in a POST handler. `from_request` reads the form data and validates it in one step:

```python
@app.post("/submit")
async def submit(request: air.Request) -> air.Html:
    form = await JeepneyRouteForm.from_request(request)

    if form.is_valid:
        form.data.route_name  # typed as str
        form.data.destination  # autocomplete works
    else:
        form.render()  # re-renders with error messages and preserved values
```

### From a dict

You can also validate a plain dict directly:

```python
form = JeepneyRouteForm()
form.validate({"route_name": "01C", "origin": "Antipolo", "destination": "Cubao"})
```

## Type-safe validated data

After validation, `form.data` is the model instance with full type information:

```python
if form.is_valid:
    form.data.route_name  # your editor knows this is a str
    form.data.destination  # autocomplete works
    form.data.orign  # typo caught by the type checker
```

In Django, `form.cleaned_data["route_name"]` is an untyped dict access. Typos become runtime bugs. In WTForms, `form.route_name.data` has no type information. Air is the first Python form system where your editor knows the shape of validated data, because `form.data` is the actual Pydantic model.

If you access `form.data` before validating or after validation fails, you get a clear `AttributeError` instead of a silent `None`.

## Error display

Here is how `render()` output changes after failed validation. First, the empty form:

```python
form = ContactForm()
form.render()
```

```html
<div class="air-field">
  <label for="name">name</label>
  <input name="name" id="name" type="text" required>
</div>
<div class="air-field">
  <label for="email">Email Address</label>
  <input name="email" id="email" type="email" required>
</div>
```

Now the same form after submitting with an empty name and a valid email:

```python
form.validate({"name": "", "email": "audreyfeldroy@example.com"})
form.render()
```

```html
<div class="air-field air-field-error">
  <label for="name">name</label>
  <input name="name" id="name" type="text" required aria-invalid="true" aria-describedby="name-error">
  <div class="air-field-message" id="name-error" role="alert">This field is required.</div>
</div>
<div class="air-field">
  <label for="email">Email Address</label>
  <input name="email" id="email" type="email" required value="audreyfeldroy@example.com">
</div>
```

The email field preserves the submitted value so the user doesn't have to retype it. The name field gets `aria-invalid="true"`, `aria-describedby` linking to the error, and a `role="alert"` error message for screen readers.

Air automatically converts Pydantic's technical errors to user-friendly messages. For unknown error types, it falls back to the technical Pydantic message.

- **Missing fields**: "This field is required."
- **Invalid numbers**: "Please enter a valid number."
- **Invalid email addresses**: "Please enter a valid email address."
- **Values too short/long**: "This value is too short." / "This value is too long."
- **URL validation**: "Please enter a valid URL."

## AirField: customizing HTML output

`AirField` wraps `pydantic.Field` and adds HTML-specific metadata. All standard `pydantic.Field` parameters (`min_length`, `max_length`, `gt`, `ge`, `pattern`, etc.) work alongside the HTML ones:

```python
from air import AirField, AirModel


class ContactModel(AirModel):
    name: str = AirField(label="Full Name", min_length=2, max_length=100)
    email: str = AirField(type="email", label="Email Address")
    message: str = AirField(label="Message", min_length=10)
```

The presentation parameters are:

- **`type`**: HTML input type (`"email"`, `"password"`, `"url"`, `"hidden"`, etc.)
- **`widget`**: Input mechanism (`"textarea"`, `"toggle"`, `"slider"`, etc.)
- **`label`**: Custom label text (defaults to the field name)
- **`placeholder`**: Hint text shown when the field is empty
- **`help_text`**: Explanatory text below the input
- **`choices`**: List of `(value, label)` tuples, renders as `<select>`
- **`autofocus`**: Set to `True` to autofocus the field
- **`primary_key`**: Set to `True` for database primary keys (auto-hidden in forms)

For context-aware visibility, use `Annotated` with AirField metadata types directly:

```python
from typing import Annotated
from airfield import Hidden, ReadOnly


class ArticleModel(AirModel):
    title: str
    slug: Annotated[str, Hidden("form")]  # hidden in forms, visible in tables
    internal: Annotated[str, ReadOnly("form")]  # read-only in forms
```

Pydantic constraints like `min_length` and `max_length` automatically become HTML5 `minlength` and `maxlength` attributes, so browser-side validation matches server-side rules.

## Creating a form

Pass your model as a type parameter to `AirForm`:

```python
class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    pass
```

This works with any `pydantic.BaseModel`, not just AirModel. The type parameter gives your editor full autocomplete on `form.data`.

## Excluding fields

Use `excludes` to hide fields from display, saving, or both:

```python
class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    excludes = (
        "internal_id",  # hidden from display and save
        ("origin", "display"),  # not rendered, still in save_data()
        ("tracking_code", "save"),  # rendered, excluded from save_data()
    )
```

A bare string excludes from both display and save. A tuple targets specific scopes: `"display"`, `"save"`, or both. PrimaryKey fields are default display excludes.

## Saving to database

Use `save_data()` to get a dict with save-excluded fields stripped:

```python
if form.is_valid:
    await JeepneyRouteModel.create(**form.save_data())
```

## Pre-populated edit forms

Pass a dict to the form constructor to fill in values:

```python
route = await JeepneyRouteModel.get(id=42)
form = JeepneyRouteForm(route.model_dump())
form.render()  # inputs have existing values
```

## How the type parameter works

When you write `class JeepneyRouteForm(AirForm[JeepneyRouteModel])`, two things happen:

1. **For your editor**: the type parameter tells the type checker that `form.data` returns a `JeepneyRouteModel`. This is what powers autocomplete and catches typos.

2. **For Air**: Python stores the type argument at class creation time. Air's `__init_subclass__` hook reads it and sets `model = JeepneyRouteModel` on the form class automatically. No need to write it yourself.

If you prefer to set the model explicitly, that still works:

```python
class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    model = JeepneyRouteModel  # optional, Air sets this from the type parameter
```
