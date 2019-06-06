FROM exporter/selenium_base:latest

# pip
COPY ui_automation_tests/e2e.txt /tmp/e2e.txt
RUN pip install -r /tmp/e2e.txt
RUN easy_install -U setuptools
RUN pip install pytest-dependency

# Dokcer entry
COPY ui_automation_tests/docker-entry.sh .
ENTRYPOINT ["/docker-entry.sh"]

CMD ["/bin/true"]
