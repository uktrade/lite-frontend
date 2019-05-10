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

    time_id = datetime.datetime.now().strftime("%m%d%H%M")

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
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()
    log.info("Starting application")
    apply_for_licence.click_start_now_btn()
    logging.info("Clicked start button")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    apply_for_licence.enter_name_or_reference_for_application("Test Application " + time_id)
    apply_for_licence.click_save_and_continue()

    goods.enter_destination("Cuba")
    goods.click_save_and_continue()
    logging.info("Entered Destination and clicked save and continue")

    goods.enter_usage("communication")
    goods.click_save_and_continue()
    logging.info("Entered usage and clicked save and continue")

    goods.enter_activity("Proliferation")
    goods.click_save_and_continue()
    logging.info("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title

    apply_for_licence.click_goods_link()
    apply_for_licence.click_add_from_organisations_goods()
    apply_for_licence.add_good_to_application("Good T1")

    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Value: A valid number is required.' in element.text
    assert 'Quantity: A valid number is required.' in element.text

    apply_for_licence.enter_value("500")
    apply_for_licence.enter_quantity("1")
    apply_for_licence.select_unit_of_measurement("Gram")

    apply_for_licence.click_save_and_continue()

    log.info("verifying goods added")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='Good T1']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='1.0 grams']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='£500.00']")

    apply_for_licence.click_add_from_organisations_goods()
    apply_for_licence.add_good_to_application("Good T2")
    apply_for_licence.enter_value("1200")
    apply_for_licence.enter_quantity("12")
    apply_for_licence.select_unit_of_measurement("Grams")
    apply_for_licence.click_save_and_continue()

    log.info("verifying goods added")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='Good T2']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='G2-23']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='ML34a']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='1.0 grams']")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()='£1200.00']")


def test_search_for_goods_by_description(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()
    log.info("Starting application")
    goods.click_start_now_btn()
    logging.info("Clicked start button")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    goods.enter_name_or_reference_for_application("Test Application " + time_id)
    goods.click_save_and_continue()

    goods.enter_destination("Cuba")
    goods.click_save_and_continue()
    logging.info("Entered Destination and clicked save and continue")

    goods.enter_usage("communication")
    goods.click_save_and_continue()
    logging.info("Entered usage and clicked save and continue")

    goods.enter_activity("Proliferation")
    goods.click_save_and_continue()
    logging.info("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_description("Good T1")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1
    assert goods[0].find_element(By.TAG_NAME, "h4").text == "Good T1"


def test_search_for_goods_by_part_number(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()

    log.info("Starting application")
    goods.click_start_now_btn()
    logging.info("Clicked start button")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    goods.enter_name_or_reference_for_application("Test Application " + time_id)
    goods.click_save_and_continue()

    goods.enter_destination("Cuba")
    goods.click_save_and_continue()
    logging.info("Entered Destination and clicked save and continue")

    goods.enter_usage("communication")
    goods.click_save_and_continue()
    logging.info("Entered usage and clicked save and continue")

    goods.enter_activity("Proliferation")
    goods.click_save_and_continue()
    logging.info("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_part_number("G1-12")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1
    assert "G1-12" in goods[0].text


def test_remove_filter(driver,open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()

    log.info("Starting application")
    goods.click_start_now_btn()
    logging.info("Clicked start button")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    goods.enter_name_or_reference_for_application("Test Application " + time_id)
    goods.click_save_and_continue()
    goods.enter_destination("Cuba")
    goods.click_save_and_continue()
    logging.info("Entered Destination and clicked save and continue")

    goods.enter_usage("communication")
    goods.click_save_and_continue()
    logging.info("Entered usage and clicked save and continue")

    goods.enter_activity("Proliferation")
    goods.click_save_and_continue()
    logging.info("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_description("Good T1")
    goods.enter_part_number("G1-12")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1

    filter_tags = driver.find_elements_by_css_selector(".lite-filter-bar a")
    for tag in range(len(filter_tags)):
        driver.find_element_by_css_selector(".lite-filter-bar a").click()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) > 1


def test_teardown(driver):
    driver.quit()
