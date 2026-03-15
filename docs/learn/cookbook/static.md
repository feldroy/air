# Serving static files

Drop a `static/` directory into your project and Air serves it automatically with cache-busted URLs. Every file gets a content hash in its URL and is served with immutable cache headers. Any `/static/` paths in your HTML responses are rewritten to their hashed versions automatically.

```
myproject/
    main.py
    static/
        styles.css
        scripts.js
        images/
            logo.png
```

```python
import air

app = air.Air()


@app.page
def index():
    return air.layouts.mvpcss(
        air.H1("Welcome to My Site!"),
        air.Link(rel="stylesheet", href="/static/styles.css"),
        air.Script(src="/static/scripts.js"),
        air.Img(src="/static/images/logo.png", alt="Logo"),
    )
```

The `/static/styles.css` path in your HTML is rewritten to something like `/static/styles.a1b2c3d4.css` in the response, so browsers cache aggressively and always get the latest version when you change a file.
