# Forms

Forms are how data is collected from users on web pages.

> ## Note
> This document covers how **Forms** work. The full reference for them is the [Forms reference](https://feldroy.github.io/air/api/forms/).

## A simple form example

This contact form is in the classic Starlette way, with no validation of data. However, it does show a method to build forms quickly.

```python
import air

app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(
        air.Title("Contact Form"),
        air.H1("Contact Form"),
        air.Article(
            air.Form(
                air.Label(
                    "Email",
                    air.Input(name="email", type_="email"),
                    for_="Email",
                ),
                air.Label(
                    "Name",
                    air.Input(name="name"),
                ),
                air.Button("submit", type_="submit"),
                action="/add-contact",
                method="post",
            )
        ),
    )


@app.post("/add-contact")
async def add(request: air.Request):
    form = await request.body()
    return air.layouts.mvpcss(
        air.Title("Contact Form Result"),
        air.H1("Contact Form Result"),
        air.Pre(air.Code(form)),
    )
```

## Air Forms

Air Forms are powered by Air Models, which inherit directly from `pydantic.BaseModel`. You define your data model once, and the form inherits its validation rules, field types, and constraints automatically. Air Forms also work with plain `BaseModel` if you prefer.

### Defining a form

Pass your model as a type parameter to `AirForm`:

```python
import air


class JeepneyRouteModel(air.AirModel):
    route_name: str
    origin: str
    destination: str


class JeepneyRouteForm(air.AirForm[JeepneyRouteModel]):
    pass
```

That's it. No `model = JeepneyRouteModel` declaration needed. Air reads the type parameter and sets the model automatically. The model is specified exactly once.

### Type-safe validated data

After validation, `form.data` is the model instance with full type information:

```python
form = JeepneyRouteForm()
form.validate({"route_name": "01C", "origin": "Antipolo", "destination": "Cubao"})

if form.is_valid:
    form.data.route_name    # your editor knows this is a str
    form.data.destination   # autocomplete works
    form.data.orign         # typo caught by the type checker
```

In Django, `form.cleaned_data["route_name"]` is an untyped dict access. Typos become runtime bugs. In WTForms, `form.route_name.data` has no type information. Air is the first Python form system where your editor knows the shape of validated data, because `form.data` is the actual Pydantic model.

If you access `form.data` before validating or after validation fails, you get a clear `AttributeError` instead of a silent `None`.

### How the type parameter works

When you write `class JeepneyRouteForm(AirForm[JeepneyRouteModel])`, two things happen:

1. **For your editor**: the type parameter tells the type checker that `form.data` returns a `JeepneyRouteModel`. This is what powers autocomplete and catches typos.

2. **For Air**: Python stores the type argument at class creation time. Air's `__init_subclass__` hook reads it and sets `model = JeepneyRouteModel` on the form class automatically. No need to write it yourself.

If you prefer to set the model explicitly, that still works:

```python
class JeepneyRouteForm(air.AirForm[JeepneyRouteModel]):
    model = JeepneyRouteModel  # optional, Air sets this from the type parameter
```

### Using AirField for HTML customization

`AirField` lets you add HTML-specific metadata like input types and labels:

```python
from air import AirField, AirModel


class ContactModel(AirModel):
    name: str
    email: str = AirField(type="email", label="Email")


contact_form = ContactModel.to_form()
```

### Displaying an Air Form

```python
contact_form.render()
```

```html
<fieldset>
  <label
    >name
    <input name="name" type="text" id="name" />
  </label>
  <label
    >Email
    <input name="email" type="email" id="email" />
  </label>
</fieldset>
```

## Validation using forms

```python
# This empty dict represents a user who submitted without adding data
empty_form = {}
contact_form.validate(empty_form)
```

## Displaying a failed form

```python
contact_form.render()
```

```html
<fieldset>
  <label>
    name
    <input name="name" type="text" id="name" aria-invalid="true" />
    <small id="name-error">This field is required.</small>
  </label>
  <label>
    Email
    <input name="email" type="email" id="email" aria-invalid="true" />
    <small id="email-error">This field is required.</small>
  </label>
</fieldset>
```

## Converting Pydantic Models to Air Forms

You can convert any Pydantic model into an Air Form using the `to_form` function:

```python
from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    name: str
    email: EmailStr


contact_form = air.to_form(ContactModel)
```

The returned form carries the generic type parameter, so `contact_form.data` is typed as `ContactModel` after validation.

## Enhanced Error Messages

Air Forms automatically display user-friendly error messages that clearly explain validation failures:

- **Missing fields**: "This field is required."
- **Invalid numbers**: "Please enter a valid number."
- **Invalid email addresses**: "Please enter a valid email address."
- **Values too short/long**: "This value is too short." / "This value is too long."
- **URL validation**: "Please enter a valid URL."
- **And many more...**

For unknown error types, the system falls back to the technical Pydantic error message, ensuring developers always get meaningful feedback.
