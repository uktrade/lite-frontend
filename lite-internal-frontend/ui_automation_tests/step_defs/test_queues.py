from pytest_bdd import when, then, parsers, scenarios, given
import shared.tools.helpers as utils
from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from pages.queues_pages import QueuesPages
from pages.shared import Shared


scenarios("../features/queues.feature", strict_gherkin=False)


@when("I go to the countersigning queue")
def go_to_countersigning_queue(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/queues/" + context.countersigning_queue_id)


@when("I edit the new queue")
def click_on_edit_queue(driver, context):
    queues = QueuesPages(driver)
    no = utils.get_element_index_by_text(
        Shared(driver).get_rows_in_lite_table(), context.queue_name, complete_match=False
    )
    queues.click_queue_edit_button(no)
    context.queue_name = str(context.queue_name)[:12] + "edited"
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()


@when("I edit the new queue with a countersigning queue")
def edit_queue_with_countersigning(driver, context):
    queues = QueuesPages(driver)
    no = utils.get_element_index_by_text(
        Shared(driver).get_rows_in_lite_table(), context.queue_name, complete_match=False
    )
    queues.click_queue_edit_button(no)
    QueuesPages(driver).select_countersigning_queue(context.countersigning_queue_name)
    Shared(driver).click_submit()


@then("I see my queue")
def see_queue_in_queue_list(driver, context):
    Shared(driver).filter_by_name(context.queue_name)
    assert context.queue_name in QueuesPages(driver).get_row_text(context.queue_name)


@then("I see my queue in the list with a countersigning queue")
def see_queue_in_queue_list_with_countersigning_queue(driver, context):
    Shared(driver).filter_by_name(context.queue_name)
    row = QueuesPages(driver).get_row_text(context.queue_name)
    assert context.countersigning_queue_name in row
    assert context.countersigning_queue_name in row


@then("I dont see previously created application")
def dont_see_queue_in_queue_list(driver, context):
    driver.set_timeout_to(0)
    if len(driver.find_elements_by_css_selector(".lite-information-text__text")) != 1:
        assert context.app_id not in driver.find_element_by_css_selector(".govuk-table").text
        assert context.case_id not in driver.find_element_by_css_selector(".govuk-table").text
    driver.set_timeout_to_10_seconds()


@then(parsers.parse('I see at least "{num}" queue checkboxes selected'))
def see_number_of_checkboxes_selected(driver, context, num):
    ApplicationPage(driver).click_move_case_button()
    # May be more queues due to case routing automation
    assert int(QueuesPages(driver).get_number_of_selected_queues()) >= int(num)


@then("queue change is in audit trail")
def queue_change_in_audit(driver, context, internal_url):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)

    assert "moved the case to " + context.queue_name in Shared(driver).get_audit_trail_text()


@when("I go to application previously created for my queue")
def go_to_case_for_queue(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/queues/" + context.queue_id + "/cases/" + context.case_id)


@when(parsers.parse('I click on the "{queue_name}" queue in dropdown'))  # noqa
def system_queue_shown_in_dropdown(driver, queue_name):  # noqa
    CaseListPage(driver).click_on_queue_name(queue_name)


@given("a new countersigning queue has been created")  # noqa
def create_countersigning_queue(context, api_test_client):  # noqa
    api_test_client.queues.add_queue("countersigningqueue" + utils.get_formatted_date_time_y_m_d_h_s())
    context.countersigning_queue_name = api_test_client.context["queue_name"]
    context.countersigning_queue_id = api_test_client.context["queue_id"]
