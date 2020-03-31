from pytest_bdd import when, then, parsers, scenarios
import shared.tools.helpers as utils
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages
from pages.shared import Shared

scenarios("../features/queues.feature", strict_gherkin=False)


@when("I add a new queue called Review")  # noqa
def add_a_queue(driver, context, add_queue):  # noqa
    pass


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


@then("I see the new queue")
def see_queue_in_queue_list(driver, context):
    assert context.queue_name in Shared(driver).get_text_of_body()


@then("I see the edited queue")
def see_edited_queue_in_queue_list(driver, context):
    assert context.queue_name in Shared(driver).get_text_of_body()


@then("I dont see previously created application")
def dont_see_queue_in_queue_list(driver, context):
    driver.set_timeout_to(0)
    if len(driver.find_elements_by_css_selector(".lite-information-text__text")) != 1:
        assert context.app_id not in driver.find_element_by_css_selector(".govuk-table").text
        assert context.case_id not in driver.find_element_by_css_selector(".govuk-table").text
    driver.set_timeout_to_10_seconds()


@then(parsers.parse('I see "{num}" queue checkboxes selected'))
def see_number_of_checkboxes_selected(driver, context, num):
    ApplicationPage(driver).click_move_case_button()
    assert QueuesPages(driver).get_number_of_selected_queues() == int(num)


@then("queue change is in audit trail")
def queue_change_in_audit(driver, context):
    assert "moved the case to: " + context.queue_name in ApplicationPage(driver).get_text_of_audit_trail_item(0)
