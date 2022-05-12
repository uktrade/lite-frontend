from pytest_bdd import given, scenarios, then, parsers
from selenium.webdriver.common.by import By


scenarios("../features/sanctions.feature", strict_gherkin=False)


@given("I want to check that the sanction match is highlighted")  # noqa
def check_sanction(driver, sso_sign_in):  # noqa
    pass


@given("For a case is created with a name on it that has a sanction")  # noqa
def sanctioned_case(driver, sso_sign_in):  # noqa
    pass


@then(parsers.parse('I should see that the sanction match is highlighted as "{end_user_name}", "{end_user_address}"'))
def check_sanction_highlighted(driver, end_user_name, end_user_address):  # noqa
    sanctions_table = driver.find_element(by=By.ID, value="table-sanction-matches")
    name_element = sanctions_table.find_element(by=By.XPATH, value="//tbody/tr/td[4]")
    assert name_element.text == end_user_name
