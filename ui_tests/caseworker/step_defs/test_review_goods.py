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


@then(parsers.parse('I add a case note "{case_note_text}" and click Post note'))
def add_case_note(driver, case_note_text):
    ApplicationPage(driver).enter_case_note(case_note_text)
    ApplicationPage(driver).click_post_note_btn()


@when(parsers.parse('I select "{option}" for is a licence required'))
def select_licence_required(driver, option):
    value = {"Yes": "True", "No": "False"}[option]
    driver.find_element(
        by=By.XPATH, value=f"//input[@type='radio' and contains(@name, 'is_good_controlled') and @value='{value}']"
    ).click()


@when(parsers.parse('I input "{summary}" as annual report summary'))
def input_annual_report_summary(driver, summary):
    summary_element = driver.find_element(by=By.ID, value="report_summary")
    summary_element.clear()
    summary_element.send_keys(summary)


@then(parsers.parse('the product status is "{status}"'))
def check_product_rating_and_status(driver, status):
    product_table = driver.find_element(by=By.ID, value="table-goods")
    status_element = product_table.find_element(by=By.XPATH, value="//tbody/tr/td[7]/div/span")
    assert status_element.text == status
