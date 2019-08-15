from pytest import fixture
from helpers.seed_data import SeedData


@fixture(scope="session")
def add_an_ecju_query_picklist(driver, api_url):
    return SeedData(api_url=api_url, logging=True).add_ecju_query_picklist()
