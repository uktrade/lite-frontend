FROM exporter/selenium-framework

# create project folder with the name code
RUN mkdir /code

# project scope
WORKDIR /code

# install requirements_e2e
COPY requirements_e2e.txt .
RUN pip install -r requirements_e2e.txt

# Set Docker entry
RUN pwd
COPY ./docker-entry.sh /code
ENTRYPOINT ["/code/docker-entry.sh"]

# Install Docker from official repo
RUN apt-get update -qq && \
    apt-get install -qqy apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update -qq && \
    apt-get install -qqy docker-ce && \
    usermod -aG docker jenkins && \
    chown -R jenkins:jenkins $JENKINS_HOME/

USER jenkins

VOLUME [$JENKINS_HOME, "/var/run/docker.sock"]