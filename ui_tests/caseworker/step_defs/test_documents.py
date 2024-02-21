from pytest_bdd import when, then, scenarios, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.attach_document_page import AttachDocumentPage
from ui_tests.caseworker.pages.documents_page import DocumentsPage

scenarios("../features/documents.feature", strict_gherkin=False)


@when("I click on the Attach Document button")
def click_attach_documents(driver):
    documents_page = DocumentsPage(driver)
    documents_page.click_attach_documents()


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))
def upload_a_file(driver, filename, description, tmp_path):
    attach_document_page = AttachDocumentPage(driver)

    named_file = tmp_path / filename
    named_file.write_text("file contents")

    attach_document_page.choose_file(str(named_file))
    attach_document_page.enter_description(description)

    old_page = driver.find_element(by=By.TAG_NAME, value="html")
    attach_document_page.click_submit_btn()
    WebDriverWait(driver, 45).until(expected_conditions.staleness_of(old_page))


@then(parsers.parse('I see a file with filename "{filename}" is uploaded'))
def verify_file_uploaded(driver, filename):
    document_names = DocumentsPage(driver).get_uploaded_documents()
    assert filename in document_names


@then("I can click on the consignee document download link")
def can_click_on_the_consignee_document_download_link(driver):
    assert ApplicationPage(driver).consignee_document_link_is_enabled()


@then("I can click on the end user document download link")
def can_click_on_the_end_user_document_download_link(driver):
    assert ApplicationPage(driver).end_user_document_link_is_enabled()


@then("I can click on the additional document download link")
def can_click_on_the_additional_document_download_link(driver):
    assert ApplicationPage(driver).additional_document_link_is_enabled()
