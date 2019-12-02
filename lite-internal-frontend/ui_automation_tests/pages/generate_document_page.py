from ui_automation_tests.shared.BasePage import BasePage


class GeneratedDocument(BasePage):
    PREVIEW = "preview"  # ID
    PARAGRAPHS = "paragraph_content"  # ID
    DOWNLOAD = "link-download"  # ID

    def click_letter_template(self, document_template_name):
        self.driver.find_element_by_id(document_template_name).click()

    def preview_is_shown(self):
        return self.driver.find_element_by_id(self.PREVIEW).is_displayed()

    def get_document_text(self):
        return self.driver.find_element_by_id(self.PARAGRAPHS).text

    def check_download_link_is_present(self, row):
        return row.find_element_by_id(self.DOWNLOAD).is_displayed()
