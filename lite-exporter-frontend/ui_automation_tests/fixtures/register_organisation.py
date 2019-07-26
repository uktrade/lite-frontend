from pytest import fixture
import helpers.helpers as utils
from pages.internal_hub_page import InternalHubPage
from selenium.webdriver.common.by import By


@fixture(scope="session")
def register_organisation(driver, request, sso_login_info, exporter_sso_login_info, context):
    driver.get(request.config.getoption("--sso_sign_in_url"))
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(request.config.getoption("--internal_url"))
    internal_hub = InternalHubPage(driver)

    internal_hub.click_manage_organisations_link()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        internal_hub.click_new_organisation()

        internal_hub.enter_business_name("Test Org")
        internal_hub.enter_eori_number("GB987654312000")
        internal_hub.enter_sic_number("73200")
        internal_hub.enter_vat_number("123456789")
        internal_hub.enter_company_registration_number("000000011")
        internal_hub.click_save_and_continue()

        internal_hub.enter_site_name("Site 1")
        internal_hub.enter_address_line_1("123 Cobalt Street")
        internal_hub.enter_address_line_2("123 Cobalt Street")
        internal_hub.enter_zip_code("N23 6YL")
        internal_hub.enter_city("London")
        internal_hub.enter_state("London")
        internal_hub.enter_country("Ukraine")

        internal_hub.click_save_and_continue()

        internal_hub.enter_email(exporter_sso_login_info['email'])
        internal_hub.enter_first_name("Test")
        internal_hub.enter_last_name("User1")

        internal_hub.click_submit()
        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists
