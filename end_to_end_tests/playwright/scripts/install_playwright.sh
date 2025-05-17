#!/bin/sh -e

pipenv install --dev
pipenv install --categories end-to-end-packages
pipenv run python -m playwright install
