from pytest_bdd import given, scenarios, then, parsers, when
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tests_common import selectors


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


@when("I select <end_user_name> and press remove sanction match")
def click_remove_sanctions_match(driver, end_user_name):  # noqa
    checkbox_element = driver.find_element(
        by=By.CSS_SELECTOR, value="#table-sanction-matches > tbody > tr > td:nth-child(1)"
    )
    checkbox_element.find_element(by=By.CSS_SELECTOR, value=f"#table-sanction-matches {selectors.CHECKBOX}").click()
    driver.find_element(by=By.ID, value="button-remove-sanction-matches").click()


@then(parsers.parse("I am asked to provide a reason"))
def provide_reason_to_remove(driver):  # noqa
    comment_text = driver.find_element(by=By.CSS_SELECTOR, value="#id_comment")
    comment_text.send_keys("test remove sanction")
    comment_text.submit()


@then(parsers.parse("the sanction is removed from the case page"))
def check_removal(driver):  # noqa
    banner = driver.find_element(by=By.CLASS_NAME, value="app-snackbar__content")
    assert "Sanction match successfully removed" in banner.text
    try:
        driver.find_element(by=By.XPATH, value="//*[contains(text(),'Sanction matches')]")
    except NoSuchElementException:
        pass
