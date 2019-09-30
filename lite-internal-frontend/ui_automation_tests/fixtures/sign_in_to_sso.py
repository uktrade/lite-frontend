from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope="session")
def sign_in_to_internal_sso(driver, internal_url, sso_sign_in_url, sso_login_info, context, api_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    lite_client = get_lite_client(context, api_url)
    context.org_name = lite_client.context['org_name']
