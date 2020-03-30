from pytest_bdd import given, when, then, parsers, scenarios

from pages.queues_pages import QueuesPages
from shared.tools.helpers import get_formatted_date_time_m_d_h_s
from pages.shared import Shared

from shared.tools.wait import wait_until_page_is_loaded
from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios("../features/filter_and_sort_cases.feature", strict_gherkin=False)


@given("a queue has been created")
def create_queue(context, api_test_client):
    api_test_client.queues.add_queue("queue" + get_formatted_date_time_m_d_h_s())
    context.queue_name = api_test_client.context["queue_name"]


@given("case has been moved to new Queue")
def assign_case_to_queue(api_test_client):
    api_test_client.cases.assign_case_to_queue()


@when("case has been moved to new Queue")
def assign_case_to_queue_when(api_test_client):
    api_test_client.cases.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == Shared(driver).get_number_of_rows_in_lite_table(), "incorrect number of cases are shown"


@when("I click clear filters")
def i_show_filters(driver, context):
    CaseListPage(driver).click_clear_filters_button()


@when("I hide filters")
def i_hide_filters(driver, context):
    CaseListPage(driver).click_hide_filters_link()


@when("I sort cases by status")
def i_sort_cases_by(driver, context):
    wait_until_page_is_loaded(driver)
    CaseListPage(driver).sort_by_status()


@then(parsers.parse('the case at index "{index}" has the status of "{status}"'))
def the_cases_are_in_order_of(driver, index, status):
    assert status in Shared(driver).get_lite_row_text_by_index(index), status + " is not in the correct order"


@then("the filters are shown")
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible(), "filters are not shown"


@then("the filters are hidden")
def the_filters_are_hidden(driver, context):
    driver.set_timeout_to(0)
    assert not CaseListPage(driver).is_filters_visible(), "filters are shown"
    driver.set_timeout_to_10_seconds()


@then("there are no cases shown")  # noqa
def no_cases_shown(driver):
    assert (
        "No cases match your filters" in QueuesPages(driver).get_no_cases_text()
    ), "There are cases shown in the newly created queue."


@when(parsers.parse('filter case type has been changed to "{case_type}"'))  # noqa
def filter_status_change(driver, context, case_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(case_type)
    CaseListPage(driver).click_apply_filters_button()


@when("I click filter to show cases with open team ecju queries")  # noqa
def i_show_filters(driver, context):  # noqa
    CaseListPage(driver).click_checkbox_to_show_team_ecju_query()
    CaseListPage(driver).click_apply_filters_button()
