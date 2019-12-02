from shared.BasePage import BasePage


class DocumentsPage(BasePage):
    ATTACH_DOCS_BUTTON = "button-attach-document"  # ID
    DOC_DESCRIPTION = "tbody tr td:nth-of-type(2)"  # CSS
    DOC_FILENAME = "tbody tr th"  # CSS

    def click_attach_documents(self):
        return self.driver.find_element_by_id(self.ATTACH_DOCS_BUTTON).click()

    def get_document_description_at_position(self, position: int):
        return self.driver.find_elements_by_css_selector(self.DOC_DESCRIPTION)[position].text

    def get_document_filename_at_position(self, position: int):
        return self.driver.find_elements_by_css_selector(self.DOC_FILENAME)[position].text
