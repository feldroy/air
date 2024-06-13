# air

An ultra-lightweight static site generator.

## Quickstart

First, create a directory for your site, initialize it with Rye, and add the `air` package. Replace `example.com` with the name of your site:

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

## Deploying to GitHub Pages

First, create a repository on GitHub with your site's domain name as the repository name, e.g. example.github.io

Enable GitHub Pages: In your repository, go to "Settings" > "Pages" and set:

* Source: Deploy from a branch
* Branch: main
* Folder: / (root)

Click "Save".

Commit and push your HTML files to the `main` branch.

Set up your custom domain per GitHub's instructions.
