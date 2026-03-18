# Forms

Forms are how data is collected from users on web pages.

> ## Note
> This document covers how **Forms** work. The full reference for them is the [Forms reference](https://feldroy.github.io/air/api/forms/).

## A complete example

Here is a contact form that renders on GET, validates on POST, re-renders with errors if validation fails, and uses the typed data on success:

```python
import air


class ContactModel(air.AirModel):
    name: str
    email: str = air.AirField(type="email", label="Email Address")


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

Air Forms are powered by Air Models, which inherit directly from `pydantic.BaseModel`. You define your data model once, and the form inherits its validation rules, field types, and constraints automatically.

```python
import air


class JeepneyRouteModel(air.AirModel):
    route_name: str
    origin: str
    destination: str
```

## Defining a form

Pass your model as a type parameter to `AirForm`:

```python
class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    pass
```

That's it. No `model = JeepneyRouteModel` declaration needed. Air reads the type parameter and sets the model automatically. The model is specified exactly once.

## Rendering a form

Call `render()` to get the form HTML:

```python
form = JeepneyRouteForm()
form.render()
```

```html
<label>route_name <input name="route_name" type="text" id="route_name" required /></label>
<label>origin <input name="origin" type="text" id="origin" required /></label>
<label>destination <input name="destination" type="text" id="destination" required /></label>
```

Air generates `<label>` and `<input>` pairs from the model fields, with HTML5 validation attributes (`required`, `minlength`, `maxlength`) derived from Pydantic constraints.

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
    form.data.route_name    # your editor knows this is a str
    form.data.destination   # autocomplete works
    form.data.orign         # typo caught by the type checker
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
<label>name <input name="name" type="text" id="name" required /></label>
<label>Email Address <input name="email" type="email" id="email" required /></label>
```

Now the same form after submitting with an empty name and a valid email:

```python
form.validate({"name": "", "email": "audreyfeldroy@example.com"})
form.render()
```

```html
<label>
  name
  <input name="name" type="text" id="name" aria-invalid="true" required />
  <small id="name-error">This field is required.</small>
</label>
<label>
  Email Address
  <input name="email" type="email" id="email" value="audreyfeldroy@example.com" required />
</label>
```

The email field preserves the submitted value so the user doesn't have to retype it. The name field gets `aria-invalid="true"` and a `<small>` error message.

Air automatically converts Pydantic's technical errors to user-friendly messages. For unknown error types, it falls back to the technical Pydantic message.

- **Missing fields**: "This field is required."
- **Invalid numbers**: "Please enter a valid number."
- **Invalid email addresses**: "Please enter a valid email address."
- **Values too short/long**: "This value is too short." / "This value is too long."
- **URL validation**: "Please enter a valid URL."

## AirField: customizing HTML output

`AirField` wraps `pydantic.Field` and adds HTML-specific metadata. All standard `pydantic.Field` parameters (`min_length`, `max_length`, `gt`, `ge`, `pattern`, etc.) work alongside the HTML ones:

```python
class ContactModel(air.AirModel):
    name: str = air.AirField(label="Full Name", min_length=2, max_length=100)
    email: str = air.AirField(type="email", label="Email Address")
    message: str = air.AirField(label="Message", min_length=10)
```

The HTML-specific parameters are:

- **`type`**: HTML input type (`"email"`, `"password"`, `"url"`, `"hidden"`, etc.)
- **`label`**: Custom label text (defaults to the field name)
- **`autofocus`**: Set to `True` to autofocus the field

Pydantic constraints like `min_length` and `max_length` automatically become HTML5 `minlength` and `maxlength` attributes, so browser-side validation matches server-side rules.

## Three ways to create a form

These all produce the same thing. Pick whichever fits your situation:

**1. Subclass (recommended).** Best when you want a reusable form class with type safety:

```python
class JeepneyRouteForm(AirForm[JeepneyRouteModel]):
    pass
```

**2. AirModel.to_form().** Best for quick one-off forms:

```python
form = JeepneyRouteModel.to_form()
```

**3. air.to_form().** Works with any `pydantic.BaseModel`, not just AirModel:

```python
from pydantic import BaseModel

class PlainModel(BaseModel):
    name: str

form = air.to_form(PlainModel)
```

All three paths produce an `AirForm` instance. The subclass approach gives the type checker the most information. The `to_form()` shortcuts are convenient when you don't need a named class.

## Rendering a subset of fields

Use `includes` to render only specific fields. This is useful for multi-step forms or splitting a form into fieldsets:

```python
form = JeepneyRouteModel.to_form(includes=["route_name"])
form.render()  # only renders route_name
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
