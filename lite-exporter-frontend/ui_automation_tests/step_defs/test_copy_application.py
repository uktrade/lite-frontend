from pytest_bdd import when, parsers, then, scenarios

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.generic_application.task_list import TaskListPage
from ui_automation_tests.shared import functions

scenarios("../features/copy_application.feature", strict_gherkin=False)


@when("I click copy application")
def click_on_an_application(driver):
    ApplicationPage(driver).click_copy_application()


@when(parsers.parse('I add a name "{name}", and select "{option}" to being referred with code "{code}"'))
def enter_details_of_copied_application(driver, context, name, option, code):
    ApplyForALicencePage(driver).enter_name_or_reference_for_application(name)
    functions.click_submit(driver)
    ApplyForALicencePage(driver).click_export_licence_yes_or_no(option)
    ApplyForALicencePage(driver).type_into_reference_number(code)
    context.name = name
    context.reference_code = code
    functions.click_submit(driver)


@then("I see my new name added")
def name_is_defined(driver, context):
    assert context.name in TaskListPage(driver).get_text_of_lite_task_list_items()


@then("I see the new reference code added")
def reference_code_added(driver, context):
    assert context.reference_code in TaskListPage(driver).get_text_of_lite_task_list_items()
