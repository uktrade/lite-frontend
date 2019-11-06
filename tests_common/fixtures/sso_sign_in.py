from pytest import fixture

from ..tools import utils


@fixture(scope="session")
def sso_sign_in(driver, internal_url, sso_sign_in_url, internal_info, context, seed_data_config):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(internal_info['email'])
    driver.find_element_by_name("password").send_keys(internal_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    lite_client = utils.get_lite_client(context, seed_data_config)
    context.org_name = lite_client.context['org_name']
