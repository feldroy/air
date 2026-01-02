# The app.page decorator

For simple HTTP GET requests, Air provides the handy @app.page shortcut. It converts the name of the function to a URL, where underscores are replaced with dashes and `index` is replaced with '/'.

When to use @app.page vs @app.get

`@app.page` is convenient when the URL path can be derived from the function name.

Use `@app.get("/path")` instead when you need to:

- Specify a custom URL path that doesn't match the function name
- Include path parameters like `/users/{user_id}`

```
import air

app = air.Air()


@app.page
def index():
    # Same as route app.get('/')
    return air.H1("Welcome to our site!")


@app.page
def dashboard():
    # Same as route app.get('/dashboard')
    return air.H1("Dashboard")


@app.page
def show_item():
    # same as app.get('/show-item')
    return air.H1("Showing an item")
```

An option has been added to change the path separator to forward slashes instead of dashes.

```
import air

app = air.Air(path_separator="/")


@app.page
def about_us():
    # same as app.get('/about/us`)
    return air.H1("About us!")
```
