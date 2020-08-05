from pytest_bdd import scenarios, when, parsers, given, then

from ui_automation_tests.conftest import enter_type_of_application
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.generic_application.declaration import DeclarationPage
from ui_automation_tests.pages.ogel_pages import OgelPage
from ui_automation_tests.shared import functions

scenarios("../features/ogel.feature", strict_gherkin=False)


@given("an ogel licence has been added")  # noqa
def ogel_licence_created(apply_for_ogel):  # noqa
    pass


@when(parsers.parse('I search for an ogel application of type "{good_type}" for "{country}"'))  # noqa
def create_standard_application(driver, good_type, country, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "ogel", context)
    ogel = OgelPage(driver)
    ogel.enter_control_list_entry(good_type)
    ogel.enter_country(country)


@when("I select the created OGEL")
def select_created_ogel(driver, context):
    OgelPage(driver).select_created_ogel(context.ogel_id)


@when("I agree to the ogel declaration")
def ogel_declaration(driver):
    declaration = DeclarationPage(driver)
    declaration.agree_to_ogel_conditions()
    declaration.agree_to_ogel_export_conditions()
    functions.click_submit(driver)


@when("I go to the OGEL tab")
def go_to_ogel_tab(driver):
    OgelPage(driver).click_ogel_tab()


@then("I see my OGEL displayed")
def ogel_displayed(driver, context):
    ogel = OgelPage(driver)
    ogel.filter_by_name(context.ogel_name)
    assert context.ogel_name in ogel.get_text_of_ogel_accordion(), (
        context.ogel_name + " is not found in " + ogel.get_text_of_ogel_accordion()
    )
