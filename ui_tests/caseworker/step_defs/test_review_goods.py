from pytest_bdd import then, scenarios, parsers, when
from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_page import CasePage

scenarios("../features/review_goods.feature", strict_gherkin=False)


@then("I select the product and click on Review goods")
def select_product_for_review(driver):
    CasePage(driver).select_first_good()
    click_review_goods(driver)


@when("I select all goods")
def select_all_goods_for_review(driver):
    CasePage(driver).select_all_goods()


@when("I click review goods")
def click_review_goods(driver):
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


@when(parsers.parse('I input "{new_clc_entry}" as the control list entry'))
def input_clc_entry_during_review(driver, new_clc_entry):
    clear_clc_entry(driver)

    # input new entry
    clc_input_element = driver.find_element_by_class_name("tokenfield-input")
    clc_input_element.send_keys(new_clc_entry)
    clc_input_element.click()


@when("I leave control list entry field blank")
def clear_clc_entry(driver):
    # clear existing entries (click 'x' for each item which is a link)
    for element in driver.find_elements_by_class_name("tokenfield-set-item"):
        remove_btn = element.find_element_by_xpath(".//a")
        remove_btn.click()


@when("I select this product does not have a control list entry")
def select_no_clc_entry_checkbox(driver):
    driver.find_element(
        by=By.XPATH, value="//input[@type='checkbox' and contains(@name, 'does_not_have_control_list_entries')]"
    ).click()


@when(parsers.parse('I select "{option}" for is a licence required'))
def select_licence_required(driver, option):
    value = {"Yes": "True", "No": "False"}[option]
    driver.find_element(
        by=By.XPATH, value=f"//input[@type='radio' and contains(@name, 'is_good_controlled') and @value='{value}']"
    ).click()


@when(parsers.parse('I input "{summary}" as annual report summary'))
def input_annual_report_summary(driver, summary):
    summary_element = driver.find_element_by_id("report_summary")
    summary_element.clear()
    summary_element.send_keys(summary)


@then(parsers.parse('for the first good I see "{value}" for "{name}"'))
def check_first_goods_row(driver, value, name):
    assert value == CasePage(driver).get_goods_row_with_headers(row_num=1)[name]


@then(parsers.parse('for the second good I see "{value}" for "{name}"'))
def check_second_goods_row(driver, value, name):
    assert value == CasePage(driver).get_goods_row_with_headers(row_num=2)[name]


@then(parsers.parse('the product status is "{status}"'))
def check_product_rating_and_status(driver, status):
    product_table = driver.find_element_by_id("table-goods")
    status_element = product_table.find_element_by_xpath("//tbody/tr/td[7]/div/span")
    assert status_element.text == status
