# Containerizing an Air application

Air applications are closely similar to FastAPI applications. Building a Docker image for your Air app is very much straightforward as you would building a Docker image for a FastAPI application, with some minor differences.

### Why build a container image? 

There are many advantages to building a container image for your Air application. For one, the container image you generate becomes a discreet deployable unit making your application more portable. You can then run your container image on Docker Engine, Docker Desktop, other platforms that support Docker images, or deploy your container image into any flavor of Kubernetes.

### The Dockerfile

We have provided a sample Dockerfile that you can use to bootstrap your way to building your own Docker container image.

By default, the Dockerfile expects your app file to be `main.py`. If you have used a different filename for your app file, make sure to update the line with `main:app` of the sample Dockerfile to reflect your app name and file:

`CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers", "--forwarded-allow-ips", "*"]`

You can copy the provided sample Dockerfile and put it in your project folder.

### Dependencies

Before attempting to build, ensure that you have installed the dependencies required by Air and your application. The following dependencies are for the sample airblog app:

```
uv add uvicorn
uv add frontmatter
uv add mistletoe
uv add fastapi[standard]
```

By running the previous uv commands, the dependencies are added by uv to pyproject.toml and will be referenced during Docker build.

### Building

Docker now requires you use `buildx` instead of `build` for building your Docker images.

For multi-platform builds (eg. you want your image to support `linux/amd64` and `linux/arm64`) you will need to add multi-platform support for Docker. You can refer to https://docs.docker.com/build/building/multi-platform/ for more information.

To run the actual build, run:

`docker buildx build -t <your-registry>/<your-app>:<tag> --push . `

For multi-platform build, run:

`docker buildx build --platform linux/amd64,linux/arm64 -t <your-registry>/<your-app>:<tag> --push . `

Your image will then be pushed automatically to your designated image registry. You can then test it out by pulling your container image and running it:

`docker pull <your-registry>/<your-app>:<tag>`

`docker run --name your-app -p <local port>:<container port> <your-registry>/<your-app>:<tag>`

You are now ready to play some more with Air!

---
title: Containerizing an Air application
author: Romar Mayer Micabalo (hardwyrd@gmail.com)
date: 10/28/2025
---
