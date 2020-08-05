from datetime import datetime, date

from pytest_bdd import scenarios, when, then, parsers

from conf.constants import DATE_FORMAT
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.documents_page import DocumentsPage
from ui_automation_tests.pages.generate_decision_documents_page import GeneratedDecisionDocuments
from ui_automation_tests.pages.good_country_matrix_page import GoodCountryMatrixPage
from ui_automation_tests.pages.grant_licence_page import GrantLicencePage

scenarios("../features/finalise_case.feature", strict_gherkin=False)


@then("I see the final advice documents page")
def final_advice_documents_page(driver, context):
    assert GeneratedDecisionDocuments(driver).decision_row_exists(context.advice_type)


@then(parsers.parse('The decision row status is "{status}"'))
def decision_row_status(driver, context, status):
    assert GeneratedDecisionDocuments(driver).get_section_status(context.advice_type) == status


@then("The case is finalised and a document is created in the audits")
def licence_audit(driver, context, internal_url):
    case_page = ApplicationPage(driver)
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    finalised_audit = case_page.get_text_of_audit_trail_item(0)
    assert "finalised" in finalised_audit
    document_audit = case_page.get_text_of_audit_trail_item(1)
    assert context.document_template_name in document_audit


@then("The generated decision document is visible")
def generated_decision_document(driver, context):
    documents_page = DocumentsPage(driver)
    assert context.document_template_name in documents_page.get_document_filename_at_position(0)
    assert "Generated" in documents_page.get_document_type_at_position(0)


@then("I see the applied for goods details on the licence page")
def applied_for_goods_details(driver, context):
    page = GrantLicencePage(driver)
    good_on_app_id = context.goods[0]["id"]
    assert context.goods[0]["quantity"] == float(page.get_good_quantity(good_on_app_id))
    assert round(float(context.goods[0]["value"]) * context.goods[0]["quantity"], 2) == float(
        page.get_good_value(good_on_app_id)
    )
    date_in_form = GrantLicencePage(driver).get_date_in_date_entry()
    today = date.today()
    assert today.day == int(date_in_form["day"])
    assert today.month == int(date_in_form["month"])
    assert today.year == int(date_in_form["year"])
    context.licence_duration = page.get_duration_in_finalise_view()
    context.licence_start_date = datetime.now().strftime(DATE_FORMAT)


@when("I go to the team advice page by url")  # noqa
def final_advice_page(driver, context, internal_url):  # noqa
    driver.get(
        internal_url.rstrip("/")
        + "/queues/00000000-0000-0000-0000-000000000001/cases/"
        + context.case_id
        + "/team-advice/"
    )


@then("I see the good country combination")
def approvable_good_country_combination(driver, context):
    row = GoodCountryMatrixPage(driver).get_enabled_good_country_decision_row(context.goods_type["id"])
    assert context.goods_type["description"] in row
    assert context.goods_type["control_list_entries"][0]["rating"] in row
    assert context.country["name"] in row


@then("I see the refused good country combination")
def refused_good_country_combination(driver, context):
    row = GoodCountryMatrixPage(driver).get_refused_good_country_decision_row(context.goods_type["id"])
    assert context.goods_type["description"] in row
    assert context.goods_type["control_list_entries"][0]["rating"] in row
    assert context.country["name"] in row
