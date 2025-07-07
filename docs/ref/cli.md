# CLI

!!! warning

    Air's CLI is currently being completely reworked. Everything on this
    page will change in the future. Until the design and UI are more stable,
    do not use the features described here for critical projects.

## Static Site Generation

First, create a directory for your site:

```bash
mkdir example.com
cd example.com
```

Then create an `input` directory and add some templates:

```bash
touch input/base.html input/index.html
```

Put the following content in `input/base.html`:

```html
<!DOCTYPE html>
<html>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

And put the following content in `input/index.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Hello, world!</h1>
{% endblock %}
```

Then run the `air` command:

```bash
air
```

The generated site will be in the `public` directory.

### Using Markdown

Put the following content in `input/hello.md`:

```markdown
---
title: Home
---

# Hello, world!
```

Then run the `air` command:

```bash
air
```

The generated site will be in the `public` directory, with a `hello.html` page generated from the `hello.md` file.

### Deploying to GitHub Pages

First, create a repository on GitHub with your site's domain name as the repository name, e.g. example.github.io

Enable GitHub Pages: In your repository, go to "Settings" > "Pages" and set:

* Source: Deploy from a branch
* Branch: main
* Folder: / (root)

Click "Save".

Commit and push your HTML files to the `main` branch.

Set up your custom domain per GitHub's instructions.


::: air.cli