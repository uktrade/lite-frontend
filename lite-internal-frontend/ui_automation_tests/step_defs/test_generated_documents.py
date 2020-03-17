from pytest_bdd import scenarios, when, given, then, parsers

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


@when("I add a paragraph to the document")
def add_paragraph(driver, context):
    generated_document_page = GeneratedDocument(driver)
    generated_document_page.click_add_paragraphs_link()
    new_paragraph = generated_document_page.select_and_return_first_checkbox_value()
    context.document_template_paragraph_text.append(new_paragraph)
    Shared(driver).click_submit()


@when(parsers.parse('I add my custom text "{custom_text}"'))
def add_custom_text(driver, context, custom_text):
    GeneratedDocument(driver).add_text_to_edit_text(custom_text)


@when("I click regenerate")
def click_regenerate(driver, context):
    GeneratedDocument(driver).click_regenerate_btn()


@then("I see the template text to edit")
def template_text(driver, context):
    text = GeneratedDocument(driver).get_document_text_in_edit_text_area()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in text
        # Remove matched strings to ensure the same string isn't matched twice
        text = text.replace(paragraph, "", 1)


@then("I see the generated document preview")
def generated_document_preview(driver, context):
    generated_document_page = GeneratedDocument(driver)
    assert generated_document_page.preview_is_shown()
    paragraphs = generated_document_page.get_document_text_in_preview()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in paragraphs
        # Remove matched strings to ensure the same string isn't matched twice
        paragraphs = paragraphs.replace(paragraph, "", 1)


@then("I see my generated document")
def generated_document(driver, context):
    most_recent_doc = Shared(driver).get_first_row_of_gov_uk_table()
    row_text = most_recent_doc.text
    # Check document name
    assert context.document_template_name in row_text
    assert "Generated" in row_text
    # Check download link is present
    assert GeneratedDocument(driver).check_download_link_is_present(most_recent_doc)


@then("I see both my generated documents")
def both_generated_documents(driver, context):
    document_rows = Shared(driver).get_rows_in_lite_table()
    for document_row in document_rows:
        row_text = document_row.text
        assert context.document_template_name in row_text
        assert "Generated" in row_text
        assert GeneratedDocument(driver).check_download_link_is_present(document_row)
    # Check 2 documents have been created
    assert document_rows[0].text != document_rows[1].text
