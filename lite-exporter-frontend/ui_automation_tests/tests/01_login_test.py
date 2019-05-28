from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.applications_page import ApplicationsPage
import helpers.helpers as utils
import pytest
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.fixture(scope="function")
def open_exporter_hub(driver, exporter_url):
    # navigate to the application home page
    driver.get(exporter_url)
    # driver.maximize_window()
    assert driver.title == "Log In - LITE"
    log.info(driver.current_url)


def test_login_invalid_credentials(driver, open_exporter_hub):
    logging.info("Test Started")
    exporter_hub = ExporterHubPage(driver)

    exporter_hub.login("test@mail.com", "invalid")

    assert utils.is_element_present(driver, By.CSS_SELECTOR, ".govuk-error-message")
    assert "Enter a valid email/password combination" in driver.find_element_by_css_selector(".govuk-error-message").text


def test_login_valid_credentials(driver, open_exporter_hub):
    logging.info("Test Started")

    exporter_hub = ExporterHubPage(driver)
    exporter_hub.login("test@mail.com", "password")
    assert driver.title == "Exporter Hub - LITE"


def test_teardown(driver):
    driver.quit()
