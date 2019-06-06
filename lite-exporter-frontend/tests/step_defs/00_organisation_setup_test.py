from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from pages.internal_hub_page import InternalHubPage
import helpers.helpers as utils
scenarios('../features/organisation_setup.feature')

@when('I register a new organisation')
def register_organisation(driver):
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
        internal_hub.enter_country("United Kingdom")

        internal_hub.click_save_and_continue()

        internal_hub.enter_email("test@mail.com")
        internal_hub.enter_first_name("Test")
        internal_hub.enter_last_name("User1")
        internal_hub.enter_password("password")

        internal_hub.click_submit()

@then('organisation is registered')
def verify_registered_organisation(driver):
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
    assert exists
