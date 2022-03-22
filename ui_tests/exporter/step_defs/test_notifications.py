from pytest_bdd import scenarios, given, then, parsers

from ui_tests.exporter.pages.hub_page import Hub
from ui_tests.exporter.pages.shared import Shared
from tests_common.tools import helpers

scenarios("../features/notifications.feature", strict_gherkin=False)


@given("an application exists a case note and an ecju query have been added via internal gov site")
def application_exists_case_note_added(apply_for_open_application, api_test_client, context, driver):
    api_test_client.ecju_queries.add_ecju_query(context.case_id)
    api_test_client.cases.add_case_note(context, context.case_id)


@then(parsers.parse('I see "{num}" notifications on application list'))
def notification_on_application_list(driver, context, num):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = helpers.get_element_index_by_text(elements, context.app_name, complete_match=False)
    assert num in elements[no].find_element_by_css_selector(Shared(driver).NOTIFICATION).text


@then("I can see the internally added note")
def internal_note_visible(driver, context):
    assert context.case_note_text in driver.find_element_by_css_selector(".lite-case-notes").text


@then("I cannot see a notification")
def notification_does_not_exist(driver, context):
    if context.number_of_notifications != 1:
        number_of_notifications_after_acknowledgment = Hub(driver).return_number_of_notifications()
        assert number_of_notifications_after_acknowledgment + 1 == context.number_of_notifications
