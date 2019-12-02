from pytest_bdd import scenarios, when, given, then

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.generate_document_page import GeneratedDocument
from ui_automation_tests.pages.shared import Shared

scenarios("../features/generated_documents.feature", strict_gherkin=False)


@given("I create a template")
def create_template(add_a_document_template):
    pass


@when("I click on the Generate document button")
def click_generated_documents(driver, context):
    ApplicationPage(driver).click_generate_document_button()


@when("I select the template previously created")
def selected_created_template(driver, context):
    GeneratedDocument(driver).click_letter_template(context.document_template_id)
    Shared(driver).click_submit()


@then("I see the generated document preview")
def generated_document_preview(driver, context):
    generated_document_page = GeneratedDocument(driver)
    assert generated_document_page.preview_is_shown()
    paragraphs = generated_document_page.get_document_text()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in paragraphs


@then("I see my generated document")
def generated_document(driver, context):
    most_recent_doc = Shared(driver).get_first_row_of_gov_uk_table()
    row_text = most_recent_doc.text
    # Check document name
    assert context.document_template_name in row_text
    assert "Generated" in row_text
    # Check download link is present
    assert GeneratedDocument(driver).check_download_link_is_present(most_recent_doc)
