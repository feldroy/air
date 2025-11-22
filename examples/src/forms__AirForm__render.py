"""Example: Using AirForm.render to generate HTML for a simple contact form.

Run:

    uv run examples/src/forms__AirForm__render.py

Then open http://127.0.0.1:8000/contact in your browser.
"""

from pydantic import BaseModel

import air

app = air.Air()


class ContactModel(BaseModel):
    """Pydantic model backing the contact form."""

    name: str
    email: str
    message: str


class ContactForm(air.AirForm):
    """AirForm that uses ContactModel for validation and rendering."""

    model = ContactModel


@app.page
def contact(request: air.Request):
    """Render a page with a contact form built using AirForm.render()."""
    form = ContactForm()
    return air.layouts.mvpcss(
        air.H1("Contact us"),
        air.P("This form is rendered using AirForm.render()."),
        air.Form(
            form.render(),
            air.Button("Send message", type="submit"),
            method="post",
            action=submit.url(),  # type: ignore[unresolved-attribute]
        ),
    )


@app.post("/contact")
async def submit(request: air.Request) -> air.Html:
    """Handle form submission and re-render the form if there are errors."""
    form = ContactForm()
    form_data = await request.form()

    # Validate incoming form data; AirForm.render() will then include errors
    # and preserve submitted values when re-rendered.
    form.validate(form_data)

    if form.is_valid:
        return air.Html(
            air.H1("Thank you for your message!"),
            air.P("Your contact form was submitted successfully."),
        )

    error_count = len(form.errors or [])
    return air.Html(
        air.H1("Please fix the errors below."),
        air.P(f"Found {error_count} validation error(s)."),
        air.Form(
            form.render(),
            air.Button("Send message", type="submit"),
            method="post",
            action=submit.url(),  # type: ignore[unresolved-attribute]
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
