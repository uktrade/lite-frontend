from datetime import datetime

from pytest_bdd import scenarios, when, parsers, then

from pages.application_page import ApplicationPage
from pages.case_page import CasePage, CaseTabs

from ui_automation_tests.pages.case_list_page import CaseListPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared import functions

scenarios("../features/view_open_application.feature", strict_gherkin=False)


@when("I go to the activity tab")
def go_to_activity_tab(driver, internal_url, context):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)


@when(parsers.parse('filter user_type has been changed to "{user_type}"'))  # noqa
def filter_status_change(driver, user_type):  # noqa
    page = ApplicationPage(driver)
    page.select_filter_user_type_from_dropdown(user_type)


@then("exporter is at the first audit in the trail")  # noqa
def exporter_first_audit_in_trail(driver, exporter_info):  # noqa
    first_audit = Shared(driver).get_audit_trail_text()
    assert f"{exporter_info['first_name']}" in first_audit
    assert f"{exporter_info['last_name']}" in first_audit


@then("exporter is not in the audit trail")  # noqa
def exporter_is_not_in_audit_trail(driver, exporter_info):  # noqa
    audit = Shared(driver).get_audit_trail_text()
    assert f"{exporter_info['first_name']}" not in audit
    assert f"{exporter_info['last_name']}" not in audit


@when("I click set next review date button")
def i_click_next_review_date_button(driver):
    CasePage(driver).click_set_next_review_date()


@when("I enter a next review date")
def i_enter_a_next_review_date(driver, context):
    ApplicationPage(driver).set_next_review_date("01", "01", "2100", context)
    Shared(driver).click_submit()


@then("I see the review date has been set")
def i_see_the_next_review_date(driver, context):
    context.formatted_next_review_date = (
        datetime.strptime(context.next_review_date, "%Y-%m-%d").date().strftime("%d %B %Y")
    )

    assert CasePage(driver).get_next_review_date() == context.formatted_next_review_date


@then("review date is at the first audit in the trail")  # noqa
def exporter_first_audit_in_trail(driver, context):  # noqa
    first_audit = Shared(driver).get_audit_trail_text()
    assert context.formatted_next_review_date in first_audit


@then("I see previously hidden created application")  # noqa
def see_queue_in_queue_list(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.click_checkbox_to_show_team_ecju_query_and_hidden_cases()
    case_page.filter_by_case_reference(context.reference_code)
    case_page.click_apply_filters_button()
    assert driver.find_element_by_id(context.case_id).is_displayed()
