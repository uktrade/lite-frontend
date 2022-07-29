# e2e test Docker stack setup

End to end tests requires the following docker setup:

- Latest/Release Tagged API image (stored in GCR)
- Elasticsearch (standard image)
- Redis (standard image)
- Postgres DB using a UAT DB snapshot (stored in GCR)
- Caseworker/Exporter (built from code)


## Creating and pushing the dependency docker image

The below steps should be run every time a change is done on `Dockerfile.dependencies`

```bash
export VERSION=1.0.0 # Increment this version each time when you edit the Dockerfile.dependencies file
```
Ensure you have gcloud sdk and you are logged in following their instructions:

```bash
gcloud auth login
gcloud auth configure-docker
```

Check this out for further help on setting up gcloud: https://cloud.google.com/sdk/docs

```bash
docker build -f Dockerfile.dependencies -t lite-frontend-dependencies .

docker tag lite-frontend-dependencies:latest gcr.io/sre-docker-registry/lite-frontend-dependencies:${VERSION}

docker tag lite-frontend-dependencies:latest gcr.io/sre-docker-registry/lite-frontend-dependencies:latest

docker push gcr.io/sre-docker-registry/lite-frontend-dependencies:${VERSION}

docker push gcr.io/sre-docker-registry/lite-frontend-dependencies:latest
```

Your image should be now listed at [Google Container Registry](http://gcr.io/sre-docker-registry/github.com/uktrade).


## Creating and pushing the lite-db docker image

`lite-db` image is hosted in GCR and latest image is pulled each time stack is built. `lite-api-db-cci-docker-image-refresh` Jenkins job is responsible for keeping it up to date.

In case we want to update it manually, it can be done with following steps:
1. Get hold of lite-uat.sql from Cloud Foundry
```bash
cf login -a api.london.cloud.service.gov.uk --sso
cf conduit lite-api-pg-uat -- pg_dump -f ~/Documents/lite-uat.sql
```
2. add following lines to lite-uat.sql, after SET statements
```bash
CREATE ROLE "ssK27FgZjhTQBg18";
CREATE ROLE "rdsbroker_8b531254_c02c_469e_af42_a5062f734658_manager";
CREATE ROLE "rdsbroker_8b531254_c02c_469e_af42_a5062f734658_reader";
CREATE ROLE "rdsadmin";
ALTER USER "rdsadmin" WITH SUPERUSER;
```
3. Copy the file into the same location as Dockerfile.db in lite-api
4. run `docker build -f Dockerfile.db -t lite-db .`
5. Tag and push image to GCR
```bash
export VERSION=1.0.0 # Make sure this is set appropriately higher than one currently in GCR
```
Ensure you have gcloud sdk and you are logged in following their instructions:

```bash
gcloud auth login
gcloud auth configure-docker
```
Check this out for further help on setting up gcloud: https://cloud.google.com/sdk/docs

```bash
docker tag lite-db:latest eu.gcr.io/sre-docker-registry/lite-db:${VERSION}
docker tag lite-db:latest eu.gcr.io/sre-docker-registry/lite-db:latest

docker push eu.gcr.io/sre-docker-registry/lite-db:${VERSION}
docker push eu.gcr.io/sre-docker-registry/lite-db:latest
```

Your image should be now listed at [Google Container Registry](http://gcr.io/sre-docker-registry/github.com/uktrade).

Note that `lite-db` image is hosted in private registry.


## Creating and pushing the lite-api docker image

`lite-api` image is hosted in GCR and latest image is pulled from there each time stack is built. A GCR trigger, lite-api, is responsible for building it for each merge to master and tag it as `latest`. 

Note: In order to run automated tests before production release, we need `lite-api` image tagged with release tag that is ready for release. There is another GCR trigger `lite-api-release-tag`, that builds api image upon git releases. But currently it is not able to tag correctly with release tag, it is done manually until fixed.

In case we want to update the image manually, simply run the trigger from GCR console.

We can always build it locally and push to GCR - if required.

```bash
docker build -f Dockerfile.e2e -t lite-api .

gcloud auth login
gcloud auth configure-docker

docker tag lite-api:latest gcr.io/sre-docker-registry/github.com/uktrade/lite-api:latest

docker push gcr.io/sre-docker-registry/github.com/uktrade/lite-api:latest
```
