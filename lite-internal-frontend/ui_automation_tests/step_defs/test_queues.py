from pytest_bdd import given, when, then, parsers, scenarios
import helpers.helpers as utils
from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from pages.header_page import HeaderPage
from pages.queues_pages import QueuesPages
from pages.shared import Shared

scenarios('../features/queues.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@given('I go to queues')
def go_to_queues(driver, sign_in_to_internal_sso, internal_url):
    driver.get(internal_url.rstrip('/') + '/queues/')


@when('I go to queues via menu')
def go_to_queues_via_menu(driver):
    HeaderPage(driver).click_lite_menu()
    HeaderPage(driver).click_queues()


@when('I edit the new queue')
def click_on_edit_queue(driver, context):
    queues = QueuesPages(driver)
    no = utils.get_element_index_by_partial_text(Shared(driver).get_rows_in_lite_table(), context.queue_name)
    queues.click_queue_edit_button(no)
    context.queue_name = str(context.queue_name)[:12] + "edited"
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()


@when(parsers.parse('I enter in queue name "{queue_name}"'))
def add_a_queue(driver, queue_name):
    QueuesPages(driver).click_add_a_queue_button()
    QueuesPages(driver).enter_queue_name(queue_name)
    Shared(driver).click_submit()


@when('I enter in queue name Review')
def add_a_queue(driver, context, add_queue):
    pass


@then('I see the new queue')
def see_queue_in_queue_list(driver, context):
    assert context.queue_name in Shared(driver).get_text_of_body()


@then('I see previously created application')
def see_queue_in_queue_list(driver, context):
    assert QueuesPages(driver).is_case_on_the_list(context.case_id) == 1, "previously created application is not displayed " + context.case_id


@then('I dont see previously created application')
def dont_see_queue_in_queue_list(driver, context):
    driver.set_timeout_to(0)
    if len(driver.find_elements_by_css_selector('.lite-information-text__text')) != 1:
        assert context.app_id not in driver.find_element_by_css_selector('.lite-cases-table').text
        assert context.case_id not in driver.find_element_by_css_selector('.lite-cases-table').text
    driver.set_timeout_to_10_seconds()


@then('I dont see previously created clc query')
def dont_see_queue_in_queue_list(driver, context):
    driver.set_timeout_to(0)
    if len(driver.find_elements_by_css_selector('.lite-information-text__text')) == 1:
        assert True
    else:
        assert context.case_id not in driver.find_element_by_css_selector('.lite-cases-table').text
    driver.set_timeout_to_10_seconds()


@when('I add case to newly created queue')
def move_case_to_new_queue(driver, context):
    ApplicationPage(driver).click_move_case_button()
    driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()


@then(parsers.parse('I see "{num}" queue checkboxes selected'))
def see_number_of_checkboxes_selected(driver, context, num):
    ApplicationPage(driver).click_move_case_button()
    assert QueuesPages(driver).get_size_of_selected_queues() == int(num)
    Shared(driver).click_back_link()


@when('I remove case from new cases queue')
def move_case_to_new_queue(driver, context):
    ApplicationPage(driver).click_move_case_button()
    QueuesPages(driver).click_on_new_cases_queue()
    Shared(driver).click_submit()


@when('I deselect all queues')
def deselect_all_queues(driver):
    ApplicationPage(driver).click_move_case_button()
    QueuesPages(driver).deselect_all_queues()
    Shared(driver).click_submit()


@when('I move case to new cases original queue and remove from new queue')
def move_case_to_original_queue(driver, context):
    ApplicationPage(driver).click_move_case_button()
    driver.find_element_by_id(context.queue_name).click()
    QueuesPages(driver).click_on_new_cases_queue()
    Shared(driver).click_submit()
