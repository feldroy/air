# Serving static files

You can serve static files like CSS, JavaScript, and images using Air's built-in static file serving capabilities. In this example, we’ll create a simple Air app that serves static files from a `static` directory, but the name of the directory can be anything (`public` is also common).

```
import air

app = air.Air()
app.mount("/static", air.StaticFiles(directory="static"), name="static")

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1("Welcome to My Site!"),
        air.Link(rel="stylesheet", href="/static/styles.css"),
        air.Script(src="/static/scripts.js"),
        air.Img(src="/static/images/logo.png", alt="Logo"),
    )
```
