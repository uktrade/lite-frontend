from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.support.ui import Select
from helpers.helpers import get_formatted_date_time_m_d_h_s
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr

from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios('../features/filter_and_sort_cases.feature', strict_gherkin=False)


@given('a queue has been created')
def create_queue(register_organisation, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.add_queue('queue' + get_formatted_date_time_m_d_h_s())
    context.queue_name = api.context['queue_name']


@when('case has been moved to new Queue')
def assign_case_to_queue(context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == len(driver.find_elements_by_css_selector('.lite-cases-table .lite-cases-table-row'))


@when(parsers.parse('filter status has been changed to "{status}"'))
def filter_status_change(driver, context, status):
    select = Select(driver.find_element_by_id('status'))
    select.select_by_visible_text(status)
    CaseListPage(driver).click_apply_filters_button()


@when(parsers.parse('filter case type has been changed to "{case_type}"'))
def filter_status_change(driver, context, case_type):
    select = Select(driver.find_element_by_id('case_type'))
    select.select_by_visible_text(case_type)
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
    driver.find_element_by_link_text(sort_type).click()


@then(parsers.parse('the case at index "{index}" has the status of "{status}"'))
def the_cases_are_in_order_of(driver, context, index, status):
    row = driver.find_elements_by_css_selector('.lite-cases-table-row')[int(index)]
    assert status in row.text


@then('the filters are shown')
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible()


@then('the filters are hidden')
def the_filters_are_hidden(driver, context):
    assert not CaseListPage(driver).is_filters_visible()
