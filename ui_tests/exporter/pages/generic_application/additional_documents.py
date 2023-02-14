from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage

from tests_common import functions
from tests_common.functions import element_with_id_exists


class AdditionalDocumentsPage(BasePage):
    REMOVE_ADDITIONAL_DOCUMENT_LINK = "document_delete"  # ID
    DELETE_ADDITIONAL_DOC_CONFIRM_YES = "delete_document_confirmation-yes"  # ID

    def does_remove_additional_document_exist(self, driver):
        return element_with_id_exists(driver, self.REMOVE_ADDITIONAL_DOCUMENT_LINK)

    def confirm_delete_additional_document(self):
        self.driver.find_element(by=By.ID, value=self.DELETE_ADDITIONAL_DOC_CONFIRM_YES).click()
        functions.click_submit(self.driver)

    def find_remove_additional_document_link(self):
        try:
            return self.driver.find_element(by=By.ID, value=self.REMOVE_ADDITIONAL_DOCUMENT_LINK)
        except NoSuchElementException:
            return None
