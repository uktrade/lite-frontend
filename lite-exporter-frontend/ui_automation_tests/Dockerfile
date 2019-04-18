FROM exporter/selenium-framework

# create project folder with the name code
RUN mkdir /code

# project scope
WORKDIR /code

# install requirements
COPY requirements_e2e.txt .
RUN pip install -r requirements_e2e.txt

# Set Dokcer entry
RUN pwd
COPY ./docker-entry.sh /code
ENTRYPOINT ["/code/docker-entry.sh"]
