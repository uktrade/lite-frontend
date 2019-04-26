#!/bin/bash
docker-compose run exporter-fe pipenv run ./manage.py migrate
