from pytest_bdd import scenarios, given, when, then

from ui_automation_tests.pages.hub_page import Hub
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared.tools import helpers
from ui_automation_tests.shared.tools.utils import get_lite_client

scenarios("../features/notifications.feature", strict_gherkin=False)


@given("an application exists and a case note has been added via internal gov site")
def application_exists_case_note_added(apply_for_standard_application, api_client_config, context, driver):
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    lite_client.ecju_queries.add_ecju_query(context.case_id)
    lite_client.cases.add_case_note(context, context.case_id)
    context.number_of_notifications = Hub(driver).return_number_of_notifications()


@then("I can see a notification in application tile")
def notification_exists(driver, context):
    # Creating an application creates an ecju-query attached to it,
    # and we add a case_note, should expect 2 new notifications
    assert "You have" in Hub(driver).get_text_of_application_tile()
    context.number_of_notifications = Hub(driver).return_number_of_notifications()


@when("I click on my application")
def click_on_application(driver, context):
    elements = Shared(driver).get_gov_table_cell_links()
    no = helpers.get_element_index_by_text(elements, context.app_time_id, complete_match=False)
    elements[no].click()


@then("I see a notification on application list")
def notification_on_application_list(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = helpers.get_element_index_by_text(elements, context.app_time_id, complete_match=False)
    assert elements[no].find_element_by_css_selector(Shared(driver).NOTIFICATION).is_displayed()


@then("I can see the internally added note")
def internal_note_visible(driver, context):
    assert context.case_note_text in driver.find_element_by_css_selector(".lite-case-notes").text


@then("I cannot see a notification")
def notification_does_not_exist(driver, context):
    if context.number_of_notifications != 1:
        number_of_notifications_after_acknowledgment = Hub(driver).return_number_of_notifications()
        assert number_of_notifications_after_acknowledgment + 1 == context.number_of_notifications
