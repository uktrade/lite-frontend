from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.applications_page import ApplicationsPage
from pages.internal_hub_page import InternalHubPage

import helpers.helpers as utils
import pytest
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@pytest.fixture(scope="function")
def open_exporter_hub(driver, exporter_url):
    driver.get(exporter_url)
    # driver.maximize_window()
    # assert driver.title == "Exporter Hub - LITE"
    log.info(driver.current_url)


def test_add_site(driver, open_exporter_hub, exporter_url):
    time_id = datetime.datetime.now().strftime("%m%d%H%M")

    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)
    site_page = InternalHubPage(driver)


    log.info("logging in as test@mail.com")
    exporter_hub.login("test@mail.com", "password")

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_sites()
    exporter_hub.click_new_site()

    driver.find_element_by_id("name").send_keys("New Site " + time_id)
    driver.find_element_by_id("address.address_line_1").send_keys("123 Cobalt Street")
    driver.find_element_by_id("address.postcode").send_keys("N23 6YL")
    driver.find_element_by_id("address.city").send_keys("London")
    driver.find_element_by_id("address.region").send_keys("Westminster")
    driver.find_element_by_id("address.country").send_keys("United Kingdom")
    site_page.click_submit()

    assert driver.find_element_by_tag_name("h1").text == "Sites", \
        "Failed to return to Sites list page after Adding site"

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'New Site "+time_id+"')]]")


def test_edit_site(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    site_page = InternalHubPage(driver)

    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_sites()

    driver.find_element_by_xpath("//*[text()[contains(.,'Site 1')]]/following-sibling::td[last()]/a").click()

    driver.find_element_by_id("name").clear()
    driver.find_element_by_id("name").send_keys("Site 1 Edited")
    driver.find_element_by_id("address.address_line_1").clear()
    driver.find_element_by_id("address.address_line_1").send_keys("123 Cobalt Street Edited")
    driver.find_element_by_id("address.postcode").clear()
    driver.find_element_by_id("address.postcode").send_keys("Edited")
    driver.find_element_by_id("address.city").clear()
    driver.find_element_by_id("address.city").send_keys("London Edited")
    driver.find_element_by_id("address.region").clear()
    driver.find_element_by_id("address.region").send_keys("Westminster Edited")
    driver.find_element_by_id("address.country").clear()
    driver.find_element_by_id("address.country").send_keys("United Kingdom")
    site_page.click_submit()

    # Cleanup
    driver.find_element_by_xpath("//*[text()[contains(.,'Site 1')]]/following-sibling::td[last()]/a").click()
    driver.find_element_by_id("name").clear()
    driver.find_element_by_id("name").send_keys("Site 1")
    driver.find_element_by_id("address.address_line_1").clear()
    driver.find_element_by_id("address.address_line_1").send_keys("123 Cobalt Street")
    driver.find_element_by_id("address.postcode").clear()
    driver.find_element_by_id("address.postcode").send_keys("N23 6YL")
    driver.find_element_by_id("address.city").clear()
    driver.find_element_by_id("address.city").send_keys("London")
    driver.find_element_by_id("address.region").clear()
    driver.find_element_by_id("address.region").send_keys("Westminster")
    driver.find_element_by_id("address.country").clear()
    driver.find_element_by_id("address.country").send_keys("United Kingdom")
    site_page.click_submit()


def test_teardown(driver):
    driver.quit()

