from django.contrib.humanize.templatetags.humanize import intcomma
from pytest_bdd import (
    given,
    parsers,
    scenarios,
    then,
    when,
)

from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.pages.licence_page import LicencePage
from ui_tests.exporter.pages.licences_page import LicencesPage

scenarios("../features/licences.feature", strict_gherkin=False)


@when("I go to the licences page")
def licences_page(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/licences/")


@then("I see my standard licence")
def standard_licence_row(context, driver, assessed_control_list_entries):
    Shared(driver).filter_by_reference_number(context.reference_code)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert ", ".join(assessed_control_list_entries) in row
    assert context.goods[0]["good"]["name"] in row
    assert context.end_user["country"]["name"] in row
    assert context.end_user["name"] in row
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
def standard_licence_details(driver, context, assessed_control_list_entries):
    page = LicencePage(driver)
    assert context.end_user["country"]["name"] in page.get_destination()
    assert context.end_user["name"] in page.get_end_user()
    good_row = page.get_good_row()
    assert ", ".join(assessed_control_list_entries) in good_row
    formatted_licenced_quantity = intcomma(context.goods[0]["quantity"]).split(".")[0]
    formatted_licenced_value = intcomma(float(context.goods[0]["value"]) * context.goods[0]["quantity"]).split(".")[0]
    assert formatted_licenced_quantity in good_row
    assert formatted_licenced_value in good_row
    assert "0" in page.get_usage()


@given(parsers.parse('I assess the goods with "{cle_entries}"'), target_fixture="assessed_control_list_entries")
def assess_goods(api_test_client, cle_entries):
    cle_entries = [cle.strip() for cle in cle_entries.split(",")]
    api_test_client.goods.update_good_clc(
        good_id=api_test_client.context["good_id"],
        good_on_application_id=api_test_client.context["good_on_application_id"],
        case_id=api_test_client.context["case_id"],
        control_list_entries=cle_entries,
        is_good_controlled=True,
        report_summary="ARS",
    )
    return cle_entries
