from ui_automation_tests.shared.BasePage import BasePage


class GeneratedDocument(BasePage):
    PREVIEW = "preview"  # ID
    PARAGRAPHS = "paragraph_content"  # ID
    DOWNLOAD = "link-download"  # ID
    TEXT = "text"  # ID
    ADD_PARAGRAPHS = "add_paragraphs"  # name
    PARAGRAPH_CHECKBOXES = ".govuk-checkboxes__input"  # CSS
    REGENERATE_LINK = "regenerate"  # ID

    def click_letter_template(self, document_template_name):
        self.driver.find_element_by_id(document_template_name).click()

    def preview_is_shown(self):
        return self.driver.find_element_by_id(self.PREVIEW).is_displayed()

    def get_document_text_in_preview(self):
        return self.driver.find_element_by_id(self.PARAGRAPHS).text

    def check_download_link_is_present(self, row):
        return row.find_element_by_id(self.DOWNLOAD).is_displayed()

    def get_document_text_in_edit_text_area(self):
        return self.driver.find_element_by_id(self.TEXT).text

    def click_add_paragraphs_link(self):
        self.driver.find_element_by_name(self.ADD_PARAGRAPHS).click()

    def select_and_return_first_checkbox_value(self):
        checkbox = self.driver.find_element_by_css_selector(self.PARAGRAPH_CHECKBOXES)
        checkbox.click()
        return checkbox.get_attribute("value")

    def add_text_to_edit_text(self, text):
        return self.driver.find_element_by_id(self.TEXT).send_keys(text)

    def click_regenerate_btn(self):
        self.driver.find_element_by_id(self.REGENERATE_LINK).click()
