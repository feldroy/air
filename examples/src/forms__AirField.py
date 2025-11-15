"""Example: Using AirField to control HTML form behavior.

This example demonstrates:

- How AirField customizes HTML input types (e.g. email, datetime-local)
- How labels and autofocus attributes appear in rendered forms
- How AirForm binds to a Pydantic model for validation
- How the form behaves when submitted with valid and invalid data

Run:

    uv run examples/src/forms__AirField.py

Then visit http://127.0.0.1:8000/ in your browser.
"""

from pydantic import BaseModel

import air

app = air.Air()


class ContactModel(BaseModel):
    name: str = air.AirField(label="Full Name", min_length=2, max_length=50)
    # Note: This uses `str` for email. For stricter server-side validation,
    # you can use `EmailStr` from pydantic.
    email: str = air.AirField(type="email", label="Email Address")
    message: str = air.AirField(label="Message", min_length=10, max_length=500)
    preferred_datetime: str = air.AirField(
        type="datedatetime-local",
        label="Preferred Date & Time",
    )


class ContactForm(air.AirForm):
    model = ContactModel


@app.page
def index(request: air.Request):
    """Render a simple page containing the contact form."""
    form = ContactForm()
    return air.layouts.mvpcss(
        air.H1("Contact Form Example Using AirField"),
        air.P("Submit the form below to see AirField + AirForm in action."),
        air.Form(
            form.render(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        ),
    )


@app.post("/submit")
async def submit(request: air.Request) -> air.Html:
    """Handle POSTed form data and re-render with errors if invalid."""
    form = ContactForm()

    # Parse form data from the incoming request and validate
    form_data = await request.form()
    form.validate(form_data)

    if form.is_valid:
        return air.Html(
            air.layouts.mvpcss(
                air.H1("Thanks for your message!"),
                air.P("Here is what you sent:"),
                air.Ul(
                    air.Li(f"Name: {form.data.name}"),
                    air.Li(f"Email: {form.data.email}"),
                    air.Li(f"Message: {form.data.message}"),
                    air.Li(f"Preferred Date & Time: {form.data.preferred_datetime}"),
                ),
            )
        )

    # If invalid, re-render the form with errors and values preserved
    return air.Html(
        air.layouts.mvpcss(
            air.H1("Please fix the errors below."),
            air.Form(
                form.render(),
                air.Button("Submit", type="submit"),
                method="post",
                action="/submit",
            ),
        )
    )


if __name__ == "__main__":
    # Run this example with:
    #   uv run examples/src/forms__AirField.py
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
