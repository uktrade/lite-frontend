import datetime
import logging

from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

from conf.settings import env
from pages.exporter_hub_page import ExporterHubPage
import helpers.helpers as utils

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
scenarios('../features/users.feature', strict_gherkin=False)


@when('I click on the users link')
def click_users_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()


@when('I add the second test user')
def add_second_test_user(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()
    exists = 'Testy McTestFace' in driver.find_element_by_css_selector('.govuk-table').text
    if not exists:
        exporter_hub.click_add_a_user_btn()
        exporter_hub.enter_first_name("Testy")
        exporter_hub.enter_last_name("McTestFace")
        exporter_hub.enter_add_user_email(env('TEST_EXPORTER_SSO_EMAIL2'))
        exporter_hub.click_save_and_continue()


@then('I add a user')
def add_user(driver):
    exporter_hub = ExporterHubPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//td[text()[contains(.,'testuser_1@mail.com')]]")
    if not exists:
        for x in range(3):
            i = str(x + 1)
            exporter_hub.click_add_a_user_btn()
            exporter_hub.enter_first_name("Test")
            exporter_hub.enter_last_name("user_" + i)
            exporter_hub.enter_add_user_email("testuser_" + i + "@mail.com")
            exporter_hub.click_save_and_continue()


@when('I add user')
def add_user(driver, context, exporter_sso_login_info):
    user_id = datetime.datetime.now().strftime("%H%M%S")
    first_name = "Test"
    last_name = "User" + user_id
    full_name = first_name + last_name
    context.added_user_name = full_name
    email = full_name.lower() + "@mail.com"
    context.email_to_search = email
    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_users()
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    # When I choose the option to manage users # Then I should see the current user for my company
    no = utils.get_element_index_by_text(elements, exporter_sso_login_info["email"])
    assert 'Active' in elements[no].text
    # And I should have the ability to add a new user # And I can insert an name, last name email and password for user
    exporter_hub.click_add_a_user_btn()
    exporter_hub.enter_first_name(first_name)
    exporter_hub.enter_last_name(last_name)
    exporter_hub.enter_add_user_email(email)

    # When I Save
    exporter_hub.click_save_and_continue()


@then('user is added')
def user_is_added(driver, context):
    # Then I return to "Manage users" # And I can see the original list of users
    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = utils.get_element_index_by_text(elements, context.email_to_search)
    assert 'Active' in elements[no].text


@when('I edit user then user is edited')
def user_is_edited(driver, exporter_url, context, exporter_sso_login_info):
    user_id = datetime.datetime.now().strftime("%d%m%H%M")
    exporter_hub = ExporterHubPage(driver)

    full_name = "Test user_2"
    email = context.email_to_search

    email_edited = "testuser_2_edited" + user_id+ "@mail.com"
    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_edit_for_user(email)
    exporter_hub.enter_add_user_email(email_edited)
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


@when('I deactivate user then user is deactivated')
def user_is_deactivated(driver, exporter_url, context, request):
    exporter_hub = ExporterHubPage(driver)


    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_user_name_link("Testy McTestFace")

    # When I choose to deactivate an active user # Then I return to "Manage users"
    exporter_hub.click_deactivate_btn()

    # And I can see that the user is now deactivated
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    # When I choose the option to manage users # Then I should see the current user for my company
    no = utils.get_element_index_by_text(elements, 'Testy McTestFace')
    assert 'Deactivated' in elements[no].text, \
        "user should status was expected to be Deactivated"

    # Given I am a deactivated user # When I attempt to log in # And I cannot log in
    exporter_hub.logout()
    driver.find_element_by_id('header-sign-in-link').click()
    exporter_hub.login(env('TEST_EXPORTER_SSO_EMAIL2'), env('TEST_EXPORTER_SSO_PASSWORD2'))
    driver.get(request.config.getoption("--exporter_url"))


    assert driver.find_element_by_css_selector('.govuk-heading-xl').text == 'User not found'

    driver.get("https://great.uat.uktrade.io/sso/accounts/")
    driver.find_element_by_id("header-sign-out-link").click()
    driver.find_element_by_css_selector('.button').click()

    exporter_hub.login(env('TEST_EXPORTER_SSO_EMAIL'), env('TEST_EXPORTER_SSO_PASSWORD'))
    driver.get(request.config.getoption("--exporter_url"))


@when('I reactivate user then user is reactivated')
def user_reactivate(driver, exporter_url, context):
    exporter_hub = ExporterHubPage(driver)
    email = "testuser_1@mail.com"

    # As a logged in user # I want to reactivate users who have previously been deactivated
    # So that returned users can perform actions in the system
    exporter_hub.click_users()

    # When I choose to activate a deactivated user # Then I am asked "Are you sure you want to re-activate"
    exporter_hub.click_user_name_link('Testy McTestFace')
    exporter_hub.click_reactivate_btn()
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    # When I choose the option to manage users # Then I should see the current user for my company
    no = utils.get_element_index_by_text(elements, 'Testy McTestFace')
    assert 'Active' in elements[no].text, \
        "user should status was expected to be Active"


@when('I try to deactivate myself I cannot')
def cant_deactivate_self(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_user_profile()
    assert "Test" in driver.find_element_by_tag_name("h1").text
    deactivate = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Deactivate')]]")
    assert not deactivate

