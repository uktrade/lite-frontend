import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.register_a_business_page import RegisterABusinessPage
from pages.organisations_page import OrganisationsPage
from pages.exporter_hub import ExporterHub
import helpers.helpers as utils
import datetime
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_view_sites_for_organisation(driver, open_internal_hub, internal_url, exporter_url):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_a_business_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)
    exporter_hub = ExporterHub(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    time_id = datetime.datetime.now().strftime("%m%d%H%M")

    register_a_business_page.enter_business_name("Organisation T" + time_id)
    register_a_business_page.enter_eori_number("GB543129876000")
    register_a_business_page.enter_sic_number("73200")
    register_a_business_page.enter_vat_number("123456789")
    register_a_business_page.enter_company_registration_number("000000011")
    register_a_business_page.click_save_and_continue()
    log.info("Create a default site for this organisation")
    register_a_business_page.enter_site_name("Site 1")
    register_a_business_page.enter_address_line_1("123 Cobalt Street")
    register_a_business_page.enter_postcode("N23 6YL")
    register_a_business_page.enter_city("London")
    register_a_business_page.enter_region("Greater London")
    register_a_business_page.enter_country("United Kingdom")
    register_a_business_page.click_save_and_continue()
    register_a_business_page.enter_email("T" + time_id + "@mail.com")
    register_a_business_page.enter_first_name("Test")
    register_a_business_page.enter_last_name("User1")
    register_a_business_page.enter_password("password")
    register_a_business_page.click_submit()

    driver.find_element_by_xpath("//*[text()='Go to organisations']").click()

    driver.find_element_by_xpath("//*[text()[contains(.,'" + time_id + "')]]").click()

    assert driver.find_element_by_xpath("//*[text()='GB543129876000']").is_displayed()
    assert driver.find_element_by_xpath("//*[text()='73200']").is_displayed()
    assert driver.find_element_by_xpath("//*[text()='123456789']").is_displayed()
    assert driver.find_element_by_xpath("//*[text()='000000011']").is_displayed()

    assert driver.find_element_by_xpath("//*[text()[contains(.,'Site 1')]]").is_displayed()

    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("T"+time_id+"@mail.com", "password")

    exporter_hub.click_sites()
    exporter_hub.click_new_site()

    driver.find_element_by_id("name").send_keys("Site 2")
    driver.find_element_by_id("address.address_line_1").send_keys("123 Cobalt Street")
    driver.find_element_by_id("address.postcode").send_keys("N23 6YL")
    driver.find_element_by_id("address.city").send_keys("London")
    driver.find_element_by_id("address.region").send_keys("Westminster")
    driver.find_element_by_id("address.country").send_keys("United Kingdom")
    exporter_hub.click_submit()

    dit_hub_page.go_to(internal_url)
    dit_hub_page.click_manage_organisations_link()
    driver.find_element_by_xpath("//*[text()[contains(.,'" + time_id + "')]]").click()

    assert driver.find_element_by_xpath("//*[text()[contains(.,'Site 2')]]").is_displayed()


def test_teardown(driver):
    driver.quit()
