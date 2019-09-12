from pytest_bdd import scenarios, given, when, then

from pages.hub_page import Hub
from pages.shared import Shared
from ui_automation_tests.helpers import helpers

scenarios('../features/notifications.feature', strict_gherkin=False)


@given('an application exists and a case note has been added via internal gov site')
def application_exists_case_note_added(driver, add_an_application, internal_case_note, context):
    context.number_of_notifications = Hub(driver).return_number_of_notifications()


@then('I can see a notification in application tile')
def notification_exists(driver, context):
    # Creating an application creates an ecju-query attached to it, and we add a case_note, should expect 2 new notifications
    assert "You have " + str(context.number_of_notifications + 2) in Hub(driver).get_text_of_application_tile()
    context.number_of_notifications = Hub(driver).return_number_of_notifications()


@when('I click on my application')
def click_on_application(driver, context):
    elements = Shared(driver).get_gov_table_cell_links()
    no = helpers.get_element_index_by_text(elements, context.app_id)
    elements[no].click()


@then('I see a notification on application list')
def notification_on_application_list(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = helpers.get_element_index_by_partial_text(elements, context.app_name)
    assert "New notification" in elements[no].text


@then('I can see the internally added note')
def internal_note_visible(driver, context):
    assert context.text in driver.find_element_by_css_selector('.lite-case-notes').text


@then('I cannot see a notification')
def notification_does_not_exist(driver, context):
    if context.number_of_notifications != 1:
        number_of_notifications_after_acknowledgment = Hub(driver).return_number_of_notifications()
        assert number_of_notifications_after_acknowledgment+1 == context.number_of_notifications
