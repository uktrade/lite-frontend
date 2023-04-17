FROM python:3.7-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update --fix-missing
RUN apt-get install -y gcc build-essential python3-dev libmagic1 wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update --fix-missing
RUN apt-get -y install chromium chromium-driver
RUN pip3 install pipenv
ADD Pipfile* /app/
RUN pipenv install --dev --system --deploy
ADD . /app
