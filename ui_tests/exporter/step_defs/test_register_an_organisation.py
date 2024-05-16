from django.conf import settings
from bs4 import BeautifulSoup
from faker import Faker
from pytest_bdd import scenarios, then, given, when, parsers

from selenium.webdriver.common.by import By

import tests_common.tools.helpers as utils
from ui_tests.exporter.fixtures.register_organisation import get_eori_number
from ui_tests.exporter.pages.govuk_signin_page import GovukSigninPage
from ui_tests.exporter.pages.register_organisation import RegisterOrganisation
from ui_tests.exporter.pages.mock_signin_page import MockSigninPage
from ui_tests.exporter.pages.start_page import StartPage
from tests_common import functions
from tests_common.api_client.sub_helpers.users import create_govuk_sso_user
from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.fixtures.sso_sign_in import sso_sign_in


scenarios("../features/register_an_organisation.feature", strict_gherkin=False)

@given("I register but I don't belong to an organisation")
def new_log_in(context):
    response = create_govuk_sso_user()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@when("I enter my information from steps 1-4 to register a commercial organisation")
def register_commercial(driver, get_eori_number):
    register = RegisterOrganisation(driver)
    register.click_create_an_account_button()
    register.select_commercial_or_individual_organisation("commercial")
    functions.click_submit(driver)
    register.click_inside_of_uk_location()
    functions.click_submit(driver)
    register.enter_random_company_name()
    register.enter_random_eori_number(get_eori_number)
    register.enter_random_sic_number()
    register.enter_random_vat_number()
    register.enter_random_registration_number()
    functions.click_submit(driver)
    register.enter_random_site()
    functions.click_submit(driver)
    functions.click_finish_button(driver)


def register_individual(driver):
    register = RegisterOrganisation(driver)
    register.click_create_an_account_button()
    register.select_commercial_or_individual_organisation("individual")
    functions.click_submit(driver)
    register.click_outside_of_uk_location()
    functions.click_submit(driver)
    register.enter_random_company_name()
    functions.click_submit(driver)
    register.enter_random_site_with_country_and_address_box()
    functions.click_submit(driver)
    functions.click_finish_button(driver)


@when("I sign in as user without an organisation registered")  # noqa
def go_to_exporter_when(driver, exporter_url, context):  # noqa
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()

    if "signin" in driver.current_url:
        GovukSigninPage(driver).sign_in(context.newly_registered_email, context.newly_registered_password)


@given("I am not signed into LITE but signed into GREAT SSO")
def not_logged_into_LITE(exporter_url, driver, context):
    driver.get(exporter_url.rstrip("/") + "/auth/logout")
    if "accounts/logout" in driver.current_url:
        driver.find_element(by=By.CSS_SELECTOR, value="[action='/sso/accounts/logout/'] button").click()
        driver.get(exporter_url)

    response = create_govuk_sso_user()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@then("the organisation is registered successfully")
def organisation_registered_successfully(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    heading = soup.find(id="registration-confirmation-value").text.replace("\n", "").replace("\t", "").strip()
    message = soup.find(id="application-processing-message-value").text.replace("\n", "").replace("\t", "").strip()
    assert heading.startswith("You've successfully registered:") == True
    assert message == "We're currently processing your application."

# fake = Faker("en_GB")


# @given("I register but I don't belong to an organisation")
# def new_log_in(context):
#     response = create_govuk_sso_user()
#     context.newly_registered_email = response["email"]
#     context.newly_registered_password = response["password"]


# @when("I enter my information to register a commercial organisation")
# def register_commercial(driver, get_eori_number):

#     register = RegisterOrganisation(driver)
#     register.enter_random_company_name()
#     register.enter_random_eori_number(get_eori_number)
#     register.enter_random_sic_number()
#     register.enter_random_vat_number()
#     register.enter_random_registration_number()
#     functions.click_submit(driver)

#     register.enter_random_site()
#     functions.click_submit(driver)
#     functions.click_submit(driver)


# @when("I enter my information to register an individual organisation")
# def register_individual(driver, get_eori_number):
#     register = RegisterOrganisation(driver)
#     register.enter_random_company_name()
#     register.enter_random_eori_number(get_eori_number)
#     register.enter_random_registration_number()
#     functions.click_submit(driver)

#     register.enter_random_site()
#     functions.click_submit(driver)
#     functions.click_submit(driver)


# @when("I sign in as a new user without an organisation registered")  # noqa
# def go_to_exporter_when(driver, exporter_url, context):  # noqa
#     driver.get(exporter_url)
#     StartPage(driver).try_click_sign_in_button()
#     driver.find_element(by=By.LINK_TEXT, value="Sign out").click()
#     StartPage(driver).try_click_sign_in_button()

#     if "signin" in driver.current_url and not settings.MOCK_SSO_ACTIVATE_ENDPOINTS:
#         GovukSigninPage(driver).sign_in(fake.email(), fake.password())

#     if settings.MOCK_SSO_ACTIVATE_ENDPOINTS and not getattr(settings, "MOCK_SSO_USER_EMAIL", None):
#         MockSigninPage(driver).sign_in(fake.email())

#         driver.find_element(by=By.ID, value="id_first_name").send_keys(fake.first_name())
#         driver.find_element(by=By.ID, value="id_last_name").send_keys(fake.last_name())
#         driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']").click()
        


# @then(parsers.parse('I pick an organisation "{organisation}"'))
# def pick_org(driver, organisation):
#     if "register-an-organisation" in driver.current_url:
#         no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), organisation)
#         Shared(driver).click_on_radio_buttons(no)
#         functions.click_submit(driver)
#     else:
#         assert False


# @then(parsers.parse('I choose the option "{option}"'))
# def pick_option(driver, option):
#     no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), option)
#     Shared(driver).click_on_radio_buttons(no)
#     functions.click_submit(driver)


# @given("I am not signed into LITE but signed into GREAT SSO")
# def not_logged_into_LITE(exporter_url, driver, context):
#     driver.get(exporter_url.rstrip("/") + "/auth/logout")
#     if "accounts/logout" in driver.current_url:
#         driver.find_element(by=By.CSS_SELECTOR, value="[action='/sso/accounts/logout/'] button").click()
#         driver.get(exporter_url)

#     response = create_govuk_sso_user()
#     context.newly_registered_email = response["email"]
#     context.newly_registered_password = response["password"]


# @then("the organisation is registered successfully")
# def organisation_registered_successfully(driver):
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     heading = soup.find(id="registration-confirmation-value").text.replace("\n", "").replace("\t", "").strip()
#     message = soup.find(id="application-processing-message-value").text.replace("\n", "").replace("\t", "").strip()
#     assert heading.startswith("You've successfully registered:") == True
#     assert message == "We're currently processing your application."

# @when("I click the logout link")
# def click_the_logout_link(driver):
#     driver.find_element(by=By.LINK_TEXT, value="Sign out").click()