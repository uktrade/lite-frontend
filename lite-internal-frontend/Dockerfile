FROM python:3.7-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install -y libpq-dev gcc
RUN pip3 install pipenv
ADD Pipfile* /app/
RUN pipenv sync
ADD . /app
