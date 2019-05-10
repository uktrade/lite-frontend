import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.register_a_business_page import RegisterABusinessPage
from pages.organisations_page import OrganisationsPage
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


def test_register_a_business(driver, open_internal_hub, internal_url):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_a_business_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    time_id = datetime.datetime.now().strftime("%m%d%H%M")

    register_a_business_page.enter_business_name("Test Business " + time_id)
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

    register_a_business_page.enter_email(time_id+"@mail.com")
    register_a_business_page.enter_first_name("Test")
    register_a_business_page.enter_last_name("User1")
    register_a_business_page.enter_password("password")

    register_a_business_page.click_submit()

    registration_complete_message = driver.find_element_by_tag_name("h1").text
    assert registration_complete_message == "Organisation Registered"
    logging.info("Application Submitted")

    # verify application is in organisations list
    dit_hub_page.go_to(internal_url)
    dit_hub_page.click_manage_organisations_link()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + time_id + "')]]")
    logging.info("Test Complete")


def test_cancel_register_a_business(driver, open_internal_hub):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    logging.info("Cancelling...")
    register_page.click_gov()
    # register_page.click_cancel()

    title = driver.title
    assert "Cases" in title

    logging.info("Application Cancelled")
    logging.info("Test Complete")


def test_cannot_submit_without_required_fields(driver, open_internal_hub):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_a_business_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    logging.info("clicked submit")
    register_a_business_page.click_save_and_continue()

    assert driver.find_element_by_xpath("//a[text()[contains(.,'Name:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Eori_Number:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Sic_Number:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Vat_Number:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Registration_Number:')]]").is_displayed()

    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    register_a_business_page.enter_business_name("Test Business " + time_id)
    register_a_business_page.enter_eori_number("GB987654312000")
    register_a_business_page.enter_sic_number("73200")
    register_a_business_page.enter_vat_number("123456789")
    register_a_business_page.enter_company_registration_number("000000011")

    register_a_business_page.click_save_and_continue()
    register_a_business_page.click_save_and_continue()

    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Name:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Address.Address_Line_1:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Address.Postcode:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Address.City:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Address.Region:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'Site.Address.Country:')]]").is_displayed()

    register_a_business_page.enter_site_name("Site 1")
    register_a_business_page.enter_address_line_1("123 Cobalt Street")
    register_a_business_page.enter_address_line_2("123 Cobalt Street")
    register_a_business_page.enter_postcode("N23 6YL")
    register_a_business_page.enter_city("London")
    register_a_business_page.enter_region("London")
    register_a_business_page.enter_country("United Kingdom")

    register_a_business_page.click_save_and_continue()
    register_a_business_page.click_submit()

    assert driver.find_element_by_xpath("//a[text()[contains(.,'User.Email:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'User.First_Name:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'User.Last_Name:')]]").is_displayed()
    assert driver.find_element_by_xpath("//a[text()[contains(.,'User.Password:')]]").is_displayed()
    driver.find_element_by_id("error-summary-title").is_displayed()

    title = driver.title
    assert "Overview" not in title

    logging.info("Test Complete")


def test_teardown(driver):
    driver.quit()
