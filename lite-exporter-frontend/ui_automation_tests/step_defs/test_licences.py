from django.contrib.humanize.templatetags.humanize import intcomma
from pytest_bdd import scenarios, given, when, then

from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.licence_page import LicencePage
from ui_automation_tests.pages.licences_page import LicencesPage

scenarios("../features/licences.feature", strict_gherkin=False)


@when("I go to the licences page")
def licences_page(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/licences/")


@then("I see my standard licence")
def standard_licence_row(context, driver):
    Shared(driver).filter_by_reference_number(context.reference_code)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert ", ".join(x["rating"] for x in context.goods[0]["good"]["control_list_entries"]) in row
    assert context.goods[0]["good"]["description"] in row
    assert context.end_user["country"]["name"] in row
    assert context.end_user["name"] in row
    assert "Issued" in row


@then("I see my open licence")
def open_licence_row(context, driver):
    Shared(driver).filter_by_reference_number(context.reference_code)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert ", ".join(x["rating"] for x in context.goods_type["control_list_entries"]) in row
    assert context.goods_type["description"] in row
    assert context.country["name"] in row
    assert "Issued" in row


@when("I click on the clearances tab")
def clearances_tab(driver):
    LicencesPage(driver).click_clearances_tab()


@when("I click on the NLR tab")
def nlrs_tab(driver):
    LicencesPage(driver).click_nlr_tab()


@then("I see my nlr document")
def nlr_document_visible(context, driver):
    Shared(driver).filter_by_reference_number(context.reference_code)
    row = LicencesPage(driver).licence_row_properties(context.generated_document)
    assert context.reference_code in row


@then("I see my exhibition licence")
def exhibition_licence_row(context, driver):
    Shared(driver).filter_by_reference_number(context.reference_code)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert ", ".join(x["rating"] for x in context.goods[0]["good"]["control_list_entries"]) in row
    assert context.goods[0]["good"]["description"] in row
    assert "Issued" in row


@when("I view my licence")
def view_licence(driver, context):
    LicencesPage(driver).click_licence(context.licence)


@then("I see all the typical licence details")
def licence_details(driver, context):
    page = LicencePage(driver)
    assert context.reference_code in page.get_heading_text()
    assert page.is_licence_document_present()


@then("I see my standard application licence details")
def standard_licence_details(driver, context):
    page = LicencePage(driver)
    assert context.end_user["country"]["name"] in page.get_destination()
    assert context.end_user["name"] in page.get_end_user()
    good_row = page.get_good_row()
    assert ", ".join(x["rating"] for x in context.goods[0]["good"]["control_list_entries"]) in good_row
    formatted_licenced_quantity = intcomma(context.goods[0]["quantity"]).split(".")[0]
    formatted_licenced_value = intcomma(float(context.goods[0]["value"]) * context.goods[0]["quantity"]).split(".")[0]
    assert formatted_licenced_quantity in good_row
    assert formatted_licenced_value in good_row
    assert "0" in page.get_usage()


@then("I see my open application licence details")
def open_licence_details(driver, context):
    page = LicencePage(driver)
    assert context.country["name"] in page.get_destination()
    good_row = page.get_good_row()
    assert ", ".join(x["rating"] for x in context.goods_type["control_list_entries"]) in good_row
    assert "0" in page.get_usage()


@then("I see my exhibition application licence details")
def exhibition_licence_details(driver, context):
    assert (
        ", ".join(x["rating"] for x in context.goods[0]["good"]["control_list_entries"])
        in LicencePage(driver).get_good_row()
    )


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):  # noqa
    pass
