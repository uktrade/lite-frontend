from pytest_bdd import given, scenarios, then, parsers
from selenium.webdriver.common.by import By

from tests_common import selectors
from tests_common.tools.helpers import scroll_to_element_by_id


scenarios("../features/sanctions.feature", strict_gherkin=False)


@given("I want to check that the sanction match is highlighted")  # noqa
def check_sanction(driver, sso_sign_in):  # noqa
    pass


@given("For a case is created with a name on it that has a sanction")  # noqa
def sanctioned_case(driver, sso_sign_in):  # noqa
    pass

@then(parsers.parse("I see the section of the case page entitled Sanction matches"))
def check_sanction_matches(driver, end_user_name, end_user_address):  # noqa
    sanctions_h2 = driver.findElement (By.xpath ("//*[contains(text(),'Sanction matches')]"))
    assert sanctions_h2 is not None


@then(parsers.parse('I see "{end_user_name}" listed there'))
def check_sanction_highlighted(driver, end_user_name, end_user_address):  # noqa
    sanctions_table = driver.find_element(by=By.ID, value="table-sanction-matches")
    name_element = sanctions_table.find_element(by=By.XPATH, value="//tbody/tr/td[4]")
    assert name_element.text == end_user_name

def remove_sanctions_match(self):
    scroll_to_element_by_id(self.driver, "table-sanction-matches")
    self.driver.find_element_by_css_selector(f"#table-sanction-matches {selectors.CHECKBOX}").click()
    self.driver.find_element_by_id("button-remove-sanction-matches").click()
