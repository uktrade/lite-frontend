FROM python:3.7-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install -y libpq-dev gcc \
  # Libraries required for PDF generation via WeasyPrint
  # (https://weasyprint.readthedocs.io/en/stable/install.html#debian-ubuntu)
  build-essential python3-dev python3-pip python3-setuptools python3-wheel \
  python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
  libffi-dev shared-mime-info \
  # Extra fonts for PDF generation
  fonts-liberation2

RUN pip3 install pipenv
ADD Pipfile* /app/
RUN pipenv sync
ADD . /app
