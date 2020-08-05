from pytest_bdd import scenarios, then, given, when

from ui_automation_tests.pages.great_signin_page import GreatSigninPage
from ui_automation_tests.pages.register_organisation import RegisterOrganisation
from ui_automation_tests.pages.start_page import StartPage
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.api_client.sub_helpers.users import post_user_to_great_sso

scenarios("../features/register_an_organisation.feature", strict_gherkin=False)


@then("I should see a success page")
def success(driver):
    assert "successfully registered" in driver.title


@given("I register but I don't belong to an organisation")
def new_log_in(context):
    response = post_user_to_great_sso()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@when("I register a new commercial organisation")
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


@when("I register a new individual organisation")
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


@when("I sign as user without an organisation registered")  # noqa
def go_to_exporter_when(driver, exporter_url, context):  # noqa
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()

    if "login" in driver.current_url:
        GreatSigninPage(driver).sign_in(context.newly_registered_email, context.newly_registered_password)


@given("I am not logged in")
def not_logged_in(exporter_url, driver):
    driver.get(exporter_url.rstrip("/") + "/auth/logout")
    if "accounts/logout" in driver.current_url:
        driver.find_element_by_css_selector("[action='/sso/accounts/logout/'] button").click()
        driver.get(exporter_url)
