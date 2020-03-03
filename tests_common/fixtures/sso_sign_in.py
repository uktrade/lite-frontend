from pytest import fixture

from ..tools.utils import get_lite_client


@fixture(scope="session")
def sso_sign_in(driver, internal_url, sso_sign_in_url, internal_info, context, api_client_config):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(internal_info["email"])
    driver.find_element_by_name("password").send_keys(internal_info["password"])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    lite_client = get_lite_client(context, api_client_config)
    context.org_id = lite_client.context["org_id"]
    context.org_name = lite_client.context["org_name"]
    context.gov_user_id = lite_client.context["gov_user_id"]
    context.exporter_user_id = lite_client.context["exporter_user_id"]
