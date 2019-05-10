from selenium.webdriver.common.by import By
import helpers.helpers as utils
from pages.register_a_business_page import RegisterABusinessPage
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.organisations_page import OrganisationsPage
import pytest
import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_new_organisation_setup(driver, open_internal_hub):
    log.info("Setting up new organisation")
    register_a_business_page = RegisterABusinessPage(driver)
    internal_hub_page = DepartmentOfInternationalTradeHub(driver)
    organisations_page = OrganisationsPage(driver)

    internal_hub_page.click_manage_organisations_link()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        organisations_page.click_new_organisation_btn()

        register_a_business_page.enter_business_name("Test Org")
        register_a_business_page.enter_eori_number("GB987654312000")
        register_a_business_page.enter_sic_number("73200")
        register_a_business_page.enter_vat_number("123456789")
        register_a_business_page.enter_company_registration_number("000000011")

        register_a_business_page.click_save_and_continue()

        log.info("Create a default site for this organisation")

        register_a_business_page.enter_site_name("Site 1")
        register_a_business_page.enter_address_line_1("123 Cobalt Street")
        register_a_business_page.enter_address_line_2("123 Cobalt Street")
        register_a_business_page.enter_postcode("N23 6YL")
        register_a_business_page.enter_city("London")
        register_a_business_page.enter_region("London")
        register_a_business_page.enter_country("United Kingdom")

        register_a_business_page.click_save_and_continue()

        register_a_business_page.enter_email("test@mail.com")
        register_a_business_page.enter_first_name("Test")
        register_a_business_page.enter_last_name("User1")
        register_a_business_page.enter_password("password")

        register_a_business_page.click_submit()

        assert "Organisations" in driver.title, "Error in registering business"

        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists


def test_teardown(driver):
    driver.quit()
