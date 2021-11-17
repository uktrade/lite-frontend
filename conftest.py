DEBUG = False


def pytest_configure(config):
    global DEBUG  # pylint: disable=global-statement
    DEBUG = config.option.debug
