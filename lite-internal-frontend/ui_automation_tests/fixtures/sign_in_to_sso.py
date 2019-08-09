from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="session")
def sign_in_to_internal_sso(driver, internal_url, sso_sign_in_url, sso_login_info, context, api_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    context.org_name = api.context['org_name']
