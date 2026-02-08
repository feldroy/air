# Deploying Air on Railway

Railway is a platform for deploying web applications with automatic scaling, built-in databases, and zero-config
deployments. This guide shows how to deploy an Air application to Railway using Nixpacks for builds and Hypercorn for
serving.

## Prerequisites

- An Air project with a `main.py` file containing your app.
- A Railway account and project connected to your Git repository.
- (Optional) Railway's PostgreSQL plugin if your app uses a database.

Railway automatically detects Python projects and uses Nixpacks to build them. It provides a `$PORT` environment
variable for binding your server.

## Add hypercorn to the dependency list

We use Hypercorn instead of Uvicorn here because one of the prerequisites for deploying Starlette apps to Railway is
Hypercorn as a dependency in the pyproject.toml. When using `uv`, add it to your base packages in `pyproject.toml` thus:

```sh
uv add hypercorn
```

If using `pip` or `uv pip`, you'll need to add hypercorn to whatever file stores your dependency list (often this is
`requirements.txt`).

## Basic Configuration

Create a `railway.json` file in your project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uv run hypercorn main:app --bind \"[::]:$PORT\""
  }
}
```

Tips:

- Commit your uv.lock file to the repo. Don't .gitignore or .railwayignore it.
- Use hypercorn because Railway insists on using it instead of uvicorn.
