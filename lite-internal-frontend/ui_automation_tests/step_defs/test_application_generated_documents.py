from pytest_bdd import scenarios, when, given, then, parsers

from pages.case_page import CasePage, CaseTabs
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.generate_document_page import GeneratedDocument

scenarios("../features/generated_documents.feature", strict_gherkin=False)


@given("I create a template")
def create_template(add_a_document_template):
    pass


@when("I click on the Generate document button")
def click_generated_documents(driver, context):
    CasePage(driver).change_tab(CaseTabs.DOCUMENTS)
    ApplicationPage(driver).click_generate_document_button()


@when(parsers.parse('I add my custom text "{custom_text}"'))
def add_custom_text(driver, context, custom_text):
    GeneratedDocument(driver).add_text_to_edit_text(custom_text)


@when("I click regenerate")
def click_regenerate(driver, context):
    GeneratedDocument(driver).click_regenerate_button()


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
    latest_document = GeneratedDocument(driver).get_latest_document()

    assert context.document_template_name in latest_document.text
    assert "Generated" in latest_document.text
    assert GeneratedDocument(driver).check_download_link_is_present(latest_document)


@then("I see both my generated documents")
def both_generated_documents(driver, context):
    documents = GeneratedDocument(driver).get_documents()

    for document in GeneratedDocument(driver).get_documents():
        assert context.document_template_name in document.text
        assert "Generated" in document.text
        assert GeneratedDocument(driver).check_download_link_is_present(document)

    # Check 2 documents have been created
    assert documents[0].text != documents[1].text
