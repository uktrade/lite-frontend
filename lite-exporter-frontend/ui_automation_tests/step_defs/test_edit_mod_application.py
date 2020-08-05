from pytest_bdd import scenarios, given, when

from ui_automation_tests.pages.f680_additional_information_page import F680AdditionalInformationPage
from ui_automation_tests.shared import functions

scenarios("../features/edit_mod_application.feature", strict_gherkin=False)


@given("I create a exhibition clearance application via api")  # noqa
def exhibition_clearance_exists(apply_for_exhibition_clearance):  # noqa
    pass


@given("I create a F680 clearance application via api")  # noqa
def f680_clearance_exists(apply_for_f680_clearance):  # noqa
    pass


@given("I create a gifting clearance application via api")  # noqa
def gifting_clearance_exists(apply_for_gifting_clearance):  # noqa
    pass


@when("I edit additional information")
def add_new_additional_information(driver, context):  # noqa
    page = F680AdditionalInformationPage(driver, "return")
    page.click_expedited()
    page.enter_no_date()
    page.click_foreign_technology()
    page.enter_foreign_technology()
    page.click_locally_manufactured()
    page.enter_locally_manufactured()
    page.click_mtcr_type()
    page.enter_mtcr_type()
    page.click_electronic_warfare_requirement()
    page.enter_electronic_warfare_requirement()
    page.click_uk_service_equipment()
    page.enter_uk_service_equipment()
    page.click_uk_service_equipment_type()
    page.enter_uk_service_equipment_type()
    functions.click_submit(driver, button_value="finish")
