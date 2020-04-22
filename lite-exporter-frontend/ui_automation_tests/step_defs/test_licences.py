from django.contrib.humanize.templatetags.humanize import intcomma
from pytest_bdd import scenarios, given, parsers, when, then

from ui_automation_tests.pages.licence_page import LicencePage
from ui_automation_tests.pages.licences_page import LicencesPage
from ui_automation_tests.shared.tools.helpers import find_paginated_item_by_id

scenarios("../features/licences.feature", strict_gherkin=False)


@given(parsers.parse('I create "{decision}" final advice for open application'))
def final_advice_open(context, decision, api_test_client):
    api_test_client.cases.create_final_advice(
        context.case_id, [{"type": decision, "text": "abc", "note": "", "goods_type": context.goods_type["id"]}]
    )


@when("I go to the licences page")
def licences_page(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/licences/")


@then("I see my standard licence")
def standard_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.goods[0]["good"]["control_code"] in row
    assert context.goods[0]["good"]["description"] in row
    assert context.end_user["country"]["name"] in row
    assert context.end_user["name"] in row
    assert "Finalised" in row


@then("I see my open licence")
def open_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.goods_type["control_code"] in row
    assert context.goods_type["description"] in row
    assert context.country["name"] in row
    assert "Finalised" in row


@when("I click on the clearances tab")
def clearances_tab(driver):
    LicencesPage(driver).click_clearances_tab()


@then("I see my exhibition licence")
def exhibition_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.goods[0]["good"]["control_code"] in row
    assert context.goods[0]["good"]["description"] in row
    assert "Finalised" in row


@when("I click on the nlr tab")
def nlr_tab(driver):
    LicencesPage(driver).click_nlr_tab()


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
    assert context.goods[0]["good"]["control_code"] in good_row
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
    assert context.goods_type["control_code"] in good_row
    assert "0" in page.get_usage()


@then("I see my exhibition application licence details")
def exhibition_licence_details(driver, context):
    assert context.goods[0]["good"]["control_code"] in LicencePage(driver).get_good_row()
