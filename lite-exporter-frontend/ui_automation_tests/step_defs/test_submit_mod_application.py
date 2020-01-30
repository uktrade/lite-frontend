from pytest_bdd import scenarios, when, parsers

from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.shared import functions

scenarios("../features/submit_mod_application.feature", strict_gherkin=False)


@when(parsers.parse('I select a MOD licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ApplyForALicencePage(driver).select_mod_application_type(type)
    functions.click_submit(driver)
