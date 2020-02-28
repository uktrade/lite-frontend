from ui_automation_tests.shared.BasePage import BasePage


class AttachDocumentPage(BasePage):
    FILE = "document"  # ID
    DESCRIPTION = "description"  # ID
    ADDED_DOCUMENT_ITEM = ".lite-card--download"  # CSS
    LINK_SKIP_UPLOAD_ID = "return_to_application"

    def choose_file(self, file_location_path):
        self.driver.find_element_by_id(self.FILE).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.DESCRIPTION).send_keys(description)

    def get_text_of_document_added_item(self):
        return self.driver.find_element_by_css_selector(self.ADDED_DOCUMENT_ITEM).text

    def click_save_and_return_to_overview_link(self):
        self.driver.find_element_by_id(self.LINK_SKIP_UPLOAD_ID).click()
