# air

An ultra-lightweight static site generator.

## Quickstart

First, create a directory for your site, initialize it with Rye, and add the `air` package:

```bash
mkdir example.com
cd example.com
rye init
rye add air
```

Then create a `templates` directory and add some templates:

```bash
touch templates/base.html templates/index.html
```

Put the following content in `templates/base.html`:

```html
<!DOCTYPE html>
<html>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

And put the following content in `templates/index.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Hello, world!</h1>
{% endblock %}
```

Then run the `air` command:

```bash
rye run air
```

The generated site will be in the `public` directory.

## Creating Markdown Pages

Create a `pages` directory and add some pages:

```bash
mkdir pages
touch pages/index.md
```
