import random
from pytest_bdd import given, when, then, scenarios
from pages.login_page import LoginPage

scenarios('../features/login.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@given('I go to SSO UAT login page')
def go_to_sso_login(driver, sso_sign_in_url):
    driver.get(sso_sign_in_url)


@when('I log in with invalid user')
def login_invalid_user(driver, invalid_username):
    login_page = LoginPage(driver)
    login_page.type_into_login_field(invalid_username + str(random.randint(1, 1001)))
    login_page.type_into_password_field("password")


@when('I click log in button')
def login_button_click(driver):
    login_page = LoginPage(driver)
    login_page.click_on_submit_button()


@then('I see you need to sign in error message')
def login_error_message(driver):
    assert "DIT system access" in driver.title

