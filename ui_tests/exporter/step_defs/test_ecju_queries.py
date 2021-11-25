from exporter.ecju_queries.services import get_ecju_query_documents
from pytest_bdd import when, scenarios, then, parsers
from tests_common import functions

from ui_tests.exporter.pages.respond_to_ecju_query_page import RespondToEcjuQueryPage, DocumentGradingPage


scenarios("../features/ecju_queries.feature", strict_gherkin=False)


@when("I go to the recently created application with ECJU query")
def click_on_an_application(driver, exporter_url, context, apply_for_standard_application, add_an_ecju_query):
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id)


@when("I click on an CLC query previously created")
def click_on_clc_query(driver, exporter_url, context, add_goods_clc_query):
    driver.get(exporter_url.rstrip("/") + "/goods/" + context.goods_query_good_id)


@when("I confirm I can upload a document")
def confirm_can_upload_document(driver):
    # Confirm you have a document that is not sensitive
    DocumentGradingPage(driver).confirm_upload_document("yes")
    functions.click_submit(driver)


@when("I select that I cannot attach a document")
def select_cannot_attach_a_document(driver):
    DocumentGradingPage(driver).confirm_upload_document("no")


@when("I see ECJU helpline details")
def ecju_helpline(driver):
    assert DocumentGradingPage(driver).get_ecju_help()


@when("I select a valid missing document reason")
def select_missing_document_reason(driver):
    DocumentGradingPage(driver).select_valid_missing_document_reason()
    functions.click_submit(driver)


@when(parsers.parse('I see "{expected_count:d}" documents ready to be included in the response'))
def verify_upload_document_count(driver, expected_count):
    items = RespondToEcjuQueryPage(driver).get_uploaded_document_items()
    assert len(items) == expected_count


@when(parsers.parse('I delete document "{item_index:d}" from the response'))
def delete_uploaded_document_and_submit(driver, item_index):
    document = RespondToEcjuQueryPage(driver).get_uploaded_documents_delete_links()[item_index - 1]
    driver.execute_script("arguments[0].scrollIntoView();", document)
    driver.execute_script("arguments[0].click();", document)
    functions.click_submit(driver)
