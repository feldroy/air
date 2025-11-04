# Deploying Air on Railway

Railway is a platform for deploying web applications with automatic scaling, built-in databases, and zero-config deployments. This guide shows how to deploy an Air application to Railway using Nixpacks for builds and Hypercorn for serving.

## Prerequisites

- An Air project with a `main.py` file containing your app.
- A Railway account and project connected to your Git repository.
- (Optional) Railway's PostgreSQL plugin if your app uses a database.

Railway automatically detects Python projects and uses Nixpacks to build them. It provides a `$PORT` environment variable for binding your server.

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

* Commit your uv.lock file to the repo. Don't .gitignore or .railwayignore it.
* Use hypercorn because Railway advises to use it instead of uvicorn. Last time we checked, uvicorn didn't work on Railway.
