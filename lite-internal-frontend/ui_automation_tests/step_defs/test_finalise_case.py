from datetime import datetime

from pytest_bdd import scenarios, when, then, parsers

from conf.constants import DATE_FORMAT
from pages.case_page import CasePage, CaseTabs
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.documents_page import DocumentsPage
from ui_automation_tests.pages.generate_decision_documents_page import GeneratedDecisionDocuments
from ui_automation_tests.pages.grant_licence_page import GrantLicencePage

scenarios("../features/finalise_case.feature", strict_gherkin=False)


@then("I see the final advice documents page")
def final_advice_documents_page(driver, context):
    assert GeneratedDecisionDocuments(driver).decision_row_exists(context.advice_type)


@when("I generate a document for the decision")
def generate_document(driver, context):
    GeneratedDecisionDocuments(driver).click_generate_decision_document(context.advice_type)


@then(parsers.parse('The decision row status is "{status}"'))
def decision_row_status(driver, context, status):
    assert GeneratedDecisionDocuments(driver).get_section_status(context.advice_type) == status


@then("The licence information is in the latest audit")
def licence_audit(driver, context, internal_url):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    latest_audit = ApplicationPage(driver).get_text_of_audit_trail_item(0)
    assert context.licence_duration in latest_audit
    assert context.licence_start_date in latest_audit


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
    context.licence_duration = page.get_duration_in_finalise_view()
    context.licence_start_date = datetime.now().strftime(DATE_FORMAT)
