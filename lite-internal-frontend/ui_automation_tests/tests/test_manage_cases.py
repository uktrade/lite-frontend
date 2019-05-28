import unittest
import datetime
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.exporter_hub import ExporterHub
from pages.manage_cases_page import ManageCasesPage
import helpers.helpers as utils
import logging
import time
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

def test_change_status(driver, open_internal_hub, internal_url, exporter_url):
    log.info("Test Started")
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    manage_cases_page = ManageCasesPage(driver)

    # Submit application
    log.info("submitting application on Exporter Hub")
    exporter_hub.go_to(exporter_url)
    exporter_hub.login("test@mail.com", "password")
    time_id = datetime.datetime.now().strftime("%m%d%H%M%S")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Department Of International Trade Hub")

    # Verify Case is in the New Cases Work Queue
    log.info("Verifying Case is in the New Cases Work Queue")
    cases_table = driver.find_element_by_class_name("lite-table")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + app_id + "')]]")
    log.info("Application found in work queue")

    # check details page
    logging.info("Verifying the details of a specific case in a work queue...")

    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    # Progress application
    manage_cases_page.click_progress_application()

    manage_cases_page.select_status(status="Under review")

    manage_cases_page.click_save()

    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == "Under review"

    dit_hub_page.go_to(internal_url)

    # Check application status is changed
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]/../following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Under review"

    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_applications_btn()
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + time_id + "')]]/following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Under review"
    print("Test Complete")


def test_view_submitted_cases_in_work_queue(driver, open_internal_hub, exporter_url, internal_url):
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)

    log.info("Test Started")
    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    # Submit application
    log.info("submitting application on Exporter Hub")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Department Of International Trade Hub")

    # Verify Case is in the New Cases Work Queue
    log.info("Verifying Case is in the New Cases Work Queue")
    cases_table = driver.find_element_by_class_name("lite-table")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + app_id + "')]]")
    log.info("Application found in work queue")

    # check details page
    log.info("Verifying the details of a specific case in a work queue...")

    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    details = driver.find_elements_by_css_selector(".lite-heading-s")
    try:
        for header in details:
            if header.text == "CREATED BY":
                created_by_detail = header.find_element_by_xpath("./following-sibling::p").text
                assert created_by_detail == "John Smith"
                logging.info("created by: " + created_by_detail)
            if header.text == "ACTIVITY":
                activity_detail = header.find_element_by_xpath("./following-sibling::p").text
                assert activity_detail == "Testing"
                logging.info("activity: " + activity_detail)
            # if header.text == "CONTROL CODE":
            #     control_code_detail = header.find_element_by_xpath("./following-sibling::p").text
            #     assert control_code_detail == "code123"
            #     logging.info("control code: "+ control_code_detail)
            if header.text == "DESTINATION":
                destination_details = header.find_element_by_xpath("./following-sibling::p").text
                assert destination_details == "Cuba"
                logging.info("destination: " + destination_details)
            if header.text == "USAGE":
                usage_detail = header.find_element_by_xpath("./following-sibling::p").text
                assert usage_detail == "Test usage"
                logging.info("usage: " + usage_detail)
    except NoSuchElementException:
            logging.error("Applications details not found")

    log.info("Test Complete")


def test_record_decision(driver, open_internal_hub, exporter_url, internal_url):
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)

    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    # Submit application
    log.info("submitting application on Exporter Hub")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Department Of International Trade Hub")

    # check details page
    log.info("Clicking into application...")
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    # Record Decision
    record_decision_btn = driver.find_element_by_xpath("//*[text()[contains(.,'Record Decision')]]")
    record_decision_btn.click()

    # Grant Licence
    grant_licence_radio = driver.find_element_by_css_selector("label[for='radio-grant']")
    grant_licence_radio.click()
    log.info("granting Licence")

    save_btn = driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
    save_btn.click()

    log.info("Verifying status changed to approved")
    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == "Approved"

    dit_hub_page.go_to(internal_url)

    # Check application status is changed
    status = driver.find_element_by_xpath(
        "//*[text()[contains(.,'" + app_id + "')]]/../following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Approved"

    # Deny Licence
    logging.info("Denying Licence")
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    record_decision_btn = driver.find_element_by_xpath("//*[text()[contains(.,'Record Decision')]]")
    record_decision_btn.click()

    deny_licence_radio = driver.find_element_by_css_selector("label[for='radio-deny']")
    deny_licence_radio.click()

    save_btn = driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
    save_btn.click()

    logging.info("Verifying status changed to Declined")
    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == "Declined"

    dit_hub_page.go_to(internal_url)

    # Check application status is changed
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]/../following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Declined"
    print("Test Complete")


def test_teardown(driver):
    driver.quit()
