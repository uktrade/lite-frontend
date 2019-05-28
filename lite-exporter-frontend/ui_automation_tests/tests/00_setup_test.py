from pages.exporter_hub_page import ExporterHubPage
from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest
import logging
from pages.exporter_hub_page import ExporterHubPage
from pages.internal_hub_page import InternalHubPage

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    # navigate to the application home page
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)

@pytest.fixture(scope="function")
def open_exporter_hub(driver, exporter_url):
    # navigate to the application home page
    driver.get(exporter_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_new_organisation_setup(driver, open_internal_hub):
    log.info("Setting up new organisation")
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

        log.info("Create a default site for this organisation")

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

        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists


def test_add_goods_setup(driver, open_exporter_hub):
    log.info("add 3 goods")
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.login("test@mail.com", "password")

    # Click My goods assert is on the my goods page
    exporter_hub.click_my_goods()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T1')]]")
    if not exists:
        # Add good details
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T1")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML6")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G1-12")
        exporter_hub.click_save_and_continue()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T2')]]")
    if not exists:
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T2")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML34a")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G2-23")
        exporter_hub.click_save_and_continue()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T3')]]")
    if not exists:
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T3")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML1")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G3-3")
        exporter_hub.click_save_and_continue()


def test_add_users_setup(driver, exporter_url):
    log.info("add test user")
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_users()
    exists = utils.is_element_present(driver, By.XPATH, "//td[text()[contains(.,'testuser_1@mail.com')]]")
    if not exists:
        for x in range(3):
            i = str(x + 1)
            exporter_hub.click_add_a_user_btn()
            exporter_hub.enter_first_name("Test")
            exporter_hub.enter_last_name("user_" + i)
            exporter_hub.enter_email("testuser_" + i + "@mail.com")
            exporter_hub.enter_password("1234")
            exporter_hub.click_save_and_continue()


def test_teardown(driver):
    driver.quit()
