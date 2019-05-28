from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.exporter_hub_page import ExporterHubPage
from pages.internal_hub_page import InternalHubPage
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
    # assert driver.title == "Exporter Hub - LITE"
    log.info(driver.current_url)


def test_site_goods(driver, open_exporter_hub, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    log.info("logging in as test@mail.com")
    exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)

    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    exporter_hub.click_sites_link()
    exporter_hub.click_sites_checkbox(0)
    apply_for_licence.click_save_and_continue()


def test_site_goods_empty(driver, open_exporter_hub, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)
    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    exporter_hub.click_sites_link()
    apply_for_licence.click_save_and_continue()
    assert "You have to pick at least one site." in driver.find_element_by_css_selector(".govuk-error-message").text


def test_change_goods_sites(driver, open_exporter_hub, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)
    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    exporter_hub.click_sites_link()
    exporter_hub.click_sites_checkbox(0)
    apply_for_licence.click_save_and_continue()

    exporter_hub.click_sites_link()
    assert exporter_hub.get_checked_attributes_of_sites_checkbox(0) == "true"
    exporter_hub.click_sites_checkbox(0)
    assert exporter_hub.get_checked_attributes_of_sites_checkbox(0) is not "true"
    exporter_hub.click_sites_checkbox(1)
    assert exporter_hub.get_checked_attributes_of_sites_checkbox(1) == "true"
    apply_for_licence.click_save_and_continue()


def test_add_site(driver, open_exporter_hub, exporter_url):
    time_id = datetime.datetime.now().strftime("%m%d%H%M")

    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)
    site_page = InternalHubPage(driver)

    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_sites()
    exporter_hub.click_new_site()
    new_site_name = "New Site " + time_id
    driver.find_element_by_id("name").send_keys(new_site_name)
    driver.find_element_by_id("address.address_line_1").send_keys("1234")
    driver.find_element_by_id("address.postcode").send_keys("1234")
    driver.find_element_by_id("address.city").send_keys("1234")
    driver.find_element_by_id("address.region").send_keys("1234")
    driver.find_element_by_id("address.country").send_keys("1234")
    site_page.click_submit()

    assert driver.find_element_by_tag_name("h1").text == "Sites", \
        "Failed to return to Sites list page after Adding site"

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'New Site "+time_id+"')]]")
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    exporter_hub.go_to(exporter_url)

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)
    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    exporter_hub.click_sites_link()

    assert exporter_hub.get_text_of_site(len(driver.find_elements_by_css_selector(".govuk-checkboxes__label"))-1) == new_site_name


def test_teardown(driver):
    driver.quit()
