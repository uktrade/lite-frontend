from pytest import fixture

from ui_tests.exporter.pages.start_page import StartPage
from ui_tests.exporter.pages.govuk_signin_page import GovukSigninPage


@fixture(scope="function")
def sso_sign_in(driver, exporter_url, exporter_info, context):
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()

    if "signin" in driver.current_url:
        GovukSigninPage(driver).sign_in(exporter_info["email"], exporter_info["password"])

    if "register-name" in driver.current_url:
        driver.find_element(value="id_first_name").send_keys(exporter_info["first_name"])
        driver.find_element(value="id_last_name").send_keys(exporter_info["last_name"])
        driver.find_element(value="submit-id-submit").click()
