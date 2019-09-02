from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="function")
def add_clc_query(driver, request, context, exporter_url, api_url):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=False))
    api.add_clc_good()
    context.clc_good_id = api.context['clc_good_id']
