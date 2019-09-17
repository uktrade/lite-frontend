FROM python:3.7-stretch AS selenium_base

RUN apt-get update && apt-get install -yq \
    firefox-esr \
    chromium=70.0.3538.110-1~deb9u1 \
    git-core \
    xvfb=2:1.19.2-1+deb9u5 \
    xsel=1.2.0-2+b1 \
    unzip \
    python-pytest=3.0.6-1 \
    libgconf2-4=3.2.6-4+b1 \
    libncurses5=6.0+20161126-1+deb9u2 \
    libxml2-dev=2.9.4+dfsg1-2.2+deb9u2 \
    libxslt-dev \
    libz-dev \
    xclip=0.12+svn84-4+b1

# GeckoDriver v0.19.1
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz" -O /tmp/geckodriver.tgz \
    && tar zxf /tmp/geckodriver.tgz -C /usr/bin/ \
    && rm /tmp/geckodriver.tgz

# chromeDriver v2.35
RUN wget -q "https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

# xvfb - X server display
COPY xvfb-chromium /usr/bin/xvfb-chromium
RUN ln -s /usr/bin/xvfb-chromium /usr/bin/google-chrome \
    && chmod 777 /usr/bin/xvfb-chromium

# create symlinks to chromedriver and geckodriver (to the PATH)
RUN ln -s /usr/bin/geckodriver /usr/bin/chromium-browser \
    && chmod 777 /usr/bin/geckodriver \
    && chmod 777 /usr/bin/chromium-browser


FROM selenium_base

# pip
COPY ./e2e.txt /tmp/e2e.txt
RUN pip install -r /tmp/e2e.txt
RUN easy_install -U setuptools
RUN pip install pytest-dependency

# Docker entry
COPY ./docker-entry.sh /
ENTRYPOINT ["/docker-entry.sh"]

CMD ["/bin/true"]
