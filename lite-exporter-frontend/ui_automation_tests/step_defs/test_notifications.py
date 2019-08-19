from pytest_bdd import scenarios, given, when, then
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.helpers import helpers

scenarios('../features/notifications.feature', strict_gherkin=False)


@given('An application exists and a case note has been added via internal gov site')
def application_exists_case_note_added(add_an_application, internal_case_note):
    pass


@then('I can see a notification in application tile')
def notification_exists(driver, context):
    exporter_hub_page = ExporterHubPage(driver)
    context.number_of_notifications = exporter_hub_page.return_number_of_notifications()
    assert "You have " in driver.find_element_by_css_selector('.lite-tiles [href="/applications/"] p').text


@when('I click on my application')
def click_on_application(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__cell a")
    app_id = helpers.get_element_index_by_text(elements, context.app_id)
    elements[app_id].click()


@then('I see a notification on application list')
def notification_on_application_list(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    app_id = helpers.get_element_index_by_partial_text(elements, context.app_id)
    assert "New notification" in elements[app_id].text


@then('I can see the internally added note')
def internal_note_visible(driver, context):
    assert context.text in driver.find_element_by_css_selector('.lite-case-notes').text


@then('I cannot see a notification')
def notification_does_not_exist(driver, context):
    exporter_hub_page = ExporterHubPage(driver)
    if context.number_of_notifications != 1:
        number_of_notifications_after_acknowledgment = exporter_hub_page.return_number_of_notifications()
        assert number_of_notifications_after_acknowledgment+1 == context.number_of_notifications
