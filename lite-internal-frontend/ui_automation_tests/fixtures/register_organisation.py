from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="session")
def register_organisation(driver, request, sso_login_info, api_url, context):
    timer = Timer()
    get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=False))
    context.org_name = "Test Org"
    context.org_registered_status = True
    timer.print_time('register_organisation')
