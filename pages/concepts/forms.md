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
                air.Label("Email", air.Input(name="email", type="email"), for_="Email"),
                air.Label(
                    "Name",
                    air.Input(name="name"),
                ),
                air.Button("submit", type="submit"),
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

Air Forms are powered by Pydantic. That includes both their display and validation of data. If you have any experience with Pydantic, that will go a long way towards helping your understanding of Air Forms.

### A Sample Contact Air Form

```python
from pydantic import BaseModel, Field
from air import AirForm, AirField

class ContactModel(BaseModel):
    name: str
    email: str = AirField(type="email", label="Email")

class ContactForm(AirForm):
    model = ContactModel


contact_form = ContactForm()
```

### Displaying an Air Form

```python

contact_form.render()
```

```html
<fieldset>
    <label>name
        <input name="name" type="text" id="name" />
    </label>
    <label>Email
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
        <small id="name-error">Please correct this error.</small>
    </label>
    <label>
        Email
        <input name="email" type="email" id="email" aria-invalid="true" />
        <small id="email-error">Please correct this error.</small>
    </label>
</fieldset>
```
