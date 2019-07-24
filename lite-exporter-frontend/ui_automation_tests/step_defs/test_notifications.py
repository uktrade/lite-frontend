from pytest_bdd import scenarios, given, when, then
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.helpers import helpers
from conftest import context
import helpers.helpers as utils
from selenium.webdriver.common.by import By

scenarios('../features/notifications.feature', strict_gherkin=False)


@given('An application exists and a case note has been added via internal gov site')
def application_exists_case_note_added(set_up_application_before_hook, create_note_visible_to_exporter):

    # all work done by fixtures
    assert True


@when('I can see a notification')
def notification_exists(driver):
    exporter_hub_page = ExporterHubPage(driver)
    exporter_hub_page.check_for_notification()


@when('I click on my application')
def click_on_application(driver):
    exporter_hub_page = ExporterHubPage(driver)
    exporter_hub_page.click_applications()
    elements = driver.find_elements_by_css_selector(".govuk-table__cell a")
    app_num = helpers.get_element_index_by_text(elements, context.app_id)
    elements[app_num].click()


@then('I can see the internally added note')
def internal_note_visible(driver):
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.text + "')]]")


@then('I cannot see a notification')
def notification_does_not_exist(driver):
    exporter_hub_page = ExporterHubPage(driver)
    exporter_hub_page.check_for_no_notification()
