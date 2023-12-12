from faker import Faker
from pytest_bdd import when, then, scenarios, parsers
from selenium.webdriver.common.by import By

from tests_common.helpers import applications

fake = Faker()

scenarios("../features/tau.feature", strict_gherkin=False)


@then("I select all goods")  # noqa
def select_all_goods(driver):  # noqa
    # Find the 'Select all' button by its class name and click it
    select_all_button = driver.find_element(By.CLASS_NAME, "assessment-form__select-all")
    select_all_button.click()


@when("I create an application with reused goods")
def create_application(
    api_test_client,  # noqa
    context,  # noqa
):
    app_data = {
        "reuse": True,
        "name": "Reuse",
        "end_user_name": "Joe bloggs",
        "end_user_address": "123 Main street",
        "consignee_name": "Josephine Bloggs",
        "consignee_address": "123 Main Street",
        "country": "BL",
        "end_use": "Research and development",
    }
    applications.create_standard_application(api_test_client, context, app_data)


@then(parsers.parse('I check if URL contains "{word}"'))  # noqa
def check_url_for_template(driver, word):
    current_url = driver.current_url
    assert word in current_url


@then("I deselect all checkboxes")  # noqa
def deselect_all(driver):  # noqa
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "#tau-form .govuk-checkboxes__input")
    for checkbox in checkboxes:
        if checkbox.is_selected():
            checkbox.click()


@then(parsers.parse('I select good called "{good}" and approve and continue'))  # noqa
def select_row_good(driver, good):
    rows = driver.find_elements(By.CSS_SELECTOR, "#tau-form tbody .govuk-table__row")
    for row in rows:
        if good in row.text:
            checkbox = row.find_element(By.CSS_SELECTOR, ".govuk-checkboxes__input")
            if not checkbox.is_selected():
                checkbox.click()
            break
    approve_button = driver.find_element(By.CSS_SELECTOR, ".govuk-button.assessment-formset__action")
    approve_button.click()


@then(parsers.parse('Assert if "{good}" has been assessed'))  # noqa
def assert_if_good_is_assessed(driver, good):  # noqa
    unique_parent = driver.find_element(By.CSS_SELECTOR, ".assessment-formset")
    table = unique_parent.find_element(By.ID, "tau-form")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody .govuk-table__row")

    good_found = False
    for row in rows:
        # Check if "Rifle" is in the row's text
        if good in row.text:
            good_found = True
            break

    assert good_found
