from pytest import fixture
from pages.exporter_hub_page import ExporterHubPage


@fixture(scope="function")
def sso_sign_in(driver, exporter_url, exporter_sso_login_info, context):
    driver.get(exporter_url)
    if "login" in driver.current_url:
        ExporterHubPage(driver).login(exporter_sso_login_info['email'], exporter_sso_login_info['password'])

