from pytest import fixture

from conf.settings import env


@fixture(scope="session")
def environment():
    return env
