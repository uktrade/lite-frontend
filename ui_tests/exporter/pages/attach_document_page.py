from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class AttachDocumentPage(BasePage):
    FILE = "file"  # ID
    DESCRIPTION = "description"  # ID
    LINK_SKIP_UPLOAD_ID = "return_to_application"

    def choose_file(self, file_location_path):
        self.driver.find_element(by=By.ID, value=self.FILE).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element(by=By.ID, value=self.DESCRIPTION).send_keys(description)

    def click_save_and_return_to_overview_link(self):
        self.driver.find_element(by=By.ID, value=self.LINK_SKIP_UPLOAD_ID).click()
