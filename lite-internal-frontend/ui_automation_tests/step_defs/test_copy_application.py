from pytest_bdd import then, scenarios

from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/copied_application.feature", strict_gherkin=False)


@then("I can see the original application is linked")
def original_application_linked(driver, context):
    assert context.old_app_id in ApplicationPage(driver).get_case_copy_of_field_href()
