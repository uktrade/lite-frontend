DEBUG = False


def pytest_configure(config):
    global DEBUG
    DEBUG = config.option.debug
