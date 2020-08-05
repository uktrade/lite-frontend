from pytest_bdd import when, then, parsers, scenarios

from pages.queues_pages import QueuesPages
from pages.shared import Shared
from shared import functions
from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios("../features/filter_cases.feature", strict_gherkin=False)


@when("case has been moved to new Queue")
def assign_case_to_queue_when(api_test_client):
    api_test_client.cases.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == Shared(driver).get_number_of_rows_in_lite_table(), "incorrect number of cases are shown"


@when("I hide filters")
def i_hide_filters(driver, context):
    CaseListPage(driver).click_hide_filters_link()


@then("the filters are shown")
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible(), "filters are not shown"


@then("there are no cases shown")  # noqa
def no_cases_shown(driver):
    assert QueuesPages(driver).is_no_cases_notice_displayed(), "There are cases shown in the newly created queue."


@when(parsers.parse('filter case type has been changed to "{case_type}"'))  # noqa
def filter_status_change(driver, context, case_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(case_type)
    functions.click_apply_filters(driver)


@when("I click filter to show cases with open team ecju queries")  # noqa
def filter_by_ecju(driver, context):  # noqa
    CaseListPage(driver).click_checkbox_to_show_team_ecju_query_and_hidden_cases()
    functions.click_apply_filters(driver)


@when("I click advanced filters")
def i_show_advanced_filters(driver, context):
    CaseListPage(driver).click_advanced_filters_button()


@then("I can see all advanced filters")
def i_can_see_all_advanced_filters(driver, context):
    CaseListPage(driver).assert_all_advanced_filters_available()


@when("I filter by case reference")
def i_filter_by_case_reference(driver, context):
    CaseListPage(driver).filter_by_exporter_application_reference(context.app_name)


@when("I filter by goods related description")
def i_filter_by_goods_related_description(driver, context):
    CaseListPage(driver).filter_by_goods_related_description(context.goods_type["description"])


@when("I filter by organisation name")
def i_filter_by_goods_related_description(driver, context):
    CaseListPage(driver).filter_by_organisation_name(context.org_name)


@when(parsers.parse('filter status has been changed to "{status}"'))  # noqa
def filter_status_change(driver, context, status):  # noqa
    CaseListPage(driver).select_filter_status_from_dropdown(status)
    functions.click_apply_filters(driver)
