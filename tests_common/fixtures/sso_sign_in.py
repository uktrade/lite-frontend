from pytest import fixture


@fixture(scope="session")
def sso_sign_in(driver, internal_url, sso_sign_in_url, internal_info, context, api_test_client):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(internal_info["email"])
    driver.find_element_by_name("password").send_keys(internal_info["password"])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    context.org_id = api_test_client.context["org_id"]
    context.org_name = api_test_client.context["org_name"]
    context.gov_user_id = api_test_client.context["gov_user_id"]
    context.exporter_user_id = api_test_client.context["exporter_user_id"]
