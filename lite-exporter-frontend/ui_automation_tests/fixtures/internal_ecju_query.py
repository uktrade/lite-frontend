from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="module")
def internal_ecju_query(driver,  api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_ecju_query(context.case_id)


@fixture(scope="module")
def internal_ecju_query_end_user_advisory(driver,  api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_ecju_query(context.end_user_advisory_case_id)
