from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="module")
def add_end_user_advisory(driver, request, context, exporter_url, api_url):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=False))
    api.add_eua_query()
    context.end_user_advisory_id = api.context['end_user_advisory_id']
    context.end_user_advisory_case_id = api.context['end_user_advisory_case_id']
