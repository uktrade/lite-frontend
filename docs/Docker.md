# e2e test Docker stack setup

End to end tests requires the following docker setup:

- Latest/Release Tagged API image (stored in GCR)
- Elasticsearch (standard image)
- Redis (standard image)
- Postgres DB using a UAT DB snapshot (stored in GCR)
- Caseworker/Exporter (built from code)

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
