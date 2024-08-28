import os

from selenium.webdriver.common.by import By

from pytest import fixture


@fixture(scope="session")
def sso_sign_in(driver, internal_url, sso_sign_in_url, internal_info, context, api_test_client):
    # Skip visiting the SSO signin page if our app is set to use mock SSO
    if not os.environ.get("MOCK_SSO_ACTIVATE_ENDPOINTS") == "True":
        driver.get(sso_sign_in_url)
        driver.find_element(by=By.NAME, value="username").send_keys(internal_info["email"])
        driver.find_element(by=By.NAME, value="password").send_keys(internal_info["password"])
        driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']").click()
    driver.get(internal_url)
    # If we are using mock sso and don't have an email set then we know we need
    # to fill it in
    if os.environ.get("MOCK_SSO_ACTIVATE_ENDPOINTS") == "True" and not os.environ.get("MOCK_SSO_USER_EMAIL"):
        driver.find_element(by=By.NAME, value="email").send_keys(internal_info["email"])
        driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']").click()
    context.org_id = api_test_client.context["org_id"]
    context.org_name = api_test_client.context["org_name"]
    context.gov_user_id = api_test_client.context["gov_user_id"]
    context.exporter_user_id = api_test_client.context["exporter_user_id"]
