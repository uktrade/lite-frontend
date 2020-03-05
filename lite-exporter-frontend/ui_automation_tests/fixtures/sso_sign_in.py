from pytest import fixture

from ui_automation_tests.pages.start_page import StartPage
from ui_automation_tests.pages.great_signin_page import GreatSigninPage


@fixture(scope="function")
def sso_sign_in(driver, exporter_url, exporter_info, context):
    driver.get(exporter_url)

    StartPage(driver).try_click_sign_in_button()

    if "login" in driver.current_url:
        GreatSigninPage(driver).sign_in(exporter_info["email"], exporter_info["password"])
