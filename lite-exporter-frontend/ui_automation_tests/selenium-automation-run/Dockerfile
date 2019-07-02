FROM exporter/selenium_base:latest

# pip
COPY e2e.txt /tmp/e2e.txt
RUN pip install -r /tmp/e2e.txt
RUN easy_install -U setuptools
RUN pip install pytest-dependency

# Dokcer entry
COPY docker-entry.sh .
ENTRYPOINT ["/docker-entry.sh"]

CMD ["/bin/true"]
