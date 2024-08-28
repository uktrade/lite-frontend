from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By
from ui_tests.caseworker.pages.shared import Shared

scenarios("../../features/give_advice/lu_licence_change_status.feature", strict_gherkin=False)


@when("I click change licence status")
def click_change_licence_status(driver):
    driver.find_element(by=By.LINK_TEXT, value="Change status").click()


@when("I click suspend licence and submit")
def click_suspend_licence_status_and_submit(driver):
    driver.find_element(By.XPATH, "//input[@type='radio' and @value='suspended']").click()
    Shared(driver).click_submit()


@when("I confirm the suspension")
def click_continue(driver):
    Shared(driver).click_submit()


@then(parsers.parse('I see that licence status shows as "{status}"'))
def should_see_finalised_under_status(driver, status):
    element = driver.find_element(by=By.ID, value="licence-status-id")
    assert element.text == status
