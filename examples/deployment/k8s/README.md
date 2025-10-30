# Deploying an Air application to Kubernetes

At the time of writing this README, Air is still relatively in its alpha stages but at some point the need to run Air apps on Kubernetes will soon happen.

### Why this is necessary

Most modern applications already include the ability to deploy on Kubernetes. Since Air applications are basically closely similar to FastAPI applications, we can refer to FastAPI's documentation on how to deploy apps on Kubernetes. To cut things short, this README covers some quick ways we can achieve deploying Air applications to Kubernetes.

### Requirements

Firstly, we need to ensure that we have built a Docker image (aka container image) for your application. If you haven't done so yet, feel free to refer to https://github.com/feldroy/air/tree/main/examples/containerize.

Once the container image gets built, push your container image to your container registry of choice (Docker Hub, GHCR, Quay.io, etc.) so that it can be readily referenced from within the deployment YAML file.

### The deployment.yaml

We have created a sample `deployment.yaml` file that can be used to deploy your Air application to your cluster on any flavor of Kubernetes. Feel free to use and modify the deployment.yaml to fit your Air project. Here are some sections in the YAML file that you may need to modify.

The `deployment.yaml` is divided into different sections (set as `kind:`) - Deployment, Service, Ingress, ConfigMap, and Secret.

The `Deployment` section defines how the application will be deployed into Kubernetes, and how the application will run and behave.

The `Service` section defines how the application will be accessible via the Kubernetes cluster.

The `Ingress` section defines the networking underpinnings for the routing.

The `ConfigMap` provides additional configurations for the application, which you may need to update for your app.

The `Secret` provides an area where you can securely provide credentials that will be used by your application.

For more details about Kubernetes manifests and objects, a wealth of information is available at https://kubernetes.io/docs/concepts/.

### Tweaking the deployment.yaml

Update the `name:` key to your application name. You may also optionally specify a `namespace:`, but ensure that the namespace already exists before running the deployment.
```
kind: Deployment
metadata:
  name: air-app
  labels:
    app: air-app
```

Make sure also to update any occurrence of `app:` to the name of your application.

Modify the `replicas:` key to the number of replica pods that you prefer to run for your application. Optionally, you can keep the deployment's `strategy.type` to `RollingUpdate` or set it to `Recreate` whichever you prefer. Other deployment strategies and their pros and cons are beyond the scope of this quick how-to.

```
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

Modify `containers.image` to reference your application container image. The `imagePullPolicy:` may be set to either `IfNotPresent` or keep it as is, which is `Always`.

```
containers:
      - name: air
        image: hardwyrd/air-blogdemo:0.39.0
        imagePullPolicy: Always
```

Modify the rest of the deployment.yaml as you see fit for your application.

### Running the deployment

As long as you already have your cluster ready and accessible, you can run your deployment by executing this command:

`kubectl apply -f deployment.yaml -n <your namespace>`

`<your namespace>` must have been created prior to running the deploy.

To verify if your application's pods are running, execute the command:

`kubectl get pods -n <your namespace>`

You should get a list of pods similar to the following:

```
 kubectl get pods -n air-app
NAME                      READY   STATUS    RESTARTS   AGE
air-app-65c99b986-bndnn   1/1     Running   0          11h
air-app-65c99b986-dp5xg   1/1     Running   0          11h
air-app-65c99b986-kmxrf   1/1     Running   0          11h
```

That's it. Congratulations and happy Air bending!


---
title: Deploying an Air application to Kubernetes
author: Romar Mayer Micabalo (hardwyrd@gmail.com)
date: 10/30/2025
---