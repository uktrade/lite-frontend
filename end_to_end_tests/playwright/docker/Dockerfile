FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy
# Available playwright tags:
# https://mcr.microsoft.com/en-us/product/playwright/tags

WORKDIR /code
COPY Pipfile* /code/

RUN pip install pipenv
RUN pipenv requirements --categories end-to-end-packages > requirements.txt
RUN pip install -r requirements.txt
