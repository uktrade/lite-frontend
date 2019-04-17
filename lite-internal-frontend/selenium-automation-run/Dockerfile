FROM exporter/selenium_base:latest

# pip
COPY requirements_e2e.txt /tmp/requirements_e2e.txt
RUN pip install -r /tmp/requirements_e2e.txt
RUN easy_install -U setuptools
RUN pip install pytest-dependency

# Docker entry
COPY automation_ui_tests/docker-entry.sh .
ENTRYPOINT ["/docker-entry.sh"]

CMD ["/bin/true"]
