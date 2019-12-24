from selenium.common.exceptions import NoSuchElementException

import shared.tools.helpers as utils
from pages.shared import Shared
from pytest_bdd import when, then, scenarios
from pages.application_page import ApplicationPage

scenarios("../features/assign_case_flags_to_case.feature", strict_gherkin=False)


@when("I click edit flags link")
def click_edit_case_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.click_edit_case_flags()


@when("I click edit goods flags link")
def click_edit_goods_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.select_a_good()
    application_page.click_edit_good_flags()


@then("The previously created flag is assigned to the case")
def assert_flag_is_assigned(driver, context):
    application_page = ApplicationPage(driver)
    exists = application_page.is_flag_applied(context.flag_name)
    assert exists is True


@then("the previously created goods flag is assigned to the case")
def assert_flag_is_assigned(driver, context):
    application_page = ApplicationPage(driver)
    assert application_page.is_good_flag_applied(context.flag_name)


@when("I add a flag called Suspicious at level Good")
def add_a_suspicious_flag(driver, add_suspicious_flag):
    pass


@when("I add a flag called New at level Case")
def add_a_suspicious_flag(driver, add_new_flag):
    pass


@then("I see 3 out of text")
def three_out_of_text(driver, context):
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    assert "(3 of " in elements[no].text


@then("I dont see 3 out of text")
def dont_see_three_out_of(driver, context):
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    assert "(3 of " not in elements[no].text


@when("I click chevron")  # noqa
def click_chevron(driver, context):
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    try:
        if elements[no].find_element_by_id("chevron").is_displayed():
            element = elements[no].find_element_by_css_selector(".lite-accordian-table__chevron")
            element.click()
    except NoSuchElementException:
        pass
    driver.set_timeout_to(10)
