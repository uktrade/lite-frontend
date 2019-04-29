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
def open_exporter_hub(driver, url):
    # navigate to the application home page
    driver.get(url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_add_goods(driver, open_exporter_hub, url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.login("test@mail.com", "password")

    time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Click My goods assert is on the my goods page
    exporter_hub.click_my_goods()
    exporter_hub.click_add_a_good()

    # Add good details
    exporter_hub.enter_description_of_goods("This is a description of good " + time_id)
    exporter_hub.select_is_your_good_controlled("Yes")
    exporter_hub.enter_control_code("ML6")
    exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
    exporter_hub.enter_part_number("part-123")
    exporter_hub.click_save_and_continue()

    # Assert good is added to the goods list on the goods page
    exporter_hub.verify_good_is_in_goods_list(time_id, "part-123", "ML6")

    logging.info("Test Complete")


def test_add_goods_to_application(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    # print("logging in as test@mail.com")
    # exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()

    log.info("Starting application")
    apply_for_licence.click_start_now_btn()
    logging.info("Clicked start button")
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_for_licence.enter_name_or_reference_for_application("Test Application " + app_time_id)
    apply_for_licence.click_save_and_continue()
    apply_for_licence.enter_destination("Cuba")
    apply_for_licence.click_save_and_continue()
    apply_for_licence.click_go_to_overview()
    apply_for_licence.click_goods_link()
    apply_for_licence.click_add_from_organisations_goods()
    apply_for_licence.add_good_to_application("part-123")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Quantity: A valid number is required.' in element.text
    assert 'Unit: This field may not be blank.' in element.text
    assert 'Value: A valid number is required.' in element.text

    apply_for_licence.enter_quantity("1")
    apply_for_licence.enter_value("1500")
    apply_for_licence.enter_unit_of_measurement("kg")

    apply_for_licence.click_save_and_continue()

    log.info("verifying goods added")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'part-123')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'1')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'1500.00')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'kg')]]")


def test_teardown(driver):
    driver.quit()
