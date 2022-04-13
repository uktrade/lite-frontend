from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.exporter.pages.BasePage import BasePage


class RespondToEcjuQueryPage(BasePage):
    RESPONSE_FORM = "response"  # ID
    DOCUMENT_INFORMATION_TEXT = "lite-information-text__text"
    UPLOADED_DOCUMENT_ITEM_CLASS = "app-documents__item"

    def enter_form_response(self, value):
        response_tb = self.driver.find_element(by=By.ID, value=self.RESPONSE_FORM)
        response_tb.clear()
        response_tb.send_keys(value)

    def get_missing_document_reason_text(self):
        element = self.driver.find_element_by_class_name(self.DOCUMENT_INFORMATION_TEXT)
        return element.text.split("\n")[1].strip()

    def get_uploaded_document_items(self):
        return self.driver.find_elements_by_class_name(self.UPLOADED_DOCUMENT_ITEM_CLASS)

    def get_uploaded_documents_delete_links(self):
        return self.driver.find_elements_by_link_text("Delete")


class DocumentGradingPage(BasePage):
    DOCUMENT_AVAILABLE_FOR_UPLOAD = "has_document_to_upload-"
    ECJU_HELPLINE_ID = "conditional-has_document_to_upload-no-conditional"
    MISSING_DOCUMENT_REASON = "missing_document_reason"  # ID

    def confirm_upload_document(self, option):
        # The only options accepted here are 'yes', 'no'
        self.driver.find_element_by_id(self.DOCUMENT_AVAILABLE_FOR_UPLOAD + option.lower()).click()

    def get_ecju_help(self):
        return self.driver.find_element_by_id(self.ECJU_HELPLINE_ID).is_displayed()

    def select_valid_missing_document_reason(self):
        Select(self.driver.find_element_by_id(self.MISSING_DOCUMENT_REASON)).select_by_index(2)
