from pytest import fixture
from helpers.seed_data import SeedData


@fixture(scope="session")
def add_an_ecju_query_picklist(driver, api_url):
    return SeedData(api_url=api_url, logging=True).add_ecju_query_picklist()


@fixture(scope="session")
def add_a_proviso_picklist(driver, api_url):
    return SeedData(api_url=api_url, logging=True).add_proviso_picklist()


@fixture(scope="session")
def add_a_standard_advice_picklist(driver, api_url):
    return SeedData(api_url=api_url, logging=True).add_standard_advice_picklist()
