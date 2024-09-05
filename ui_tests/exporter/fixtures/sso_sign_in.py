from pytest import fixture

from ui_tests.exporter.pages.start_page import StartPage
from ui_tests.exporter.pages.govuk_signin_page import GovukSigninPage


@fixture()
def sso_sign_in(driver, exporter_url, exporter_info, context):
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()

    if "signin" in driver.current_url:
        GovukSigninPage(driver).sign_in(exporter_info["email"], exporter_info["password"])
