from pytest_bdd import given, then, when, scenarios, parsers
from selenium.webdriver.common.by import By
from tests_common import functions

from ui_tests.exporter.pages.application_page import ApplicationPage
from ui_tests.exporter.pages.respond_to_ecju_query_page import RespondToEcjuQueryPage, DocumentGradingPage


scenarios("../features/ecju_queries.feature", strict_gherkin=False)


@when("I go to the recently created application with ecju query")
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


@given(parsers.parse('Caseworker creates an ECJU query with "{query}"'))
def caseworker_create_query(driver, query, api_test_client, context):
    api_test_client.ecju_queries.add_ecju_query(context.case_id, query=query)


@then("I see a notification next to ECJU queries")
def should_see_notification_ecju_queries(driver):
    assert ApplicationPage(driver).ecju_query_notification_count() == "1"


@then(parsers.parse('I see "{query}" as the query under open queries'))
def should_see_query_in_open_queries(driver, query):
    assert query in ApplicationPage(driver).get_open_queries_text()


@then(parsers.parse('I see "{response}" as the response under closed queries'))
def should_see_response_in_closed_queries(driver, response):
    assert response in ApplicationPage(driver).get_closed_queries_text()


@when(parsers.parse('I enter "{response}" for the response and click submit'))  # noqa
def respond_to_query(driver, response):  # noqa
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    driver.find_element(by=By.CSS_SELECTOR, value="button[value='submit']").click()
