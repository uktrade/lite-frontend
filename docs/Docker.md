# Docker

## Creating and pushing the dependency docker image

The below steps should be run every time a change is done on `Dockerfile.dependencies`

```bash
export VERSION=1.0.0 # Increment this version each time when you edit the Dockerfile.dependencies file

Ensure you have gcloud sdk and you are logged in following their instructions:

```
gcloud auth login
gcloud auth configure-docker
```

https://cloud.google.com/sdk/docs

docker build -f Dockerfile.dependencies -t lite-frontend-dependencies .

docker tag lite-frontend-dependencies:latest gcr.io/sre-docker-registry/lite-frontend-dependencies:${VERSION}

docker tag lite-frontend-dependencies:latest gcr.io/sre-docker-registry/lite-frontend-dependencies:latest

docker push gcr.io/sre-docker-registry/lite-frontend-dependencies:${VERSION}

docker push gcr.io/sre-docker-registry/lite-frontend-dependencies:latest
```

Your image should be now listed at [Google Container Registry](http://gcr.io/sre-docker-registry/github.com/uktrade).