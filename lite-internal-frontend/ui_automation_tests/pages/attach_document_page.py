from shared.BasePage import BasePage


class AttachDocumentPage(BasePage):
    FILE = "file"  # id
    DESCRIPTION = "description"  # id
    SUBMIT_BTN = '.govuk-button[value="submit"]'  # css

    def choose_file(self, file_location_path):
        self.driver.find_element_by_id(self.FILE).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.DESCRIPTION).send_keys(description)

    def click_submit_btn(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BTN).click()
