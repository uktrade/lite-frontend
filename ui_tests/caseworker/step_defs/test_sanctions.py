from pytest_bdd import given, scenarios, then, parsers, when
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
    sanctions_h2 = driver.find_element(by=By.XPATH, value="//*[contains(text(),'Sanction matches')]")
    assert sanctions_h2 is not None


@then(parsers.parse("I see <end_user_name> listed there"))
def check_sanction_highlighted(driver, end_user_name):  # noqa
    name_element = driver.find_element(
        by=By.CSS_SELECTOR, value="#table-sanction-matches > tbody > tr > td:nth-child(4)"
    )
    assert name_element.text == end_user_name


@when('I select <end_user_name> and press remove sanction match')
def remove_sanctions_match(driver, end_user_name):
    # scroll_to_element_by_id(driver, "table-sanction-matches")
    #table-sanction-matches
    driver.find_element(by=By.ID, value="'#table-sanction-matches .govuk-checkboxes__input'").click()
    # tab.find_element(f"#table-sanction-matches {selectors.CHECKBOX}").click()
    driver.find_element_by_id("button-remove-sanction-matches").click()


@then(parsers.parse("I am asked to provide a reason"))
def provide_reason_to_remove(driver):  # noqa
    comment_text = driver.find_element(
        by=By.CSS_SELECTOR, value="#table-sanction-matches > tbody > tr > td:nth-child(4)"
    )
    comment_text.send_keys('remove sanction')
    comment_text.submit()


@then(parsers.parse("the sanction is removed from the case page"))
def check_removal(driver):    # noqa
    removed_message = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/text()")
    assert removed_message is not None
    sanctions_h2 = driver.find_element(by=By.XPATH, value="//*[contains(text(),'Sanction matches')]")
    assert sanctions_h2 is None
    
