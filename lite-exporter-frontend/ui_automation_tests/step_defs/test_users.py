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
from conftest import context


@pytest.fixture(scope="function")
def open_exporter_hub(driver, exporter_url):
    driver.get(exporter_url)
    # driver.maximize_window()
    # assert driver.title == "Exporter Hub - LITE"
    log.info(driver.current_url)


def test_add_users(driver, open_exporter_hub, exporter_url):
    user_id = datetime.datetime.now().strftime("%m%d%H%M")
    first_name = "Test"
    last_name = "User" + user_id
    full_name = first_name + last_name
    email = full_name.lower() + "@mail.com"
    context.email_to_search = email
    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)
    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_users()

    # When I choose the option to manage users # Then I should see the current user for my company
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='test@mail.com']/following-sibling::td[text()='active']")

    # And I should have the ability to add a new user # And I can insert an name, last name email and password for user
    exporter_hub.click_add_a_user_btn()
    exporter_hub.enter_first_name(first_name)
    exporter_hub.enter_last_name(last_name)
    exporter_hub.enter_email(email)
    exporter_hub.enter_password("password")

    # When I Save
    exporter_hub.click_save_and_continue()

    # Then I return to "Manage users" # And I can see the original list of users
    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='active']")


def test_edit_users(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    full_name = "Test user_2"
    email = context.email_to_search
    password = "1234"
    email_edited = "testuser_2_edited@mail.com"
    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_edit_for_user(email)
    exporter_hub.enter_email(email_edited)
    exporter_hub.enter_first_name("Test_edited")
    exporter_hub.enter_last_name("user_2_edited")

    exporter_hub.click_submit()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'testuser_2_edited@mail.com')]]")

    exporter_hub.go_to(exporter_url)
    exporter_hub.click_users()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'testuser_2_edited1@mail.com')]]")

    exporter_hub.logout()
    exporter_hub.login(email_edited, password)

    # cleanup
    exporter_hub.click_users()
    exporter_hub.click_edit_for_user(email_edited)
    exporter_hub.enter_email(email)
    exporter_hub.enter_first_name("Test")
    exporter_hub.enter_last_name("user_2")
    exporter_hub.click_submit()


def test_deactivate_users(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    full_name = "Test user_1"
    email = "testuser_1@mail.com"
    password = "1234"

    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_user_name_link(full_name)

    # When I choose to deactivate an active user # Then I return to "Manage users"
    exporter_hub.click_deactivate_btn()

    # And I can see that the user is now deactivated
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='deactivated']")
    # Given I am a deactivated user # When I attempt to log in # And I cannot log in
    exporter_hub.logout()
    exporter_hub.login(email, password)
    assert "Enter a valid email/password" in driver.find_element_by_css_selector(".govuk-error-message").text


def test_reactivate_users(driver, open_exporter_hub, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    full_name = "Test user_1"
    email = "testuser_1@mail.com"
    password = "1234"

    # As a logged in user # I want to reactivate users who have previously been deactivated
    # So that returned users can perform actions in the system
    exporter_hub.click_users()

    # When I choose to activate a deactivated user # Then I am asked "Are you sure you want to re-activate"
    exporter_hub.click_user_name_link(full_name)
    exporter_hub.click_reactivate_btn()

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='active']"),\
        "user should status was expected to be active"

    # Given I am a reactivated I can log in
    exporter_hub.logout()
    exporter_hub.login(email, password)
    assert driver.title == "Exporter Hub - LITE"


def test_inability_to_deactivate_oneself(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")
    else:
        exporter_hub.go_to(exporter_url)

    exporter_hub.click_user_profile()
    assert "Test" in driver.find_element_by_tag_name("h1").text
    deactivate = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Deactivate')]]")
    assert not deactivate


def test_teardown(driver):
    driver.quit()
