from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="module")
def internal_case_note(driver,  api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_case_note(context)
