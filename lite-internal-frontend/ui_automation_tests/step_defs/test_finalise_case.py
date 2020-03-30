from datetime import datetime

from pytest_bdd import scenarios, given, when, then, parsers

from conf.constants import DATE_FORMAT
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.documents_page import DocumentsPage
from ui_automation_tests.pages.generate_decision_documents_page import GeneratedDecisionDocuments
from ui_automation_tests.pages.give_advice_pages import GiveAdvicePages
from ui_automation_tests.shared.functions import click_submit

scenarios("../features/finalise_case.feature", strict_gherkin=False)


@given(parsers.parse('I "{decision}" all elements of the application at user and team level'))
def approve_application_objects(context, api_test_client, decision):
    context.advice_type = decision
    text = "abc"
    note = ""
    data = [
        {"type": context.advice_type, "text": text, "note": note, "end_user": context.end_user["id"]},
        {"type": context.advice_type, "text": text, "note": note, "consignee": context.consignee["id"]},
        {"type": context.advice_type, "text": text, "note": note, "good": context.good_id},
    ]

    api_test_client.cases.create_user_advice(context.case_id, data)
    api_test_client.cases.create_team_advice(context.case_id, data)


@given("A template exists for the appropriate decision")
def template_with_decision(context, api_test_client):
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, advice_type=[context.advice_type]
    )
    context.document_template_id = document_template["id"]
    context.document_template_name = document_template["name"]


@when("I go to the final advice page by url")
def final_advice_page(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/cases/" + context.case_id + "/final-advice-view/")


@when("I click continue on the licence page")
def continue_licence_page(driver, context):
    page = GiveAdvicePages(driver)
    context.licence_duration = page.get_duration_in_finalise_view()
    context.licence_start_date = datetime.now().strftime(DATE_FORMAT)
    click_submit(driver)


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
def licence_audit(driver, context):
    latest_audit = ApplicationPage(driver).get_text_of_audit_trail_item(0)
    assert context.licence_duration in latest_audit
    assert context.licence_start_date in latest_audit


@then("The case is finalised and a document is created in the audits")
def licence_audit(driver, context):
    case_page = ApplicationPage(driver)
    document_audit = case_page.get_text_of_audit_trail_item(0)
    assert context.document_template_name in document_audit
    status_audit = case_page.get_text_of_audit_trail_item(1)
    assert "finalised" in status_audit


@then("The generated decision document is visible")
def generated_decision_document(driver, context):
    documents_page = DocumentsPage(driver)
    assert context.document_template_name in documents_page.get_document_filename_at_position(0)
    assert documents_page.get_document_type_at_position(0) == "Generated"
