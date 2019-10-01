from pytest_bdd import given, when, then, parsers, scenarios
from helpers.helpers import get_formatted_date_time_m_d_h_s
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr, get_lite_client
from pages.shared import Shared

from helpers.wait import wait_until_page_is_loaded
from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios('../features/filter_and_sort_cases.feature', strict_gherkin=False)


@given('a queue has been created')
def create_queue(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.add_queue('queue' + get_formatted_date_time_m_d_h_s())
    context.queue_name = lite_client.context['queue_name']


@when('case has been moved to new Queue')
def assign_case_to_queue(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == Shared(driver).get_number_of_rows_in_lite_table(), "incorrect number of cases are shown"


@when(parsers.parse('filter status has been changed to "{status}"'))
def filter_status_change(driver, context, status):
    CaseListPage(driver).select_filter_status_from_dropdown(status)
    CaseListPage(driver).click_apply_filters_button()


@when(parsers.parse('filter case type has been changed to "{case_type}"'))
def filter_status_change(driver, context, case_type):
    CaseListPage(driver).select_filter_case_type_from_dropdown(case_type)
    CaseListPage(driver).click_apply_filters_button()


@when('I show filters')
def i_show_filters(driver, context):
    CaseListPage(driver).click_show_filters_link()


@when('I click clear filters')
def i_show_filters(driver, context):
    CaseListPage(driver).click_clear_filters_button()


@when('I hide filters')
def i_hide_filters(driver, context):
    CaseListPage(driver).click_hide_filters_link()


@when(parsers.parse('I sort cases by "{sort_type}"'))
def i_sort_cases_by(driver, context, sort_type):
    wait_until_page_is_loaded(driver)
    driver.find_element_by_link_text(sort_type).click()


@then(parsers.parse('the case at index "{index}" has the status of "{status}"'))
def the_cases_are_in_order_of(driver, index, status):
    assert status in Shared(driver).get_lite_row_text_by_index(index), status + " is not in the correct order"


@then('the filters are shown')
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible(), "filters are not shown"


@then('the filters are hidden')
def the_filters_are_hidden(driver, context):
    driver.set_timeout_to(0)
    assert not CaseListPage(driver).is_filters_visible(), "filters are shown"
    driver.set_timeout_to_10_seconds()
