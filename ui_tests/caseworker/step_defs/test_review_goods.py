from tests_common import functions
from pytest_bdd import then, scenarios, parsers

from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_page import CasePage

scenarios("../features/review_goods.feature", strict_gherkin=False)


@then("I select the product and click on Review goods")
def select_product_for_review(driver):
    CasePage(driver).select_first_good()
    ApplicationPage(driver).click_review_goods()


@then("I click on Notes and timeline")
def click_on_notes_and_timeline(driver):
    ApplicationPage(driver).click_on_notes_and_timeline()


@then(parsers.parse('I add a case note "{case_note_text}" and click Post note'))
def add_case_note(driver, case_note_text):
    ApplicationPage(driver).enter_case_note(case_note_text)
    ApplicationPage(driver).click_post_note_btn()


@then("the control list is present on the case page")
def check_control_list_code(driver, context):
    goods = CasePage(driver).get_goods_text()
    assert context.goods_control_list_entry in goods


@then(parsers.parse('I update the control list entry to "{new_clc_entry}"'))
def update_clc_entry_during_review(driver, new_clc_entry):
    # clear existing entries (click 'x' for each item which is a link)
    for element in driver.find_elements_by_class_name("tokenfield-set-item"):
        remove_btn = element.find_element_by_xpath(".//a")
        remove_btn.click()

    # input new entry
    clc_input_element = driver.find_element_by_class_name("tokenfield-input")
    clc_input_element.send_keys(new_clc_entry)
    clc_input_element.click()


@then(parsers.parse('I input "{summary}" for annual report summary and submit'))
def input_annual_report_summary(driver, summary):
    summary_element = driver.find_element_by_id("report_summary")
    summary_element.clear()
    summary_element.send_keys(summary)

    save_btn = driver.find_element_by_class_name("govuk-button")
    save_btn.click()


@then(parsers.parse('the product status is "{status}"'))
def check_product_rating_and_status(driver, status):
    product_table = driver.find_element_by_id("table-goods")
    status_element = product_table.find_element_by_xpath("//tbody/tr/td[7]/div/span")
    assert status_element.text == status
