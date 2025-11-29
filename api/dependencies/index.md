# Dependencies

Air provides dependency injection utilities to help you build responsive web applications.

## HTMX Request Detection

The `is_htmx_request` dependency allows you to detect whether a request is coming from an HTMX action, enabling you to return different responses for HTMX vs regular HTTP requests.

### Common Use Cases

- Return partial HTML fragments for HTMX requests and full pages for regular requests
- Provide different response formats (JSON for HTMX, redirects for forms)
- Implement progressive enhancement patterns

### Examples

#### Basic Usage

```
import air
from fastapi import Depends

app = air.App()

@app.get("/users")
def get_users(is_htmx: bool = Depends(air.is_htmx_request)):
    users = ["Alice", "Bob", "Charlie"]

    if is_htmx:
        # Return just the user list for HTMX partial updates
        return air.Ul([air.Li(user) for user in users])
    else:
        # Return full page for regular requests
        return air.Html([
            air.Head(air.Title("Users")),
            air.Body([
                air.H1("User List"),
                air.Ul([air.Li(user) for user in users])
            ])
        ])
```

#### Form Handling

```
@app.post("/submit")
def submit_form(is_htmx: bool = Depends(air.is_htmx_request)):
    if is_htmx:
        return air.Div("Success!", class_="alert-success")
    else:
        return RedirectResponse("/success", status_code=303)
```

Tools for handling dependencies, for things like handling incoming data from client libraries like HTMX.

## is_htmx_request

```
is_htmx_request = Depends(_is_htmx_request)
```
