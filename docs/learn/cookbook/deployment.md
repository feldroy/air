# Deploying Air Applications

This is a reference for deploying Air applications to different platforms. It is by no means complete, if you have specific questions about deploying to a certain platform, please reach out on our [Discord community](https://discord.gg/nhPNn4bw6R).

## Deploying to Railway 

Railway is a Platform as a Service that supports Python deployments. To deploy an Air application to Railway, add the `hypercorn` package to your dependency list. When using the `uv` command just do this:

```sh
uv add hypercorn
```

Then, assuming you have a `main.py` with an instantiated Air `app`, add a `railway.json` file to the root of your project with the following contents:

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

Then, follow the [Railway deployment instructions](https://docs.railway.app/deploy/deploying-code) to connect your repository and deploy.


