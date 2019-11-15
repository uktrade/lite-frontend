class DocumentsPage:
    def __init__(self, driver):
        self.driver = driver
        self.attach_docs_button = "button-attach-document"  # ID
        self.doc_description = "tbody tr td:nth-of-type(1)"  # CSS
        self.doc_filename = "tbody tr th"  # CSS

    def click_attach_documents(self):
        return self.driver.find_element_by_id(self.attach_docs_button).click()

    def get_document_description_at_position(self, position: int):
        return self.driver.find_elements_by_css_selector(self.doc_description)[position].text

    def get_document_filename_at_position(self, position: int):
        return self.driver.find_elements_by_css_selector(self.doc_filename)[position].text
