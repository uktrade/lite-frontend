import datetime
import logging
from conftest import context
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
import helpers.helpers as utils

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
scenarios('../features/users.feature', strict_gherkin=False)


@when('I add user')
def add_user(driver):
    user_id = datetime.datetime.now().strftime("%m%d%H%M")
    first_name = "Test"
    last_name = "User" + user_id
    full_name = first_name + last_name
    email = full_name.lower() + "@mail.com"
    context.email_to_search = email
    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_users()

    # When I choose the option to manage users # Then I should see the current user for my company
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='test@mail.com']/following-sibling::td[text()='Active']")

    # And I should have the ability to add a new user # And I can insert an name, last name email and password for user
    exporter_hub.click_add_a_user_btn()
    exporter_hub.enter_first_name(first_name)
    exporter_hub.enter_last_name(last_name)
    exporter_hub.enter_email(email)
    exporter_hub.enter_password("password")

    # When I Save
    exporter_hub.click_save_and_continue()


@then('user is added')
def user_is_added(driver):
    # Then I return to "Manage users" # And I can see the original list of users
    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + context.email_to_search + "']/following-sibling::td[text()='Active']")


@when('I edit user then user is edited')
def user_is_edited(driver, exporter_url):
    user_id = datetime.datetime.now().strftime("%d%m%H%M")
    exporter_hub = ExporterHubPage(driver)

    full_name = "Test user_2"
    email = context.email_to_search
    password = "password"
    email_edited = "testuser_2_edited" + user_id+ "@mail.com"
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
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + email_edited + "')]]")

    exporter_hub.go_to(exporter_url)
    exporter_hub.click_users()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + email_edited + "')]]")

    exporter_hub.logout()
    exporter_hub.login("test@mail.com", password)

    # cleanup
    exporter_hub.click_users()
    exporter_hub.click_edit_for_user(email_edited)
    exporter_hub.enter_email(email)
    exporter_hub.enter_first_name("Test")
    context.last_name = "user_2"+user_id
    exporter_hub.enter_last_name(context.last_name)
    exporter_hub.click_submit()


@when('I deactivate user then user is deactivated')
def user_is_edited(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    context.full_name = "Test "+ context.last_name
    password = "1234"

    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_user_name_link(context.full_name)

    # When I choose to deactivate an active user # Then I return to "Manage users"
    exporter_hub.click_deactivate_btn()

    # And I can see that the user is now deactivated
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + context.email_to_search + "']/following-sibling::td[text()='Deactivated']")
    # Given I am a deactivated user # When I attempt to log in # And I cannot log in
    exporter_hub.logout()
    exporter_hub.login(context.email_to_search, password)
    assert "Enter a valid email/password" in driver.find_element_by_css_selector(".govuk-error-message").text


@when('I deactivate user then user is deactivated')
def user_deactivate(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    context.full_name = "Test "+ context.last_name
    password = "1234"

    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_user_name_link(context.full_name)

    # When I choose to deactivate an active user # Then I return to "Manage users"
    exporter_hub.click_deactivate_btn()

    # And I can see that the user is now deactivated
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + context.email_to_search + "']/following-sibling::td[text()='Deactivated']")
    # Given I am a deactivated user # When I attempt to log in # And I cannot log in
    exporter_hub.logout()
    exporter_hub.login(context.email_to_search, password)
    assert "Enter a valid email/password" in driver.find_element_by_css_selector(".govuk-error-message").text


@when('I reactivate user then user is reactivated')
def user_reactivate(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    email = "testuser_1@mail.com"
    password = "1234"

    # As a logged in user # I want to reactivate users who have previously been deactivated
    # So that returned users can perform actions in the system
    exporter_hub.click_users()

    # When I choose to activate a deactivated user # Then I am asked "Are you sure you want to re-activate"
    exporter_hub.click_user_name_link(context.full_name)
    exporter_hub.click_reactivate_btn()

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='Active']"),\
        "user should status was expected to be Active"

    # Given I am a reactivated I can log in
    exporter_hub.logout()
    exporter_hub.login(email, password)
    assert driver.title == "Exporter hub - LITE"


@when('I try to deactivate myself I cannot')
def cant_deactivate_self(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_user_profile()
    assert "Test" in driver.find_element_by_tag_name("h1").text
    deactivate = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Deactivate')]]")
    assert not deactivate

