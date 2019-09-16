from pytest_bdd import when, then, parsers, scenarios
from pages.case_list_page import CaseListPage
from pages.shared import Shared

scenarios('../features/users_to_queue.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I select the checkbox for previously created case to be assigned')
def click_checkbox_for_application(driver, internal_url, apply_for_standard_application, context):
    CaseListPage(driver).click_on_case_checkbox(context.case_id)
    CaseListPage(driver).click_on_assign_users_button()


@when('I select user to assign SSO users name')
def assign_user_to_case(driver, sso_users_name, context):
    driver.find_element_by_id(sso_users_name).click()
    context.user_name = sso_users_name
    Shared(driver).click_submit()


@then('user is assignee on case list')
def user_is_on_case_list(driver, context):
    assert context.user_name in CaseListPage(driver).get_text_of_assignees(context.case_id), "user name " + context.user_name + " is not an assignee on case list"


@then('only SSO users name is displayed in user list for assign cases')
def user_is_on_case_list(driver, sso_users_name):
    elements = CaseListPage(driver).get_text_checkbox_elements()
    for element in elements:
        assert sso_users_name in element.text, sso_users_name + "is not displayed in user list"


@then('user is not assignee on case list')
def user_is_not_on_case_list(driver, context):
    assert "No users assigned" in CaseListPage(driver).get_text_of_assignees(context.case_id), "No users assigned text is not displayed"


@when("I click select all cases checkbox")
def select_all_cases(driver):
    CaseListPage(driver).click_select_all_checkbox()


@when('I search for SSO users name to assign')
def filter_search_for_assign_users(driver, sso_users_name):
    CaseListPage(driver).enter_name_to_filter_search_box(sso_users_name)


@then(parsers.parse('assign users button is "{enabled_disabled}"'))
def assign_user_to_case(driver, enabled_disabled):
    if enabled_disabled == "enabled":
        assert "disabled" not in CaseListPage(driver).get_class_name_of_assign_users_button(), "assign users button is not enabled"
    elif enabled_disabled == "disabled":
        assert "disabled" in CaseListPage(driver).get_class_name_of_assign_users_button(), "assign users button is not disabled"
