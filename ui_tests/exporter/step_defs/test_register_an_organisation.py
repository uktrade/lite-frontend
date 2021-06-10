from bs4 import BeautifulSoup
from pytest_bdd import scenarios, then, given, when

from ui_tests.exporter.pages.great_signin_page import GreatSigninPage
from ui_tests.exporter.pages.register_organisation import RegisterOrganisation
from ui_tests.exporter.pages.start_page import StartPage
from tests_common import functions
from tests_common.api_client.sub_helpers.users import create_great_sso_user

scenarios("../features/register_an_organisation.feature", strict_gherkin=False)


@given("I register but I don't belong to an organisation")
def new_log_in(context):
    response = create_great_sso_user()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@when("I enter my information from steps 1-4 to register a commercial organisation")
def register_commercial(driver):
    register = RegisterOrganisation(driver)
    register.click_create_an_account_button()
    register.select_commercial_or_individual_organisation("commercial")
    functions.click_submit(driver)
    register.click_inside_of_uk_location()
    functions.click_submit(driver)
    register.enter_random_company_name()
    register.enter_random_eori_number()
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

    if "login" in driver.current_url:
        GreatSigninPage(driver).sign_in(context.newly_registered_email, context.newly_registered_password)


@given("I am not signed into LITE but signed into GREAT SSO")
def not_logged_into_LITE(exporter_url, driver, context):
    driver.get(exporter_url.rstrip("/") + "/auth/logout")
    if "accounts/logout" in driver.current_url:
        driver.find_element_by_css_selector("[action='/sso/accounts/logout/'] button").click()
        driver.get(exporter_url)

    response = create_great_sso_user()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@then("the organisation is registered successfully")
def organisation_registered_successfully(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    heading = soup.find(id="registration-confirmation-value").text.replace("\n", "").replace("\t", "").strip()
    message = soup.find(id="application-processing-message-value").text.replace("\n", "").replace("\t", "").strip()
    assert heading.startswith("You've successfully registered:") == True
    assert message == "We're currently processing your application."
