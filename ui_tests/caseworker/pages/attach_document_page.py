from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class AttachDocumentPage(BasePage):
    FILE = "file"  # id
    DESCRIPTION = "description"  # id
    SUBMIT_BTN = '.govuk-button[value="submit"]'  # css

    def choose_file(self, file_location_path):
        self.driver.find_element(by=By.ID, value=self.FILE).send_keys(file_location_path)

    def enter_description(self, description):
        self.driver.find_element(by=By.ID, value=self.DESCRIPTION).send_keys(description)

    def click_submit_btn(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.SUBMIT_BTN).click()
