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


@pytest.fixture(scope="function")
def open_exporter_hub(driver, url):
    # navigate to the application home page
    driver.get(url)
    # driver.maximize_window()
    assert driver.title == "Exporter Hub - LITE"


def test_start_draft_application(driver, open_exporter_hub, url):
    print("Test Started")
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    exporter_hub.go_to(url)
    exporter_hub.click_apply_for_a_licence()
    print("Clicked apply for a licence")

    apply_for_licence.click_start_now_btn()
    print("Clicked start button")

    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_for_licence.enter_name_or_reference_for_application("TestApp " + app_time_id)
    apply_for_licence.click_save_and_continue()
    print("Entered name of application and clicked save and continue")

    apply_for_licence.enter_control_code("000T")
    apply_for_licence.click_save_and_continue()
    print("Entered control code and clicked save and continue")

    apply_for_licence.enter_destination("Cuba")
    apply_for_licence.click_save_and_continue()
    print("Entered Destination and clicked save and continue")

    apply_for_licence.enter_usage("communication")
    apply_for_licence.click_save_and_continue()
    print("Entered usage and clicked save and continue")

    apply_for_licence.enter_activity("Proliferation")
    apply_for_licence.click_save_and_continue()
    print("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title
    print("On the application overview page")

    app_id = driver.current_url[-36:]
    exporter_hub.go_to(url)
    print("On Exporter Hub Page")

    # verify application is in drafts
    exporter_hub.click_drafts()
    print("Clicked drafts")

    drafts_table = driver.find_element_by_class_name("lite-table")
    drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + app_id + "')]").click()
    print("application found in list")
    print("clicked to open application")

    assert "Overview" in driver.title

    appName = driver.find_element_by_tag_name("h2").text
    assert "TestApp" in appName
    print("application opened to application overview")

    apply_for_licence.click_delete_application()
    assert 'Exporter Hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"

    print("Test Complete")


def test_submit_application(driver, open_exporter_hub, url):
    print("Test Started")
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)

    exporter_hub.go_to(url)
    exporter_hub.click_apply_for_a_licence()
    print("Clicked apply for a licence")

    apply_for_licence.click_start_now_btn()
    print("Clicked start button")

    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_for_licence.enter_name_or_reference_for_application("TestApp " + app_time_id)
    apply_for_licence.click_save_and_continue()
    print("Entered name of application and clicked save and continue")

    apply_for_licence.enter_control_code("000T")
    apply_for_licence.click_save_and_continue()
    print("Entered control code and clicked save and continue")

    apply_for_licence.enter_destination("Cuba")
    apply_for_licence.click_save_and_continue()
    print("Entered Destination and clicked save and continue")

    apply_for_licence.enter_usage("communication")
    apply_for_licence.click_save_and_continue()
    print("Entered usage and clicked save and continue")

    apply_for_licence.enter_activity("Proliferation")
    apply_for_licence.click_save_and_continue()
    print("Entered Activity and clicked save and continue")

    assert "Overview" in driver.title
    print("On the application overview page")

    apply_for_licence.click_submit_application()

    application_complete = driver.find_element_by_tag_name("h1").text
    assert "Application complete" in application_complete

    exporter_hub.go_to(url)
    print("On Exporter Hub Page")

    # verify application is in drafts
    exporter_hub.click_applications()
    print("Clicked Applications")

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + app_time_id + "')]]")
    print("application found in submitted applications list")

    # Check application status is Submitted
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + app_time_id + "')]]/following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Submitted"
    print("Test Complete")


def test_must_enter_fields_for_application(driver, open_exporter_hub):
    print("Test Started")

    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    exporter_hub.click_apply_for_a_licence()
    print("Clicked apply for a licence")
    apply_for_licence.click_start_now_btn()
    print("Clicked start button")

    print("no name or reference entered")
    print("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Name: This field may not be blank.' in element.text
    print("Error displayed successfully")

    apply_for_licence.enter_name_or_reference_for_application("a")
    apply_for_licence.click_save_and_continue()

    print("no control code entered")
    print("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Control_Code: This field may not be blank.' in element.text
    print("Error displayed successfully")

    apply_for_licence.enter_control_code("b")
    apply_for_licence.click_save_and_continue()

    print("no Destination entered")
    print("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Destination: This field may not be blank.' in element.text
    print("Error displayed successfully")

    apply_for_licence.enter_destination("c")
    apply_for_licence.click_save_and_continue()

    print("no Usage entered")
    print("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Usage: This field may not be blank.' in element.text
    print("Error displayed successfully")

    apply_for_licence.enter_usage("d")
    apply_for_licence.click_save_and_continue()

    print("no Activity entered")
    print("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'Activity: This field may not be blank.' in element.text
    print("Error displayed successfully")

    apply_for_licence.enter_activity("e")
    apply_for_licence.click_save_and_continue()
    print("Error displayed successfully")
    print("Test Complete")

    apply_for_licence.click_delete_application()
    assert 'Exporter Hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"


def test_status_column_and_refresh_btn_on_applications(driver, open_exporter_hub):
    print("Test Started")
    exporter_hub = ExporterHubPage(driver)
    applications = ApplicationsPage(driver)

    exporter_hub.click_applications()
    print("navigated to applications page")

    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    print("Status column is displayed")

    applications.click_refresh_btn()
    print("clicked refresh button")

    print("Test Complete")


def test_teardown(driver):
    driver.quit()
