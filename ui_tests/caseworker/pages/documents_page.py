from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class DocumentsPage(BasePage):
    ATTACH_DOCS_BUTTON = "button-attach-document"  # ID
    DOCUMENT_DETAILS_CLASS_NAME = "app-documents__item-details"

    def click_attach_documents(self):
        return self.driver.find_element(by=By.ID, value=self.ATTACH_DOCS_BUTTON).click()

    def get_uploaded_documents(self):
        return [
            element.text.split("\n")[0]
            for element in self.driver.find_elements(by=By.CLASS_NAME, value=self.DOCUMENT_DETAILS_CLASS_NAME)
        ]
