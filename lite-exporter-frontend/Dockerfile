FROM python:3.7-slim
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev
WORKDIR /app
RUN pip3 install pipenv
ADD Pipfile* /app/
RUN pipenv sync
ADD . /app