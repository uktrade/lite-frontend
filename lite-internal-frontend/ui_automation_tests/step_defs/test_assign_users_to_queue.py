from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.case_list_page import CaseListPage
from pages.shared import Shared

scenarios('../features/users_to_queue.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I select the checkbox for previously created case to be assigned')
def click_checkbox_for_application(driver, internal_url, apply_for_standard_application, context):
    driver.get(internal_url)
    href = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").get_attribute('href')
    context.case_id_split_by_slash = href.split('/')[4]
    CaseListPage(driver).click_on_case_checkbox(context.case_id_split_by_slash)
    CaseListPage(driver).click_on_assign_users_button()


@when(parsers.parse('I select user to assign "{name}"'))
def assign_user_to_case(driver, name, context):
    driver.find_element_by_id(name).click()
    context.user_name = name
    Shared(driver).click_submit()


@then('user is assignee on case list')
def user_is_on_case_list(driver, context):
    assert context.user_name in CaseListPage(driver).get_text_of_assignees(context.app_id)


@then(parsers.parse('only "{name}" is displayed in user list for assign cases'))
def user_is_on_case_list(driver, name):
    elements = CaseListPage(driver).get_text_checkbox_elements()
    for element in elements:
        assert name in element.text


@then('user is not assignee on case list')
def user_is_not_on_case_list(driver, context):
    assert "No users assigned" in CaseListPage(driver).get_text_of_assignees(context.app_id)


@when("I click select all cases checkbox")
def select_all_cases(driver):
    CaseListPage(driver).click_select_all_checkbox()


@when(parsers.parse('I search for "{name}" to assign'))
def filter_search_for_assign_users(driver, name):
    CaseListPage(driver).enter_name_to_filter_search_box(name)


@then(parsers.parse('assign users button is "{enabled_disabled}"'))
def assign_user_to_case(driver, enabled_disabled):
    if enabled_disabled == "enabled":
        assert "disabled" not in CaseListPage(driver).get_class_name_of_assign_users_button()
    elif enabled_disabled == "disabled":
        assert "disabled" in CaseListPage(driver).get_class_name_of_assign_users_button()
