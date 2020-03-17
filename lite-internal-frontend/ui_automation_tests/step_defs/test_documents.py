import os

from pytest_bdd import when, then, scenarios, parsers

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
from ui_automation_tests.pages.documents_page import DocumentsPage

scenarios("../features/documents.feature", strict_gherkin=False)


@when("I click on the Attach Document button")
def click_attach_documents(driver):
    documents_page = DocumentsPage(driver)
    documents_page.click_attach_documents()


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))
def upload_a_file(driver, filename, description):
    attach_document_page = AttachDocumentPage(driver)

    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "resources", filename))

    attach_document_page.choose_file(file_to_upload_abs_path)
    attach_document_page.enter_description(description)
    attach_document_page.click_submit_btn()


@then(parsers.parse('file "{filename}" with description "{description}" is on position "{position}"'))
def check_file2_is_uploaded(driver, filename, description, position):
    documents_page = DocumentsPage(driver)
    assert documents_page.get_document_filename_at_position(int(position)) == filename, filename + " is not uploaded"
    assert documents_page.get_document_description_at_position(int(position)) == description, (
        description + " is not uploaded"
    )


@then("I can click on the good document download link")
def can_click_on_the_good_document_download_link(driver):
    assert ApplicationPage(driver).good_document_link_is_enabled()


@then("I can click on the end user document download link")
def can_click_on_the_end_user_document_download_link(driver):
    assert ApplicationPage(driver).end_user_document_link_is_enabled()


@then("I can click on the additional document download link")
def can_click_on_the_additional_document_download_link(driver):
    assert ApplicationPage(driver).additional_document_link_is_enabled()
