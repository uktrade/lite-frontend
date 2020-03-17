from shared.BasePage import BasePage


class DocumentsPage(BasePage):
    ATTACH_DOCS_BUTTON = "button-attach-document"  # ID
    DOC_DESCRIPTION_ID = "document-description"
    DOC_FILENAME_ID = "document-name"
    DOC_TYPE_ID = "document-type"

    def click_attach_documents(self):
        return self.driver.find_element_by_id(self.ATTACH_DOCS_BUTTON).click()

    def get_document_description_at_position(self, position: int):
        return self.driver.find_elements_by_id(self.DOC_DESCRIPTION_ID)[position].text

    def get_document_filename_at_position(self, position: int):
        return self.driver.find_elements_by_id(self.DOC_FILENAME_ID)[position].text

    def get_document_type_at_position(self, position: int):
        return self.driver.find_elements_by_id(self.DOC_TYPE_ID)[position].text
