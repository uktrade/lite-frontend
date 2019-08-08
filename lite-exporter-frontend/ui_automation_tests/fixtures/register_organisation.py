from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="session")
def register_organisation(driver, request, api_url, exporter_sso_login_info, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=False))
    context.org_registered_status = True
    context.first_name = api.context['first_name']
    context.last_name = api.context['last_name']
    timer.print_time('register_organisation')
