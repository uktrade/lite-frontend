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

## Starting lite stack via docker

The docker lite stack consists of:

- Latest pushed API image from `lite-api` repo
- Elasticsearch
- Redis
- Postgres DB using a UAT DB snapshot
- Caseworker/Exporter

### Running the stack

- Copy environment variables (make sure to save your current .env files before running the below):
```
cp ci.caseworker.env caseworker.env
cp ci.exporter.env exporter.env
cp ci.api.env api.env
```
- Export the following environment variables in the terminal session that you will start docker (you can find the values of the below in vault):

```
# Common
export DIRECTORY_SSO_API_CLIENT_BASE_URL=
export DIRECTORY_SSO_API_CLIENT_API_KEY=
export AUTHBROKER_CLIENT_ID=
export AUTHBROKER_CLIENT_SECRET=
export AWS_ACCESS_KEY_ID=
export AWS_REGION=
export AWS_SECRET_ACCESS_KEY=
export AWS_STORAGE_BUCKET_NAME=
export AUTH_USER_NAME=
export AUTH_USER_PASSWORD=
export BASIC_AUTH_ENABLED=
export ENDPOINT=
# Exporter specific
export EXPORTER_AUTHBROKER_CLIENT_ID=
export EXPORTER_AUTHBROKER_CLIENT_SECRET=
export BROWSER_HOSTS_EXPORTER=
# Caseworker specific
export TEST_SSO_EMAIL=
export TEST_SSO_PASSWORD=
export BROWSER_HOSTS_CASEWORKER=
# API specific
export AV_SERVICE_PASSWORD=
export AV_SERVICE_URL=
export AV_SERVICE_USERNAME=
```

- Run `make start-caseworker`
