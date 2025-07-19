# Forms

Forms, or AirForms in Air parlance, are powered by pydantic. That includes both their display and validation of data. If you have any experience with pydantic, that will go a long way towards helping your understanding of Air Forms.

## A Sample Contact Form

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

## Displaying a form

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
