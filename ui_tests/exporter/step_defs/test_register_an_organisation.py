from bs4 import BeautifulSoup
from faker import Faker
from pytest_bdd import scenarios, then, given, when
from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.register_organisation import RegisterOrganisation
from ui_tests.exporter.pages.start_page import StartPage
from tests_common import functions
from tests_common.api_client.sub_helpers.users import create_govuk_sso_user
from ui_tests.exporter.fixtures.register_organisation import get_eori_number  # noqa
from ui_tests.exporter.pages.mock_signin_page import MockSigninPage

scenarios("../features/register_an_organisation.feature", strict_gherkin=False)

fake = Faker("en_GB")


@given("I register but I don't belong to an organisation")
def new_log_in(context):
    response = create_govuk_sso_user()
    context.newly_registered_email = response["email"]
    context.newly_registered_password = response["password"]


@given("I make sure that I am not logged in")
def not_logged_into_LITE(exporter_url, driver, context):
    driver.get(exporter_url.rstrip("/") + "/auth/logout")
    if "accounts/logout" in driver.current_url:
        driver.find_element(by=By.CSS_SELECTOR, value="[action='/sso/accounts/logout/'] button").click()
        driver.get(exporter_url)


@when("I enter company name")
def enter_company(driver):
    register = RegisterOrganisation(driver)
    register.enter_random_company_name()


@when("I enter company EORI number")
def enter_eori(driver, get_eori_number):
    register = RegisterOrganisation(driver)
    register.enter_random_eori_number(get_eori_number)


@when("I enter company SIC number")
def enter_sic(driver):
    register = RegisterOrganisation(driver)
    register.enter_random_sic_number()


@when("I enter company VAT number")
def enter_vat(driver):
    register = RegisterOrganisation(driver)
    register.enter_random_vat_number()


@when("I enter registration number and continue")
def enter_vat(driver):
    register = RegisterOrganisation(driver)
    register.enter_random_registration_number()
    functions.click_submit(driver)


@when("I enter random site details and finish submitting")
def enter_vat(driver):
    register = RegisterOrganisation(driver)
    register.enter_random_site()
    functions.click_submit(driver)
    functions.click_submit(driver)


@when("I sign in as a new user without an organisation registered")  # noqa
def go_to_exporter_when(driver, exporter_url):  # noqa
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()
    MockSigninPage(driver).sign_in(fake.email())

    driver.find_element(by=By.ID, value="id_first_name").send_keys(fake.first_name())
    driver.find_element(by=By.ID, value="id_last_name").send_keys(fake.last_name())
    driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']").click()


@then("I choose the Commercial organisation and continue")
def pick_commercial(driver):
    driver.find_element(By.ID, "id_REGISTRATION_TYPE-type_1").click()
    functions.click_submit(driver)


@then("I choose the Private invidual and continue")
def pick_individual(driver):
    driver.find_element(By.ID, "id_REGISTRATION_TYPE-type_2").click()
    functions.click_submit(driver)


@then("I choose the option In the United Kingdom and submit")
def select_uk(driver):
    driver.find_element(By.ID, "id_UK_BASED-location_1").click()
    functions.click_submit(driver)


@then("the organisation is registered successfully")
def organisation_registered_successfully(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    heading = soup.find(id="registration-confirmation-value").text.replace("\n", "").replace("\t", "").strip()
    message = soup.find(id="application-processing-message-value").text.replace("\n", "").replace("\t", "").strip()
    assert heading.startswith("You've successfully registered:") == True
    assert message == "We're currently processing your application."


@when("I click the logout link")
def click_the_logout_link(driver):
    driver.find_element(by=By.LINK_TEXT, value="Sign out").click()
