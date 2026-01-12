# Running as FastAPI

FastAPI is the direct ancestor of Air. A lot of the same concepts apply, and with a little effort Air apps can be run as FastAPI applications. This is useful for deployment scenarios where FastAPI is already supported, such as in [fastapicloud.com](https://fastapicloud.com/)

To run an Air app as a FastAPI app, use the FastAPI entrypoint in your `pyproject.toml`, where `main` is your core Python module and `app` is your Air application instance:

```
[tool.fastapi]
entrypoint = "main:app"
```

Now Air will run with `fastapi dev` or `fastapi run`, and deploy to FastAPI-compatible platforms.

Reference: [FastAPI Custom Entrypoint - Location](https://fastapicloud.com/docs/builds-and-deployments/configuring-fastapi/#custom-entrypoint---location).
