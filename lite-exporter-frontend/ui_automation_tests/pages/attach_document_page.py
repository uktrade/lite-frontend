from shared.BasePage import BasePage


class AttachDocumentPage(BasePage):

    FILE = "file"  # ID
    DESCRIPTION = "description"  # ID
    ADDED_DOCUMENT_ITEM = ".lite-card--download"  # CSS

    def choose_file(self, file_location_path):
        self.driver.find_element_by_id(self.FILE).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.DESCRIPTION).send_keys(description)

    def get_text_of_document_added_item(self):
        return self.driver.find_element_by_css_selector(self.ADDED_DOCUMENT_ITEM).text
