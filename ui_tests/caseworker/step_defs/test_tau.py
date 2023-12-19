from faker import Faker
import time
from pytest_bdd import when, then, scenarios, parsers
from selenium.webdriver.common.by import By
from tests_common import functions
from selenium.webdriver.common.keys import Keys

from tests_common.helpers import applications

fake = Faker()

scenarios("../features/tau.feature", strict_gherkin=False)


@then("I select all goods")  # noqa
def select_all_goods(driver):  # noqa
    # Find the 'Select all' button by its class name and click it
    select_all_button = driver.find_element(By.CLASS_NAME, "assessment-form__select-all")
    select_all_button.click()


@when(parsers.parse('I create an application with re-used "{goods_name}" goods'))
def create_application_with_reused_goods(api_test_client, context, goods_name):  # noqa
    app_data = {
        "name": goods_name,
        "end_user_name": "Joe bloggs",
        "end_user_address": "123 Main street",
        "consignee_name": "Josephine Bloggs",
        "consignee_address": "123 Main Street",
        "country": "BL",
        "end_use": "Research and development",
    }
    applications.create_standard_application_with_reused_goods(api_test_client, context, app_data)


@then(parsers.parse('I check if the URL contains "{word}"'))  # noqa
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
    # good was not found in any row
    else:
        assert False, "No product found"

    approve_button = driver.find_element(By.CSS_SELECTOR, ".govuk-button.assessment-formset__action")
    approve_button.click()


@then(parsers.parse('I assert if "{good}" has been assessed'))  # noqa
def assert_if_good_is_assessed(driver, good):  # noqa
    unique_parent = driver.find_element(By.CSS_SELECTOR, ".assessment-formset")
    table = unique_parent.find_element(By.ID, "tau-form")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody .govuk-table__row")

    good_found = False
    for row in rows:
        # Check if good is in the row's text
        if good in row.text:
            good_found = True
            break

    assert good_found


@then(parsers.parse('I click on "{button_label}" button'))
def click_edit_assessments(driver, button_label):
    xpath = f"//button[contains(text(), '{button_label}')]"
    driver.find_element(By.XPATH, xpath).click()


@then("I edit the fields and checks if they were updated")  # noqa
def edit_assessment_fields(driver):
    # Adds control entry ML1c
    functions.send_tokens_to_token_bar(driver, "#div_id_form-0-control_list_entries .tokenfield-input", ["ML1c"])

    # Clear and adds prefix
    suggestion_input_autocomplete_prefix = driver.find_element(by=By.ID, value="_id_form-0-report_summary_prefix")
    suggestion_input_autocomplete_prefix.click()
    suggestion_input_autocomplete_prefix.send_keys(Keys.BACK_SPACE)
    suggestion_input_autocomplete_prefix.send_keys("components for")
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//body").click()

    # Clear and adds summary
    suggestion_input_autocomplete_summary = driver.find_element(by=By.ID, value="_id_form-0-report_summary_subject")
    suggestion_input_autocomplete_summary.click()
    suggestion_input_autocomplete_summary.send_keys(Keys.BACK_SPACE)
    suggestion_input_autocomplete_summary.send_keys("sniper rifles")
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//body").click()

    # Click Submit button
    xpath = f"//button[contains(text(), 'Submit')]"
    driver.find_element(By.XPATH, xpath).click()

    # Check the first row for edit changes
    unique_parent = driver.find_element(By.CSS_SELECTOR, ".assessment-formset")
    table = unique_parent.find_element(By.ID, "tau-form")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody .govuk-table__row")
    first_row_text = rows[0].text

    assert (
        "components for sniper rifles" in first_row_text
    ), "String components for sniper rifles not found in the first row"
    assert "ML1c" in first_row_text, "String ML1c not found in the first row"
